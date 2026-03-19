import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { loginUser, saveToken } from '../api/api'

export default function Login() {
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError]       = useState('')
  const [loading, setLoading]   = useState(false)

  async function handleLogin(e) {
    e.preventDefault()
    setError('')

    if (!username || !password) {
      setError('Please enter your username and password.')
      return
    }

    setLoading(true)
    try {
      const data = await loginUser(username, password)
      saveToken(data.access_token)
      localStorage.setItem('token_type', data.token_type)
      navigate('/items')
    } catch (err) {
      setError(err.message || 'Login failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-tag">Inventory System</div>
      <h1 className="auth-title">Welcome back.</h1>
      <p className="auth-subtitle">Sign in to manage your inventory, workers and supplies.</p>

      <div className="auth-card">
        {error && <div className="alert error visible">{error}</div>}

        <form onSubmit={handleLogin}>
          <div className="field">
            <label>Username</label>
            <input
              type="text"
              placeholder="your_username"
              value={username}
              onChange={e => setUsername(e.target.value)}
              autoComplete="username"
            />
          </div>

          <div className="field">
            <label>Password</label>
            <input
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={e => setPassword(e.target.value)}
              autoComplete="current-password"
            />
          </div>

          <button
            type="submit"
            className="btn-primary"
            style={{ width: '100%', marginTop: '0.5rem' }}
            disabled={loading}
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>
      </div>

      <div className="auth-footer">
        Don't have an account? <Link to="/register">Register</Link>
      </div>
    </div>
  )
}
