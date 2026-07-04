import { useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import { inView, rise } from '../lib/motion'

type Step = { n: string; title: string; body: string }

const FLOWS: Record<'student' | 'teacher', Step[]> = {
  student: [
    { n: '01', title: 'Join a class', body: 'Scan the QR or enter the join code your teacher shares.' },
    { n: '02', title: 'Enroll your biometrics', body: 'Register your FaceID (and optional VoiceID) once, with consent.' },
    { n: '03', title: 'Get marked automatically', body: 'Show up — a single class photo or a quick phrase marks you present.' },
    { n: '04', title: 'Track & ask', body: 'See your attendance %, and ask the AI what you missed or if you’re at risk.' },
  ],
  teacher: [
    { n: '01', title: 'Create a subject', body: 'Spin up a class with a code and section in seconds.' },
    { n: '02', title: 'Share the QR / link', body: 'Students self-enroll — no manual roster entry.' },
    { n: '03', title: 'Run attendance', body: 'Snap the room, record a phrase, or scan QR. The AI builds the roster.' },
    { n: '04', title: 'Review & follow up', body: 'Confirm results, view analytics, and let the agent draft the follow-ups.' },
  ],
}

export default function HowItWorks() {
  const [role, setRole] = useState<'student' | 'teacher'>('teacher')
  const steps = FLOWS[role]

  return (
    <section id="how" className="relative mx-auto max-w-6xl px-6 py-28">
      <motion.div
        variants={rise}
        initial="hidden"
        whileInView="show"
        viewport={inView}
        className="mb-10 text-center"
      >
        <p className="mb-3 font-semibold uppercase tracking-[0.2em] text-pink">The flow</p>
        <h2 className="font-display text-4xl tracking-tight sm:text-5xl">How JioPulse works</h2>
      </motion.div>

      {/* role toggle */}
      <div className="mb-12 flex justify-center">
        <div className="relative flex rounded-full border border-white/10 bg-white/[0.03] p-1">
          {(['teacher', 'student'] as const).map((r) => (
            <button
              key={r}
              onClick={() => setRole(r)}
              className="relative z-10 rounded-full px-6 py-2 text-sm font-semibold capitalize transition-colors"
              style={{ color: role === r ? '#fff' : 'rgba(253,243,244,0.6)' }}
            >
              {role === r && (
                <motion.span
                  layoutId="rolePill"
                  className="absolute inset-0 -z-10 rounded-full bg-brand"
                  transition={{ type: 'spring', stiffness: 400, damping: 32 }}
                />
              )}
              I'm a {r}
            </button>
          ))}
        </div>
      </div>

      {/* steps as a connected flow */}
      <AnimatePresence mode="wait">
        <motion.ol
          key={role}
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -16 }}
          transition={{ duration: 0.4 }}
          className="grid gap-5 md:grid-cols-4"
        >
          {steps.map((s, i) => (
            <motion.li
              key={s.n}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1, duration: 0.5 }}
              className="relative rounded-3xl border border-white/10 bg-white/[0.03] p-6"
            >
              <span className="font-display text-3xl text-gradient">{s.n}</span>
              <h3 className="mt-3 text-lg font-semibold text-cream">{s.title}</h3>
              <p className="mt-2 text-sm text-cream/60">{s.body}</p>
              {i < steps.length - 1 && (
                <span className="absolute -right-3 top-1/2 hidden -translate-y-1/2 text-pink md:block">
                  →
                </span>
              )}
            </motion.li>
          ))}
        </motion.ol>
      </AnimatePresence>
    </section>
  )
}
