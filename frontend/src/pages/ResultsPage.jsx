import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import toast from 'react-hot-toast'
import {
  CheckCircle2, XCircle, Download, Copy, RefreshCw,
  TrendingUp, AlertCircle, Sparkles, ChevronDown, ChevronUp, FileText, Zap
} from 'lucide-react'
import './ResultsPage.css'

const containerVariants = {
  hidden: { opacity: 0 },
  visible: { 
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
}

const itemVariants = {
  hidden: { y: 20, opacity: 0 },
  visible: { y: 0, opacity: 1 }
}

function ScoreRing({ score }) {
  const radius = 42
  const circ = 2 * Math.PI * radius
  const offset = circ - (score / 100) * circ
  const color =
    score >= 70 ? 'var(--success)' :
    score >= 40 ? 'var(--warning)' :
    'var(--danger)'

  return (
    <div className="modern-score-ring">
      <svg width="120" height="120" viewBox="0 0 120 120">
        <circle cx="60" cy="60" r={radius} fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="10" />
        <motion.circle
          cx="60" cy="60" r={radius} fill="none"
          stroke={color} strokeWidth="10"
          strokeLinecap="round"
          strokeDasharray={circ}
          initial={{ strokeDashoffset: circ }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1.5, ease: "easeOut", delay: 0.5 }}
          transform="rotate(-90 60 60)"
        />
      </svg>
      <div className="score-content">
        <motion.span 
          className="score-value"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1 }}
        >
          {score}%
        </motion.span>
        <span className="score-text">Match</span>
      </div>
      <div className="ring-glow" style={{ background: color }} />
    </div>
  )
}

function SkillPill({ skill, type }) {
  return (
    <motion.div 
      className={`skill-item ${type}`}
      whileHover={{ scale: 1.05 }}
    >
      {type === 'matched' ? <CheckCircle2 size={13} /> : <XCircle size={13} />}
      <span>{skill}</span>
    </motion.div>
  )
}

export default function ResultsPage({ results, onReset }) {
  const [letter, setLetter] = useState(results.improved_cover_letter || results.cover_letter || '')
  const [showAllMissing, setShowAllMissing] = useState(false)

  const match = results.match_results || {}
  const matched = match.matched_skills || []
  const missing = match.missing_skills || []
  const score = match.match_score || 0

  const visibleMissing = showAllMissing ? missing : missing.slice(0, 8)

  function copyLetter() {
    navigator.clipboard.writeText(letter)
    toast.success('Copied to clipboard!')
  }

  function downloadLetter() {
    const blob = new Blob([letter], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'cover_letter.txt'
    a.click()
    URL.revokeObjectURL(url)
    toast.success('Downloaded!')
  }

  const verdict =
    score >= 70 ? { text: 'High Potential', Icon: Zap, color: 'var(--success)' } :
    score >= 40 ? { text: 'Good Fit',       Icon: TrendingUp, color: 'var(--warning)' } :
                  { text: 'Low Correlation', Icon: AlertCircle, color: 'var(--danger)' }

  return (
    <motion.div 
      className="results-container"
      initial="hidden"
      animate="visible"
      variants={containerVariants}
    >
      <div className="results-bg-glow" />
      
      {/* Top Header */}
      <div className="results-top-bar">
        <motion.div variants={itemVariants} className="results-header-info">
          <div className="results-badge">
            <Sparkles size={12} />
            <span>Analysis Complete</span>
          </div>
          <h1 className="results-title">Application Dashboard</h1>
        </motion.div>
        
        <motion.button 
          variants={itemVariants} 
          className="restart-btn" 
          onClick={onReset}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          <RefreshCw size={14} />
          <span>New Session</span>
        </motion.button>
      </div>

      <div className="dashboard-grid">
        {/* Sidebar / Top Section */}
        <div className="dashboard-sidebar">
          {/* Match Score Card */}
          <motion.div variants={itemVariants} className="glass-card stat-card">
            <div className="stat-header">
              <h3 className="card-lbl">Skill Correlation</h3>
              <div className="verdict-tag" style={{ color: verdict.color, background: `${verdict.color}15` }}>
                <verdict.Icon size={14} />
                <span>{verdict.text}</span>
              </div>
            </div>
            
            <div className="score-display">
              <ScoreRing score={score} />
              <p className="score-insight">
                We found <strong>{matched.length}</strong> core competencies that align with this role requirements.
              </p>
            </div>
          </motion.div>

          {/* Matched Skills */}
          <motion.div variants={itemVariants} className="glass-card skills-card">
            <div className="card-head">
              <CheckCircle2 size={16} className="text-success" />
              <h3>Identified Strengths</h3>
            </div>
            <div className="skills-flex">
              <AnimatePresence>
                {matched.map((s, i) => (
                  <SkillPill key={s} skill={s} type="matched" />
                ))}
              </AnimatePresence>
            </div>
          </motion.div>

          {/* Gap Analysis */}
          {missing.length > 0 && (
            <motion.div variants={itemVariants} className="glass-card skills-card">
              <div className="card-head">
                <AlertCircle size={16} className="text-warning" />
                <h3>Opportunity Gaps</h3>
              </div>
              <div className="skills-flex">
                {visibleMissing.map((s, i) => (
                  <SkillPill key={s} skill={s} type="missing" />
                ))}
              </div>
              {missing.length > 8 && (
                <button className="expand-btn" onClick={() => setShowAllMissing(!showAllMissing)}>
                  {showAllMissing ? <ChevronUp size={14}/> : <ChevronDown size={14}/>}
                  {showAllMissing ? 'Show Less' : `+${missing.length - 8} More`}
                </button>
              )}
            </motion.div>
          )}
        </div>

        {/* Main Content Area: Cover Letter */}
        <div className="dashboard-main">
          <motion.div variants={itemVariants} className="glass-card letter-dashboard-card">
            <div className="letter-card-header">
              <div className="head-left">
                <FileText size={18} className="text-primary" />
                <h3>Drafted Cover Letter</h3>
              </div>
              <div className="head-actions">
                <button className="icon-action-btn" onClick={copyLetter} title="Copy Content">
                  <Copy size={16} />
                </button>
                <button className="primary-action-btn" onClick={downloadLetter}>
                  <Download size={16} />
                  <span>Download PDF</span>
                </button>
              </div>
            </div>
            
            <div className="editor-container">
              <div className="editor-toolbar">
                <div className="dots">
                  <span className="dot" />
                  <span className="dot" />
                  <span className="dot" />
                </div>
                <span className="editor-status">Ready to Review</span>
              </div>
              <textarea
                className="modern-editor"
                value={letter}
                onChange={e => setLetter(e.target.value)}
                spellCheck={false}
              />
            </div>
          </motion.div>
        </div>
      </div>
    </motion.div>
  )
}
