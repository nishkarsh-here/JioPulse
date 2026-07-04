import { motion } from 'framer-motion'
import { inView, rise, stagger } from '../lib/motion'

const FEATURES = [
  {
    icon: '📸',
    title: 'Face attendance',
    body: 'One classroom photo recognizes every enrolled student from facial embeddings — the whole room, in one shot.',
  },
  {
    icon: '🎙️',
    title: 'Voice attendance',
    body: 'Students say a short phrase; voice biometrics match them against stored signatures. Perfect when cameras are shy.',
  },
  {
    icon: '📱',
    title: 'QR enrolment',
    body: 'Every class gets a unique join code and QR — students enroll in seconds, no forms, no friction.',
  },
  {
    icon: '✨',
    title: 'Agentic AI assistant',
    body: 'Ask “who is below 75% in CS101?” and get answers grounded in live data — or let it draft the nudge email.',
  },
  {
    icon: '📊',
    title: 'Live analytics',
    body: 'Attendance trends, per-student rollups, and at-risk detection surfaced as clean, interactive dashboards.',
  },
  {
    icon: '🔐',
    title: 'Cloud backend',
    body: 'Supabase-backed rosters and attendance logs, with a dark/light themed, responsive interface.',
  },
]

export default function Features() {
  return (
    <section id="features" className="relative mx-auto max-w-6xl px-6 py-28">
      <motion.div
        variants={rise}
        initial="hidden"
        whileInView="show"
        viewport={inView}
        className="mb-14 text-center"
      >
        <p className="mb-3 font-semibold uppercase tracking-[0.2em] text-pink">Everything in one place</p>
        <h2 className="font-display text-4xl tracking-tight sm:text-5xl">
          Attendance, minus the roll-call
        </h2>
      </motion.div>

      <motion.div
        variants={stagger}
        initial="hidden"
        whileInView="show"
        viewport={inView}
        className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3"
      >
        {FEATURES.map((f) => (
          <motion.div
            key={f.title}
            variants={rise}
            whileHover={{ y: -6 }}
            className="group rounded-3xl border border-white/10 bg-white/[0.03] p-7 transition-colors hover:border-pink/40"
          >
            <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-pink/20 to-brand/20 text-2xl">
              {f.icon}
            </div>
            <h3 className="mb-2 text-xl font-semibold text-cream">{f.title}</h3>
            <p className="text-cream/60">{f.body}</p>
          </motion.div>
        ))}
      </motion.div>
    </section>
  )
}
