import { SignIn } from '@clerk/clerk-react'

const LoginPage = () => {
  return (
    <div className="auth-layout">
      <div className="auth-container">
        <div className="auth-brand">
          <h1>Shopify Automation Agent</h1>
          <p>Manage your e-commerce operations with ease</p>
        </div>

        <SignIn
          appearance={{
            elements: {
              rootBox: {
                width: '100%',
              },
              card: {
                boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
                borderRadius: '16px',
                padding: '32px',
                background: '#ffffff',
                border: '1px solid #e2e8f0',
              },
              headerTitle: {
                fontSize: '1.5rem',
                fontWeight: '700',
                color: '#0f172a',
              },
              headerSubtitle: {
                color: '#475569',
                fontSize: '0.9375rem',
              },
              socialButtonsBlockButton: {
                border: '1px solid #e2e8f0',
                background: '#ffffff',
                fontSize: '0.9375rem',
                padding: '12px',
                borderRadius: '12px',
                transition: 'all 0.2s ease',
              },
              socialButtonsBlockButtonText: {
                fontWeight: '600',
              },
              formFieldInput: {
                borderRadius: '12px',
                border: '1px solid #e2e8f0',
                background: '#ffffff',
                padding: '12px 16px',
                fontSize: '0.9375rem',
              },
              formButtonPrimary: {
                background: '#2563eb',
                borderRadius: '12px',
                padding: '12px',
                fontSize: '0.9375rem',
                fontWeight: '600',
                textTransform: 'none',
                boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
              },
              footerActionLink: {
                color: '#2563eb',
                fontWeight: '600',
              },
              identityPreviewText: {
                fontWeight: '500',
              },
              formFieldLabel: {
                color: '#0f172a',
                fontWeight: '600',
                fontSize: '0.875rem',
              },
              dividerLine: {
                background: '#e2e8f0',
              },
              dividerText: {
                color: '#475569',
              },
            },
            layout: {
              socialButtonsPlacement: 'bottom',
              logoPlacement: 'none'
            }
          }}
          routing="path"
          path="/login"
          afterSignInUrl="/dashboard"
          afterSignUpUrl="/dashboard"
        />
      </div>
    </div>
  )
}

export default LoginPage
