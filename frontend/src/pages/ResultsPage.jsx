import { useState } from 'react'
import toast from 'react-hot-toast'
import {
  CheckCircle2, XCircle, Download, Copy, RefreshCw,
  TrendingUp, AlertCircle, Sparkles, ChevronDown, ChevronUp
} from 'lucide-react'
import './ResultsPage.css'

function ScoreRing({ score }) {
  const radius = 44
  const circ = 2 * Math.PI * radius
  const offset = circ - (score / 100) * circ
  const color =
    score >= 70 ? 'var(--success)' :
    score >= 40 ? 'var(--warning)' :
    'var(--danger)'

  return (
    <div className="score-ring">
      <svg width="110" height="110" viewBox="0 0 110 110">
        <circle cx="55" cy="55" r={radius} fill="none" stroke="var(--border)" strokeWidth="8" />
        <circle
          cx="55" cy="55" r={radius} fill="none"
          stroke={color} strokeWidth="8"
          strokeLinecap="round"
          strokeDasharray={circ}
          strokeDashoffset={offset}
          transform="rotate(-90 55 55)"
          style={{ transition: 'stroke-dashoffset 1.2s ease' }}
        />
      </svg>
      <div className="score-inner">
        <span className="score-num" style={{ color }}>{score}%</span>
        <span className="score-label">match</span>
      </div>
    </div>
  )
}

function SkillPill({ skill, type }) {
  return (
    <span className={`skill-pill ${type === 'matched' ? 'pill-green' : 'pill-red'}`}>
      {type === 'matched' ? <CheckCircle2 size={11} /> : <XCircle size={11} />}
      {skill}
    </span>
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
    score >= 70 ? { text: 'Strong match',   Icon: TrendingUp,   cls: 'verdict-green'  } :
    score >= 40 ? { text: 'Moderate match', Icon: AlertCircle,  cls: 'verdict-yellow' } :
                  { text: 'Low match',      Icon: XCircle,      cls: 'verdict-red'    }

  return (
    <div className="results-page">

      {/* Header */}
      <div className="results-header">
        <div className="results-header-left">
          <span className="results-eyebrow"><Sparkles size={13} /> Results ready</span>
          <h1 className="results-title">Your application package</h1>
          <p className="results-subtitle">Review your skill match and personalised cover letter below.</p>
        </div>
        <button className="results-reset-btn" onClick={onReset}>
          <RefreshCw size={14} /> Start over
        </button>
      </div>

      {/* Grid */}
      <div className="results-grid">

        {/* Left column */}
        <div className="results-left-col">

          {/* Score card */}
          <div className="results-card">
            <h2 className="card-title">Skill match score</h2>
            <div className="score-row">
              <ScoreRing score={score} />
              <div>
                <span className={`verdict ${verdict.cls}`}>
                  <verdict.Icon size={14} />
                  {verdict.text}
                </span>
                <p className="score-desc">
                  {matched.length} of {matched.length + missing.length} required skills found in your résumé.
                </p>
              </div>
            </div>
          </div>

          {/* Matched skills */}
          {matched.length > 0 && (
            <div className="results-card">
              <h2 className="card-title">
                <CheckCircle2 size={15} color="var(--success)" /> Matched skills
              </h2>
              <div className="pill-wrap">
                {matched.map(s => <SkillPill key={s} skill={s} type="matched" />)}
              </div>
            </div>
          )}

          {/* Missing skills */}
          {missing.length > 0 && (
            <div className="results-card">
              <h2 className="card-title">
                <XCircle size={15} color="var(--danger)" /> Skills to develop
              </h2>
              <div className="pill-wrap">
                {visibleMissing.map(s => <SkillPill key={s} skill={s} type="missing" />)}
              </div>
              {missing.length > 8 && (
                <button className="show-more-btn" onClick={() => setShowAllMissing(v => !v)}>
                  {showAllMissing
                    ? <><ChevronUp size={13} /> Show less</>
                    : <><ChevronDown size={13} /> Show {missing.length - 8} more</>}
                </button>
              )}
            </div>
          )}
        </div>

        {/* Cover letter */}
        <div className="results-card letter-card">
          <div className="letter-header">
            <h2 className="card-title"><Sparkles size={15} /> Cover letter</h2>
            <div className="letter-actions">
              <button className="action-btn" onClick={copyLetter}>
                <Copy size={14} /> Copy
              </button>
              <button className="action-btn action-btn-primary" onClick={downloadLetter}>
                <Download size={14} /> Download
              </button>
            </div>
          </div>
          <p className="letter-hint">You can edit the letter directly below.</p>
          <textarea
            className="letter-editor"
            value={letter}
            onChange={e => setLetter(e.target.value)}
            spellCheck
          />
        </div>

      </div>
    </div>
  )
}
