import { SignIn } from '@clerk/clerk-react'

const LoginPage = () => {
  return (
    <div className="auth-layout">
      <section className="auth-card">
        <h1>Shopify Automation Agent</h1>
        <p>Log in to continue</p>

        <SignIn
          appearance={{
            layout: {
              socialButtonsPlacement: 'bottom',
              logoPlacement: 'outside'
            }
          }}
          routing="path"
          path="/login"
          afterSignInUrl="/dashboard"
          afterSignUpUrl="/dashboard"
        />
      </section>
    </div>
  )
}

export default LoginPage
