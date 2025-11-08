import { useCallback, useEffect, useMemo, useState } from 'react'
import { useClerk } from '@clerk/clerk-react'
import { useAsyncError, useNavigate } from 'react-router-dom'
import {api, fastapi} from '../lib/api'

const ProductAnalytics = (productID) => {
  const navigate = useNavigate()
  const { signOut } = useClerk()
  const [form, setForm] = useState(emptyForm)
  const [formMessage, setFormMessage] = useState('')
  const [formError, setFormError] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [reasoning, setReasoning] = useState('')
  const [products, setProducts] = useState([])
  const [listLoading, setListLoading] = useState(true)
  const [listError, setListError] = useState('')

  const fetchProducts = useCallback(async () => {
    setListLoading(true)
    setListError('')
    try {
      const { data } = await api.get('/shopify/products')
      console.log(data)
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
      const resp = await fastapi.post('/products_analyze', {
        name: form.name,
        description: form.description,
        minPrice: Number(form.minPrice),
        maxPrice: Number(form.maxPrice)
      })

      setFormMessage('Product sent for analysis')
      const data = resp.data

      console.log("Recent data: ", data)
      console.log("Reasoning: ", data.reasoning)

      setReasoning(data.reasoning)


      alert(reasoning)

      

      console.log('FOrwarded data ', {
        title:data.product_name,
        body_html:form.description,
        vendor:"Adith's Store",
        product_type:"General",
        price:data.recommended_price,
        sku:"211N"
      })

      const res = await api.post("/shopify/create",{
        title:data.product_name,
        body_html:form.description,
        vendor:"Adith's Store",
        product_type:"General",
        price:data.recommended_price,
        sku:"211N"
      })

      console.log(res.data)

      
      setForm(emptyForm)
      
    } catch (err) {
      setFormError('Failed to send product for analysis')
    } finally {
      setSubmitting(false)
    }
  }
  const parsedProducts = useMemo(() => {
  return products.map((product) => {
    const variants = product.variants ?? [];

    // compute average price if variants exist
    let avgPrice = null;
    if (variants.length > 0) {
      const numericPrices = variants
        .map(v => parseFloat(v.price))
        .filter(p => !isNaN(p));
      if (numericPrices.length > 0) {
        avgPrice =
          numericPrices.reduce((sum, p) => sum + p, 0) / numericPrices.length;
      }
    }

    return {
      id: product.id ?? product._id ?? product.productId ?? product?.metricsId,
      title: product.title ?? product.name ?? 'Untitled',
      price:
        avgPrice !== null
          ? `$${avgPrice.toFixed(2)}`
          : product.price ?? product.priceUsd ?? '—',
      status: product.status ?? product.state ?? 'Unknown',
      sales: product.sales ?? product.metrics?.sales ?? 0,
      revenue: product.revenue ?? product.metrics?.revenue ?? 0,
    };
  });
}, [products]);


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
        HELLO 
      </div>
    </div>
  )
}

export default ProductAnalytics
