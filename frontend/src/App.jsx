import { useEffect, useState } from 'react'
import './App.css'
import { apiRequest } from './api'
import Login from './Login'
import { getAccessToken, logout, getCustomers } from './auth'

const stats = [
  { label: 'Total Tickets', value: '248', change: '+12.5%', icon: 'â–¤' },
  { label: 'Open Tickets', value: '36', change: 'Needs attention', icon: 'â—·' },
  { label: 'Resolved Today', value: '52', change: '+8.2%', icon: 'âœ“' },
  { label: 'Avg. Response', value: '4m 32s', change: '-18% this week', icon: 'ÏŸ' },
]

const tickets = [
  { id: '#HD-1024', customer: 'Olivia Martin', initials: 'OM', subject: 'Unable to access my account', priority: 'High', status: 'Open', time: '5 min ago' },
  { id: '#HD-1023', customer: 'Jackson Lee', initials: 'JL', subject: 'Payment confirmation missing', priority: 'Medium', status: 'In Progress', time: '18 min ago' },
  { id: '#HD-1022', customer: 'Isabella Chen', initials: 'IC', subject: 'How can I update my profile?', priority: 'Low', status: 'Resolved', time: '32 min ago' },
  { id: '#HD-1021', customer: 'William Kim', initials: 'WK', subject: 'Subscription renewal issue', priority: 'High', status: 'Open', time: '47 min ago' },
  { id: '#HD-1020', customer: 'Sophia Patel', initials: 'SP', subject: 'Request for invoice copy', priority: 'Low', status: 'Resolved', time: '1 hour ago' },
]

const navigation = [
  { icon: 'â–¦', label: 'Overview' },
  { icon: 'â–¤', label: 'All Tickets', count: '36' },
  { icon: 'â™™', label: 'Customers' },
  { icon: 'âœ§', label: 'AI Assistant' },
]

function App() {

  const [isAuthenticated, setIsAuthenticated] = useState(
  Boolean(getAccessToken())
)
  const [apiStatus, setApiStatus] = useState('Checking...')
  const [customers, setCustomers] = useState([])
  const [customersLoading, setCustomersLoading] = useState(true)
  const [customersError, setCustomersError] = useState('')

  useEffect(() => {
    apiRequest('/health')
      .then(() => setApiStatus('Connected'))
      .catch(() => setApiStatus('Disconnected'))
  }, [])

  useEffect(() => {
    if (!isAuthenticated) return

    let cancelled = false

    getCustomers()
      .then((data) => {
        if (!cancelled) {
          setCustomers(data)
          setCustomersError('')
        }
      })
      .catch((error) => {
        if (!cancelled) {
          setCustomersError(error.message || 'Could not load customers.')
        }
      })
      .finally(() => {
        if (!cancelled) {
          setCustomersLoading(false)
        }
      })

    return () => {
      cancelled = true
    }
  }, [isAuthenticated])

   if (!isAuthenticated)
    return <Login onLogin={() => setIsAuthenticated(true)} />
}



  return (
    <div className="app-shell">
      <aside className="sidebar">
        <a className="brand" href="#" aria-label="HelixDesk home">
          <span className="brand-mark">H</span>
          <span>HelixDesk<span className="brand-ai"> AI</span></span>
        </a>

        <div className="workspace-label">WORKSPACE</div>
        <div className="workspace">
          <div className="workspace-icon">H</div>
          <div className="workspace-info">
            <strong>HelixDesk Team</strong>
            <span>Free workspace</span>
          </div>
          <span className="workspace-chevron">âŒ„</span>
        </div>

        <div className="nav-label">MENU</div>
        <nav className="navigation" aria-label="Main navigation">
          {navigation.map((item) => (
            <a
              href="#"
              key={item.label}
              className={`nav-item ${item.label === 'Overview' ? 'active' : ''}`}
              onClick={(event) => event.preventDefault()}
            >
              <span className="nav-icon">{item.icon}</span>
              <span>{item.label}</span>
              {item.count && <span className="nav-count">{item.count}</span>}
            </a>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="ai-card">
            <div className="ai-card-icon">âœ¦</div>
            <strong>AI-powered support</strong>
            <p>Let AI help your team resolve tickets faster.</p>
            <button onClick={() => alert('AI Assistant integration is coming soon.')}>
              Explore AI <span>â†—</span>
            </button>
          </div>
          <a href="#" className="nav-item settings-link" onClick={(event) => event.preventDefault()}>
            <span className="nav-icon">âš™</span>
            Settings
          </a>
          <div className="profile">
            <div className="avatar profile-avatar">DB</div>
            <div className="profile-info">
              <strong>Workspace Admin</strong>
              <span>Administrator</span>
            </div>
            <span className="workspace-chevron">â€¢â€¢â€¢</span>
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div className="breadcrumbs">Workspace <span>/</span> <strong>Overview</strong></div>
          <div className="topbar-actions">
            <div className="system-status">
              <span />
              API: {apiStatus}
           </div>
            <button className="icon-button" aria-label="Notifications">â™§<i /></button>
            <div className="avatar top-avatar">DB</div>
          </div>
        </header>

        <div className="dashboard">
          <section className="welcome-row">
            <div>
              <div className="eyebrow"><span className="eyebrow-dot" /> CUSTOMER SUPPORT WORKSPACE</div>
              <h1>Good afternoon ðŸ‘‹</h1>
              <p className="subtitle">Here's what's happening with your support team today.</p>
            </div>
            <button className="primary-button" onClick={() => alert('New ticket creation will be connected to FastAPI next.')}>
              <span>ï¼‹</span> Create ticket
            </button>
          </section>

          <section className="stats-grid" aria-label="Support statistics">
            {stats.map((stat, index) => (
              <article className="stat-card" key={stat.label}>
                <div className="stat-top">
                  <span className={`stat-icon stat-icon-${index}`}>{stat.icon}</span>
                  <button className="more-button" aria-label={`${stat.label} options`}>Â·Â·Â·</button>
                </div>
                <p className="stat-label">{stat.label}</p>
                <div className="stat-value">{stat.value}</div>
                <div className={`stat-change ${index === 1 ? 'neutral-change' : ''}`}>
                  {index !== 1 && <span>{index === 3 ? 'â†˜' : 'â†—'}</span>}
                  {stat.change}
                </div>
              </article>
            ))}
          </section>

          <section className="customers-section">
            <div className="section-heading">
              <div>
                <h2>Customers</h2>
                <p>Customer records from your HelixDesk database.</p>
              </div>
              <span className="nav-count">{customers.length} total</span>
            </div>

            {customersLoading ? (
              <p>Loading customers...</p>
            ) : customersError ? (
              <p role="alert">{customersError}</p>
            ) : customers.length === 0 ? (
              <p>No customers yet. Add a customer to see records here.</p>
            ) : (
              <div className="table-wrap">
                <table className="tickets-table">
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Email</th>
                      <th>Created</th>
                    </tr>
                  </thead>
                  <tbody>
                    {customers.map((customer) => (
                      <tr key={customer.id}>
                        <td>{customer.name}</td>
                        <td>{customer.email}</td>
                        <td>
                          {customer.created_at
                            ? new Date(customer.created_at).toLocaleDateString()
                            : '—'}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </section>
          <section className="ticket-section">
            <div className="section-heading">
              <div>
                <h2>Recent tickets</h2>
                <p>Keep track of your latest customer conversations.</p>
              </div>
              <button className="secondary-button" onClick={() => alert('Ticket filtering will be added in a later step.')}>
                <span>â˜·</span> Filters
              </button>
            </div>

            <div className="ticket-toolbar">
              <div className="ticket-tabs">
                <button className="ticket-tab selected">All tickets <span>248</span></button>
                <button className="ticket-tab">Open <span>36</span></button>
                <button className="ticket-tab">Resolved</button>
              </div>
              <label className="search-box">
                <span>âŒ•</span>
                <input type="search" placeholder="Search tickets..." aria-label="Search tickets" />
              </label>
            </div>

            <div className="table-wrap">
              <table className="tickets-table">
                <thead>
                  <tr>
                    <th>Ticket</th>
                    <th>Customer</th>
                    <th>Subject</th>
                    <th>Priority</th>
                    <th>Status</th>
                    <th>Created</th>
                  </tr>
                </thead>
                <tbody>
                  {tickets.map((ticket) => (
                    <tr key={ticket.id}>
                      <td className="ticket-id">{ticket.id}</td>
                      <td>
                        <div className="customer-cell">
                          <span className="avatar customer-avatar">{ticket.initials}</span>
                          <span>{ticket.customer}</span>
                        </div>
                      </td>
                      <td className="ticket-subject">{ticket.subject}</td>
                      <td>
                        <span className={`priority priority-${ticket.priority.toLowerCase()}`}>
                          <span />{ticket.priority}
                        </span>
                      </td>
                      <td><span className={`status status-${ticket.status.toLowerCase().replace(' ', '-')}`}>{ticket.status}</span></td>
                      <td className="ticket-time">{ticket.time}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="table-footer">
              <span>Showing <strong>5</strong> of <strong>248</strong> tickets</span>
              <div className="pagination">
                <button disabled aria-label="Previous page">â†</button>
                <button className="page-active">1</button>
                <button>2</button>
                <button>3</button>
                <span>â€¦</span>
                <button>50</button>
                <button aria-label="Next page">â†’</button>
              </div>
            </div>
          </section>

          <footer className="dashboard-footer">
            <span>Â© 2026 HelixDesk AI</span>
            <span>Built for better customer experiences <span className="footer-heart">â™¥</span></span>
          </footer>
        </div>
      </main>
    </div>
  )
}

export default App
