import { useEffect, useMemo, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import api from '../lib/api'

const ProductDetailsPage = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchMetrics = async () => {
      setLoading(true)
      setError('')
      try {
        const response = await api.get(`/products/${id}/metrics`)
        setData(response.data)
      } catch (err) {
        setError('Failed to load product metrics')
      } finally {
        setLoading(false)
      }
    }

    fetchMetrics()
  }, [id])

  const metrics = useMemo(() => {
    const sales = data?.sales ?? data?.metrics?.sales ?? 0
    const revenue = data?.revenue ?? data?.metrics?.revenue ?? 0
    const views = data?.views ?? data?.metrics?.views ?? 0

    return [
      { label: 'Sales', value: sales },
      { label: 'Revenue', value: revenue },
      { label: 'Views', value: views }
    ]
  }, [data])

  const maxValue = Math.max(...metrics.map((metric) => metric.value), 1)

  return (
    <div className="page-layout">
      <button type="button" className="link-button" onClick={() => navigate(-1)}>
        ← Back
      </button>

      <section className="card detail-card">
        {loading && <p>Loading metrics…</p>}
        {error && <p className="form-error">{error}</p>}

        {!loading && !error && (
          <>
            <p className="eyebrow">Product #{id}</p>
            <h1>{data?.name ?? data?.title ?? 'Product details'}</h1>
            <p>{data?.description ?? data?.summary ?? 'No description provided.'}</p>

            <div className="metrics-grid">
              {metrics.map((metric) => (
                <div key={metric.label} className="metric">
                  <div className="metric-header">
                    <span>{metric.label}</span>
                    <strong>{metric.value}</strong>
                  </div>
                  <div className="metric-bar">
                    <span
                      style={{
                        width: `${(metric.value / maxValue) * 100 || 0}%`
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </>
        )}
      </section>
    </div>
  )
}

export default ProductDetailsPage
