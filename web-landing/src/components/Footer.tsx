import { motion } from 'framer-motion'
import { APP_URL, inView, rise } from '../lib/motion'

export default function Footer() {
  return (
    <footer className="relative overflow-hidden px-6 py-24">
      <motion.div
        variants={rise}
        initial="hidden"
        whileInView="show"
        viewport={inView}
        className="relative z-10 mx-auto max-w-3xl rounded-[2.5rem] border border-white/10 bg-gradient-to-br from-brand/20 to-pink/10 p-12 text-center"
      >
        <h2 className="font-display text-4xl tracking-tight sm:text-5xl">
          Ready to skip the roll-call?
        </h2>
        <p className="mx-auto mt-4 max-w-xl text-cream/70">
          Open the live app and take your first AI attendance in under a minute.
        </p>
        <a
          href={APP_URL}
          target="_blank"
          rel="noreferrer"
          className="mt-8 inline-block rounded-full bg-brand px-8 py-4 font-semibold text-white shadow-lg shadow-brand/30 transition-transform hover:scale-105"
        >
          Launch JioPulse →
        </a>
      </motion.div>

      <div className="relative z-10 mx-auto mt-16 flex max-w-5xl flex-col items-center justify-between gap-4 border-t border-white/5 pt-8 text-sm text-cream/50 sm:flex-row">
        <div className="flex items-center gap-2">
          <img src="https://i.ibb.co/YTYGn5qV/logo.png" alt="" className="h-6 w-6 rounded-md" />
          <span className="font-display text-cream/80">JioPulse</span>
        </div>
        <p>Built with ❤️ for educators everywhere</p>
      </div>
    </footer>
  )
}
