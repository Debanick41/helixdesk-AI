
import { useState } from 'react'
import { login } from './auth'

export default function Login({ onLogin }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')
    setLoading(true)

    try {
      await login(email, password)
      onLogin()
    } catch (err) {
      setError(err.message || 'Login failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main style={{
      maxWidth: '400px',
      margin: '80px auto',
      padding: '32px',
      fontFamily: 'Arial, sans-serif',
    }}>
      <h1>HelixDesk AI</h1>
      <p>Sign in to your support workspace.</p>

      <form onSubmit={handleSubmit}>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          autoComplete="username"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          required
          style={{ display: 'block', width: '100%', margin: '8px 0 16px', padding: '10px', boxSizing: 'border-box' }}
        />

        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          autoComplete="current-password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          required
          style={{ display: 'block', width: '100%', margin: '8px 0 16px', padding: '10px', boxSizing: 'border-box' }}
        />

        {error && (
          <p role="alert" style={{ color: '#dc2626' }}>
            {error}
          </p>
        )}

        <button type="submit" disabled={loading}>
          {loading ? 'Signing in...' : 'Sign in'}
        </button>
      </form>
    </main>
  )
}
