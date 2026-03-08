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
          style: {
            fontFamily: 'var(--font-body)',
            fontSize: '14px',
            background: 'var(--surface)',
            color: 'var(--text-primary)',
            border: '1px solid var(--border)',
            boxShadow: 'var(--shadow-md)',
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
