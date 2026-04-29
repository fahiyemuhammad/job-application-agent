import { useState } from 'react'
import { Toaster } from 'react-hot-toast'
import Navbar from './components/Navbar.jsx'
import UploadPage from './pages/UploadPage.jsx'
import ResultsPage from './pages/ResultsPage.jsx'

export default function App() {
  const [page, setPage] = useState('upload')
  const [results, setResults] = useState(null)

  function handleResults(data) {
    setResults(data)
    setPage('results')
  }

  function handleReset() {
    setResults(null)
    setPage('upload')
  }
 

  return (
    <>
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            fontFamily: 'var(--font-body)',
            fontSize: '14px',
            background: 'var(--bg-card)',
            color: 'var(--text-primary)',
            border: '1px solid var(--border-glass)',
            boxShadow: '0 10px 30px rgba(0, 0, 0, 0.08)',
            backdropFilter: 'blur(12px)',
            borderRadius: '12px',
            padding: '12px 20px',
          }
        }}
      />
      <Navbar onReset={handleReset} showBack={page === 'results'} />
      <main>
        {page === 'upload' && <UploadPage onResults={handleResults} />}
        {page === 'results' && <ResultsPage results={results} onReset={handleReset} />}
      </main>
    </>
  )
}
