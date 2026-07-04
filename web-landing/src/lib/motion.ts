import type { Variants } from 'framer-motion'

export const APP_URL = 'https://jiopulse.streamlit.app'

// Fade + rise, used for scroll-reveal blocks
export const rise: Variants = {
  hidden: { opacity: 0, y: 28 },
  show: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease: [0.22, 1, 0.36, 1] },
  },
}

// Container that staggers its children on reveal
export const stagger: Variants = {
  hidden: {},
  show: { transition: { staggerChildren: 0.09 } },
}

// Shared viewport config so sections reveal once, a bit before fully on-screen
export const inView = { once: true, amount: 0.3 } as const
