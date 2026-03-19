import { NavLink, useNavigate } from 'react-router-dom'
import { getUserFromToken, clearToken } from '../api/Api'

export default function Navbar() {
  const navigate = useNavigate()
  const user = getUserFromToken()

  function logout() {
    clearToken()
    navigate('/login')
  }

  return (
    <nav className="navbar">
      <NavLink to="/items" className="nav-brand">
        Inventory <span>system</span>
      </NavLink>

      <div className="nav-links">
        <NavLink
          to="/items"
          className={({ isActive }) => isActive ? 'active' : ''}
        >
          Items
        </NavLink>
        <NavLink
          to="/suppliers"
          className={({ isActive }) => isActive ? 'active' : ''}
        >
          Suppliers
        </NavLink>
        <NavLink
          to="/inwards"
          className={({ isActive }) => isActive ? 'active' : ''}
        >
          Inwards
        </NavLink>
      </div>

      <div className="nav-right">
        {user && (
          <>
            <span className="nav-user">{user.username}</span>
            <span className={`role-badge ${user.role === 'admin' ? 'role-admin' : 'role-staff'}`}>
              {user.role}
            </span>
          </>
        )}
        <button className="btn-logout" onClick={logout}>Logout</button>
      </div>
    </nav>
  )
}
