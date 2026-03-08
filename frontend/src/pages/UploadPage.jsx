import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import toast from 'react-hot-toast'
import { Upload, FileText, Link2, Building2, AlignLeft, ChevronRight, X, Loader2 } from 'lucide-react'
import axios from 'axios'
import './UploadPage.css'

const INPUT_TYPES = [
  { id: 'url',     label: 'Job Posting URL',       icon: Link2,     placeholder: 'https://careers.company.com/job/...' },
  { id: 'company', label: 'Company Website',        icon: Building2, placeholder: 'https://company.com' },
  { id: 'name',    label: 'Company Name',           icon: Building2, placeholder: 'e.g. Google, Anthropic, Safaricom' },
  { id: 'text',    label: 'Paste Job Description',  icon: AlignLeft, placeholder: 'Paste the full job description here...', multiline: true },
]

export default function UploadPage({ onResults }) {
  const [resumeFile, setResumeFile] = useState(null)
  const [inputType, setInputType] = useState('url')
  const [jobInput, setJobInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [loadingStep, setLoadingStep] = useState('')

  const onDrop = useCallback((accepted) => {
    if (accepted[0]) {
      setResumeFile(accepted[0])
      toast.success(`Loaded: ${accepted[0].name}`)
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'] },
    maxFiles: 1,
    onDropRejected: () => toast.error('Please upload a PDF file'),
  })

  async function handleSubmit() {
    if (!resumeFile) return toast.error('Please upload your resume')
    if (!jobInput.trim()) return toast.error('Please enter job details')

    setLoading(true)
    const steps = [
      'Parsing your resume…',
      'Researching the role…',
      'Matching your skills…',
      'Crafting your cover letter…',
      'Polishing final draft…',
    ]
    let i = 0
    setLoadingStep(steps[0])
    const interval = setInterval(() => {
      i = (i + 1) % steps.length
      setLoadingStep(steps[i])
    }, 2800)

    try {
      const formData = new FormData()
      formData.append('resume', resumeFile)
      formData.append('job_input', jobInput.trim())

      const res = await axios.post('/api/analyze', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 120000,
      })
      onResults(res.data)
    } catch (err) {
      const msg = err.response?.data?.detail || 'Something went wrong. Please try again.'
      toast.error(msg)
    } finally {
      clearInterval(interval)
      setLoading(false)
      setLoadingStep('')
    }
  }

  const active = INPUT_TYPES.find(t => t.id === inputType)

  return (
    <div className="upload-page">
      <div className="upload-hero">
        <p className="upload-eyebrow">AI-powered job applications</p>
        <h1 className="upload-headline">
          Your next role,<br />
          <em>perfectly framed.</em>
        </h1>
        <p className="upload-subline">
          Upload your CV, point us to a job — we'll match your skills and
          write a tailored cover letter in seconds.
        </p>
      </div>

      <div className="upload-card">

        {/* Step 1 */}
        <div className="upload-section">
          <div className="upload-step-label">
            <span className="upload-step-num">1</span>
            Upload your résumé
          </div>

          <div
            {...getRootProps()}
            className={`dropzone ${isDragActive ? 'dropzone-active' : ''} ${resumeFile ? 'dropzone-filled' : ''}`}
          >
            <input {...getInputProps()} />
            {resumeFile ? (
              <div className="file-info">
                <FileText size={22} className="file-icon" />
                <div>
                  <p className="file-name">{resumeFile.name}</p>
                  <p className="file-size">{(resumeFile.size / 1024).toFixed(0)} KB · PDF</p>
                </div>
                <button
                  className="file-remove"
                  onClick={e => { e.stopPropagation(); setResumeFile(null) }}
                >
                  <X size={15} />
                </button>
              </div>
            ) : (
              <div className="drop-hint">
                <div className="drop-icon"><Upload size={22} /></div>
                <p className="drop-text">{isDragActive ? 'Drop it here' : 'Drag & drop your PDF résumé'}</p>
                <p className="drop-sub">or <span className="drop-browse">click to browse</span></p>
              </div>
            )}
          </div>
        </div>

        <div className="upload-divider" />

        {/* Step 2 */}
        <div className="upload-section">
          <div className="upload-step-label">
            <span className="upload-step-num">2</span>
            Tell us about the role
          </div>

          <div className="type-grid">
            {INPUT_TYPES.map(t => (
              <button
                key={t.id}
                className={`type-btn ${inputType === t.id ? 'type-btn-active' : ''}`}
                onClick={() => { setInputType(t.id); setJobInput('') }}
              >
                <t.icon size={14} />
                {t.label}
              </button>
            ))}
          </div>

          {active.multiline ? (
            <textarea
              className="job-textarea"
              placeholder={active.placeholder}
              value={jobInput}
              onChange={e => setJobInput(e.target.value)}
              rows={6}
            />
          ) : (
            <input
              className="job-input"
              type="text"
              placeholder={active.placeholder}
              value={jobInput}
              onChange={e => setJobInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && handleSubmit()}
            />
          )}
        </div>

        {/* Submit */}
        <button className="submit-btn" onClick={handleSubmit} disabled={loading}>
          {loading ? (
            <><Loader2 size={17} className="submit-spinner" />{loadingStep}</>
          ) : (
            <>Generate cover letter<ChevronRight size={17} /></>
          )}
        </button>

        {loading && (
          <div className="progress-bar">
            <div className="progress-fill" />
          </div>
        )}
      </div>
    </div>
  )
}
