import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { motion, AnimatePresence } from 'framer-motion'
import toast from 'react-hot-toast'
import { Upload, FileText, Link2, Building2, AlignLeft, ChevronRight, X, Loader2, Sparkles } from 'lucide-react'
import axios from 'axios'
import './UploadPage.css'

const INPUT_TYPES = [
  { id: 'url',     label: 'Job URL',       icon: Link2,     placeholder: 'https://careers.company.com/job/...' },
  { id: 'company', label: 'Website',       icon: Building2, placeholder: 'https://company.com' },
  { id: 'name',    label: 'Company',       icon: Building2, placeholder: 'e.g. Google, Anthropic' },
  { id: 'text',    label: 'Job Text',      icon: AlignLeft, placeholder: 'Paste the full job description here...', multiline: true },
]

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

export default function UploadPage({ onResults }) {
  const [resumeFile, setResumeFile] = useState(null)
  const [inputType, setInputType] = useState('url')
  const [jobInput, setJobInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [loadingStep, setLoadingStep] = useState('')

  const onDrop = useCallback((accepted) => {
    if (accepted[0]) {
      setResumeFile(accepted[0])
      toast.success(`Résumé loaded: ${accepted[0].name}`)
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'] },
    maxFiles: 1,
    onDropRejected: () => toast.error('Please upload a PDF résumé'),
  })

  async function handleSubmit() {
    if (!resumeFile) return toast.error('Please upload your résumé')
    if (!jobInput.trim()) return toast.error('Please provide job details')

    setLoading(true)
    const steps = [
      'Scanning résumé...',
      'Analyzing job requirements...',
      'Calculating skill match...',
      'Generating cover letter...',
      'Finalizing results...',
    ]
    let i = 0
    setLoadingStep(steps[0])
    const interval = setInterval(() => {
      i = (i + 1) % steps.length
      setLoadingStep(steps[i])
    }, 2500)

    try {
      const formData = new FormData()
      formData.append('resume', resumeFile)
      formData.append('job_input', jobInput.trim())

      const res = await axios.post('https://fahiye-applyai-backend.hf.space/analyze', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 120000,
      })
      onResults(res.data)
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Analysis failed. Please try again.')
    } finally {
      clearInterval(interval)
      setLoading(false)
    }
  }

  const active = INPUT_TYPES.find(t => t.id === inputType)

  return (
    <motion.div 
      className="upload-page"
      initial="hidden"
      animate="visible"
      variants={containerVariants}
    >
      <div className="upload-glow" />
      
      <header className="upload-header">
        <motion.div variants={itemVariants} className="badge">
          <Sparkles size={12} />
          <span>Next-Gen Career Agent</span>
        </motion.div>
        
        <motion.h1 variants={itemVariants} className="hero-title">
          Master the <span className="gradient-text">Application.</span>
        </motion.h1>
        
        <motion.p variants={itemVariants} className="hero-sub">
          Our AI analyzes your skills against any job posting to craft 
          the perfect profile & cover letter instantly.
        </motion.p>
      </header>

      <motion.div variants={itemVariants} className="main-card-container">
        <div className="glass-card upload-card">
          {/* Section 1: Resume */}
          <div className="card-section">
            <h2 className="section-label">
              <span className="step-num">01</span>
              Upload your Résumé
            </h2>
            
            <div
              {...getRootProps()}
              className={`dropzone ${isDragActive ? 'active' : ''} ${resumeFile ? 'filled' : ''}`}
            >
              <input {...getInputProps()} />
              <AnimatePresence mode="wait">
                {resumeFile ? (
                  <motion.div 
                    key="file"
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.95 }}
                    className="file-info"
                  >
                    <div className="file-icon-box">
                      <FileText size={24} />
                    </div>
                    <div className="file-details">
                      <p className="file-name">{resumeFile.name}</p>
                      <p className="file-meta">{(resumeFile.size / 1024).toFixed(0)} KB · PDF</p>
                    </div>
                    <button
                      className="remove-btn"
                      onClick={e => { e.stopPropagation(); setResumeFile(null) }}
                    >
                      <X size={16} />
                    </button>
                  </motion.div>
                ) : (
                  <motion.div 
                    key="hint"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="drop-hint"
                  >
                    <div className="upload-icon-circle">
                      <Upload size={24} />
                    </div>
                    <p className="hint-main">
                      {isDragActive ? 'Drop your file here' : 'Drop your résumé PDF'}
                    </p>
                    <p className="hint-sub">or click to browse local files</p>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </div>

          <div className="divider" />

          {/* Section 2: Job Info */}
          <div className="card-section">
            <h2 className="section-label">
              <span className="step-num">02</span>
              Identify the Role
            </h2>

            <div className="tab-switcher">
              {INPUT_TYPES.map(t => (
                <button
                  key={t.id}
                  className={`tab-btn ${inputType === t.id ? 'active' : ''}`}
                  onClick={() => { setInputType(t.id); setJobInput('') }}
                >
                  <t.icon size={14} />
                  <span>{t.label}</span>
                  {inputType === t.id && (
                    <motion.div layoutId="activeTab" className="active-tab-indicator" />
                  )}
                </button>
              ))}
            </div>

            <div className="input-wrap">
              {active.multiline ? (
                <textarea
                  className="modern-textarea"
                  placeholder={active.placeholder}
                  value={jobInput}
                  onChange={e => setJobInput(e.target.value)}
                  rows={5}
                />
              ) : (
                <div className="modern-input-group">
                  <input
                    className="modern-input"
                    type="text"
                    placeholder={active.placeholder}
                    value={jobInput}
                    onChange={e => setJobInput(e.target.value)}
                    onKeyDown={e => e.key === 'Enter' && handleSubmit()}
                  />
                  <div className="input-glow" />
                </div>
              )}
            </div>
          </div>

          {/* Action Footer */}
          <div className="card-footer">
            <motion.button 
              className="magic-btn" 
              onClick={handleSubmit} 
              disabled={loading}
              whileHover={{ scale: 1.01 }}
              whileTap={{ scale: 0.99 }}
            >
              <div className="btn-glow" />
              {loading ? (
                <div className="loading-state">
                  <Loader2 size={18} className="spinner" />
                  <span>{loadingStep}</span>
                </div>
              ) : (
                <div className="btn-content">
                  <span>Generate AI Analysis</span>
                  <ChevronRight size={18} />
                </div>
              )}
            </motion.button>
            
            {loading && (
              <div className="loading-bar-outer">
                <motion.div 
                  className="loading-bar-inner"
                  initial={{ width: "0%" }}
                  animate={{ width: "100%" }}
                  transition={{ duration: 15, ease: "linear" }}
                />
              </div>
            )}
          </div>
        </div>
      </motion.div>
    </motion.div>
  )
}