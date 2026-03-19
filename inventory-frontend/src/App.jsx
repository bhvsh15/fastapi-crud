import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { getToken } from './api/api'
import Login from './pages/Login'
import Register from './pages/Register'

function ProtectedRoute({ children }) {
  if (!getToken()) return <Navigate to="/login" replace />
  return children
}

function PublicRoute({ children }) {
  if (getToken()) return <Navigate to="/login" replace />
  return children
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<PublicRoute><Login /></PublicRoute>} />
        <Route path="/register" element={<PublicRoute><Register /></PublicRoute>} />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  )
}