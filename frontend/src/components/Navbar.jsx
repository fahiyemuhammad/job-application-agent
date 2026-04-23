import { motion } from 'framer-motion'
import { ArrowLeft, Briefcase, Sparkles } from 'lucide-react'
import './Navbar.css'

export default function Navbar({ onReset, showBack }) {
  return (
    <motion.nav 
      className="nav-container"
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ type: 'spring', damping: 20, stiffness: 100 }}
    >
      <div className="nav-blur-bg" />
      <div className="nav-content">
        <div className="nav-brand" onClick={onReset}>
          <div className="nav-logo-outer">
            <Briefcase size={18} strokeWidth={2.5} />
            <motion.div 
              className="logo-glow"
              animate={{ opacity: [0.4, 0.8, 0.4] }}
              transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
            />
          </div>
          <span className="nav-logo-text">ApplyAI<span className="text-primary">.</span></span>
        </div>

        {showBack ? (
          <motion.button 
            className="nav-back-btn" 
            onClick={onReset}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <ArrowLeft size={16} />
            <span>New Application</span>
          </motion.button>
        ) : (
          <div className="nav-stats">
            <Sparkles size={14} className="text-secondary" />
            <span>AI Powered</span>
          </div>
        )}
      </div>
    </motion.nav>
  )
}
