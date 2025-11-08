import { useEffect } from 'react'
import { Navigate, Outlet, Route, Routes } from 'react-router-dom'
import { useAuth } from '@clerk/clerk-react'
import DashboardPage from './pages/DashboardPage'
import LoginPage from './pages/LoginPage'
import ProductDetailsPage from './pages/ProductDetailsPage'
import ProductAnalytics from './pages/ProductAnalytics'
import './App.css'

const TokenSynchronizer = () => {
  const { isLoaded, isSignedIn, getToken } = useAuth()

  useEffect(() => {
    if (!isLoaded) return
    let active = true

    const syncToken = async () => {
      if (!isSignedIn) {
        localStorage.removeItem('token')
        return
      }
      const token = await getToken()
      if (active) {
        if (token) {
          localStorage.setItem('token', token)
        } else {
          localStorage.removeItem('token')
        }
      }
    }

    syncToken()
    const interval = setInterval(syncToken, 5 * 60 * 1000)

    return () => {
      active = false
      clearInterval(interval)
    }
  }, [getToken, isLoaded, isSignedIn])

  return null
}

const ProtectedRoute = () => {
  const { isLoaded, isSignedIn } = useAuth()

  if (!isLoaded) {
    return (
      <div className="page-layout">
        <p>Checking session…</p>
      </div>
    )
  }

  if (!isSignedIn) {
    return <Navigate to="/login" replace />
  }

  return (
    <>
      <TokenSynchronizer />
      <Outlet />
    </>
  )
}

const PublicOnlyRoute = () => {
  const { isLoaded, isSignedIn } = useAuth()

  if (!isLoaded) {
    return (
      <div className="auth-layout">
        <p>Loading…</p>
      </div>
    )
  }

  return isSignedIn ? <Navigate to="/dashboard" replace /> : <Outlet />
}

const AppRoutes = () => (
  <Routes>
    <Route element={<PublicOnlyRoute />}>
      <Route path="/login" element={<LoginPage />} />
    </Route>

    <Route element={<ProtectedRoute />}>
      <Route path="/dashboard" element={<DashboardPage />} />
      <Route path="/product/:id" element={<ProductDetailsPage />} />
      <Route path="/product/:id/analytics" element={<ProductAnalytics />} />
    </Route>

    <Route path="*" element={<Navigate to="/dashboard" replace />} />
  </Routes>
)

const App = () => <AppRoutes />

export default App
