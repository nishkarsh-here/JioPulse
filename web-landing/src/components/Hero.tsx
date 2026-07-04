import { motion } from 'framer-motion'
import { APP_URL, rise, stagger } from '../lib/motion'

export default function Hero() {
  return (
    <section
      id="top"
      className="relative flex min-h-screen items-center justify-center overflow-hidden px-6 pt-28"
    >
      {/* animated glow blobs */}
      <motion.div
        aria-hidden
        className="pointer-events-none absolute -top-40 left-1/2 h-[42rem] w-[42rem] -translate-x-1/2 rounded-full blur-[120px]"
        style={{ background: 'radial-gradient(circle, rgba(229,9,127,0.35), transparent 60%)' }}
        animate={{ scale: [1, 1.15, 1], opacity: [0.7, 1, 0.7] }}
        transition={{ duration: 8, repeat: Infinity, ease: 'easeInOut' }}
      />
      <motion.div
        aria-hidden
        className="pointer-events-none absolute bottom-[-10rem] right-[-6rem] h-[34rem] w-[34rem] rounded-full blur-[120px]"
        style={{ background: 'radial-gradient(circle, rgba(200,16,46,0.4), transparent 60%)' }}
        animate={{ scale: [1.1, 1, 1.1], opacity: [0.6, 0.9, 0.6] }}
        transition={{ duration: 10, repeat: Infinity, ease: 'easeInOut' }}
      />

      <motion.div
        variants={stagger}
        initial="hidden"
        animate="show"
        className="relative z-10 mx-auto max-w-4xl text-center"
      >
        <motion.div
          variants={rise}
          className="mx-auto mb-6 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-1.5 text-sm text-cream/80"
        >
          <span className="h-2 w-2 animate-pulse rounded-full bg-pink" />
          AI attendance, reimagined
        </motion.div>

        <motion.h1
          variants={rise}
          className="font-display text-5xl leading-[0.95] tracking-tight sm:text-7xl md:text-8xl"
        >
          Snap the room.
          <br />
          <span className="text-gradient">It's marked.</span>
        </motion.h1>

        <motion.p
          variants={rise}
          className="mx-auto mt-7 max-w-2xl text-lg text-cream/70 sm:text-xl"
        >
          JioPulse takes attendance in seconds with computer vision, voice biometrics, and QR —
          then an agentic AI assistant answers questions and does the follow-up for you.
        </motion.p>

        <motion.div variants={rise} className="mt-10 flex flex-wrap items-center justify-center gap-4">
          <a
            href={APP_URL}
            target="_blank"
            rel="noreferrer"
            className="group rounded-full bg-brand px-7 py-3.5 font-semibold text-white shadow-lg shadow-brand/30 transition-transform hover:scale-105"
          >
            Try the live demo
            <span className="ml-2 inline-block transition-transform group-hover:translate-x-1">→</span>
          </a>
          <a
            href="#how"
            className="rounded-full border border-white/15 px-7 py-3.5 font-semibold text-cream transition-colors hover:bg-white/5"
          >
            See how it works
          </a>
        </motion.div>

        <motion.p variants={rise} className="mt-6 text-sm text-cream/45">
          Face · Voice · QR — no hardware, just a photo.
        </motion.p>
      </motion.div>
    </section>
  )
}
