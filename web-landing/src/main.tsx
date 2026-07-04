import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'

// Note: StrictMode is intentionally omitted. Its dev-only double-mount
// interrupts Framer Motion entrance animations, leaving them stuck mid-reveal.
// This does not affect production behavior.
createRoot(document.getElementById('root')!).render(<App />)
