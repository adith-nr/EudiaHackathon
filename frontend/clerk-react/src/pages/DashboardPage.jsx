import { useCallback, useEffect, useMemo, useState } from 'react'
import { useClerk } from '@clerk/clerk-react'
import { useNavigate } from 'react-router-dom'
import api from '../lib/api'

const emptyForm = {
  name: '',
  description: '',
  minPrice: '',
  maxPrice: ''
}

const DashboardPage = () => {
  const navigate = useNavigate()
  const { signOut } = useClerk()
  const [form, setForm] = useState(emptyForm)
  const [formMessage, setFormMessage] = useState('')
  const [formError, setFormError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const [products, setProducts] = useState([])
  const [listLoading, setListLoading] = useState(true)
  const [listError, setListError] = useState('')

  const fetchProducts = useCallback(async () => {
    setListLoading(true)
    setListError('')
    try {
      const { data } = await api.get('/shopify/products')
      setProducts(Array.isArray(data) ? data : data?.products ?? [])
    } catch (err) {
      setListError('Could not load products')
    } finally {
      setListLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchProducts()
  }, [fetchProducts])

  const handleChange = (event) => {
    const { name, value } = event.target
    setForm((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setSubmitting(true)
    setFormMessage('')
    setFormError('')
    try {
      await api.post('/products_analyze', {
        name: form.name,
        description: form.description,
        minPrice: Number(form.minPrice),
        maxPrice: Number(form.maxPrice)
      })
      setFormMessage('Product sent for analysis')
      setForm(emptyForm)
    } catch (err) {
      setFormError('Failed to send product for analysis')
    } finally {
      setSubmitting(false)
    }
  }

  const parsedProducts = useMemo(() => {
    return products.map((product) => ({
      id: product.id ?? product._id ?? product.productId ?? product?.metricsId,
      title: product.title ?? product.name ?? 'Untitled',
      price: product.price ?? product.priceUsd ?? '—',
      status: product.status ?? product.state ?? 'Unknown',
      sales: product.sales ?? product.metrics?.sales ?? 0,
      revenue: product.revenue ?? product.metrics?.revenue ?? 0
    }))
  }, [products])

  const handleLogout = async () => {
    localStorage.removeItem('token')
    await signOut()
    navigate('/login', { replace: true })
  }

  const handleRowClick = (id) => {
    if (!id) return
    navigate(`/product/${id}`)
  }

  return (
    <div className="page-layout">
      <header className="page-header">
        <div>
          <p className="eyebrow">Eudia Hackathon</p>
          <h1>Shopify Automation Agent</h1>
        </div>
        <button type="button" className="link-button" onClick={handleLogout}>
          Log out
        </button>
      </header>

      <div className="grid-two">
        <section className="card">
          <h2>Create Product</h2>
          <p>Send a product idea for the agent to analyze price bands.</p>

          <form className="form-grid" onSubmit={handleSubmit}>
            <label htmlFor="name">Name</label>
            <input
              id="name"
              name="name"
              placeholder="Summer linen shirt"
              value={form.name}
              onChange={handleChange}
              required
            />

            <label htmlFor="description">Description</label>
            <textarea
              id="description"
              name="description"
              rows="3"
              placeholder="Include material, audience, etc."
              value={form.description}
              onChange={handleChange}
              required
            />

            <label htmlFor="minPrice">Min price</label>
            <input
              id="minPrice"
              name="minPrice"
              type="number"
              min="0"
              step="0.01"
              value={form.minPrice}
              onChange={handleChange}
              required
            />

            <label htmlFor="maxPrice">Max price</label>
            <input
              id="maxPrice"
              name="maxPrice"
              type="number"
              min="0"
              step="0.01"
              value={form.maxPrice}
              onChange={handleChange}
              required
            />

            {formMessage && <p className="form-success">{formMessage}</p>}
            {formError && <p className="form-error">{formError}</p>}

            <button type="submit" disabled={submitting}>
              {submitting ? 'Sending…' : 'Send to agent'}
            </button>
          </form>
        </section>

        <section className="card">
          <div className="section-heading">
            <div>
              <h2>Products</h2>
              <p>Latest analyses from the agent</p>
            </div>
            <button
              type="button"
              className="link-button"
              onClick={fetchProducts}
              disabled={listLoading}
            >
              Refresh
            </button>
          </div>

          {listError && <p className="form-error">{listError}</p>}
          {listLoading ? (
            <p>Loading products…</p>
          ) : parsedProducts.length === 0 ? (
            <p>No products yet. Submit one to get started.</p>
          ) : (
            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>Title</th>
                    <th>Price</th>
                    <th>Status</th>
                    <th>Sales</th>
                    <th>Revenue</th>
                  </tr>
                </thead>
                <tbody>
                  {parsedProducts.map((product) => (
                    <tr
                      key={product.id}
                      onClick={() => handleRowClick(product.id)}
                      tabIndex={0}
                      onKeyDown={(event) => event.key === 'Enter' && handleRowClick(product.id)}
                    >
                      <td>{product.title}</td>
                      <td>{product.price}</td>
                      <td>{product.status}</td>
                      <td>{product.sales}</td>
                      <td>{product.revenue}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </div>
    </div>
  )
}

export default DashboardPage
