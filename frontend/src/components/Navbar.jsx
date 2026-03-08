import { ArrowLeft, Briefcase } from 'lucide-react'
import './Navbar.css'

export default function Navbar({ onReset, showBack }) {
  return (
    <nav className="nav">
      <div className="nav-inner">
        <div className="nav-brand" onClick={onReset}>
          <span className="nav-logo-mark">
            <Briefcase size={16} strokeWidth={2} />
          </span>
          <span className="nav-logo-text">ApplyAI</span>
        </div>

        {showBack && (
          <button className="nav-back-btn" onClick={onReset}>
            <ArrowLeft size={15} />
            New application
          </button>
        )}
      </div>
    </nav>
  )
}
