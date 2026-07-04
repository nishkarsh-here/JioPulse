import { motion } from 'framer-motion'
import { APP_URL } from '../lib/motion'

const LINKS = [
  { label: 'Features', href: '#features' },
  { label: 'How it works', href: '#how' },
  { label: 'AI', href: '#ai' },
]

export default function Nav() {
  return (
    <motion.header
      initial={{ y: -80, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
      className="fixed inset-x-0 top-0 z-50 flex justify-center px-4 pt-4"
    >
      <nav className="flex w-full max-w-5xl items-center justify-between rounded-full border border-white/10 bg-ink-soft/70 px-4 py-2.5 backdrop-blur-xl">
        <a href="#top" className="flex items-center gap-2">
          <img
            src="https://i.ibb.co/YTYGn5qV/logo.png"
            alt="JioPulse"
            className="h-8 w-8 rounded-lg"
          />
          <span className="font-display text-lg tracking-tight text-cream">JioPulse</span>
        </a>

        <div className="hidden items-center gap-8 md:flex">
          {LINKS.map((l) => (
            <a
              key={l.href}
              href={l.href}
              className="text-sm text-cream/70 transition-colors hover:text-cream"
            >
              {l.label}
            </a>
          ))}
        </div>

        <a
          href={APP_URL}
          target="_blank"
          rel="noreferrer"
          className="rounded-full bg-brand px-4 py-2 text-sm font-semibold text-white transition-transform hover:scale-105"
        >
          Launch App
        </a>
      </nav>
    </motion.header>
  )
}
