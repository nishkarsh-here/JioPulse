import { motion } from 'framer-motion'
import { APP_URL, inView, rise, stagger } from '../lib/motion'

const CHAT = [
  { from: 'user', text: 'Which students are below 75% in CS101?' },
  { from: 'ai', text: '3 students are below 75%: Ayan (68%), Mihika (72%), Anoushka (74%). Want me to draft a nudge email?' },
  { from: 'user', text: 'Yes, draft it.' },
  { from: 'ai', text: 'Drafted a friendly reminder to all 3 with their current %. Review and approve to send. ✅' },
]

export default function AISection() {
  return (
    <section id="ai" className="relative mx-auto max-w-6xl px-6 py-28">
      <div className="grid items-center gap-14 lg:grid-cols-2">
        <motion.div variants={rise} initial="hidden" whileInView="show" viewport={inView}>
          <p className="mb-3 font-semibold uppercase tracking-[0.2em] text-pink">Agentic AI</p>
          <h2 className="font-display text-4xl leading-tight tracking-tight sm:text-5xl">
            An assistant that doesn't just answer — it acts
          </h2>
          <p className="mt-6 text-lg text-cream/70">
            Built on retrieval-augmented generation and a tool-using agent loop. It reads your live
            attendance data, grounds every number in the source, and can take actions — draft
            emails, flag at-risk students, prep reports — always with your approval.
          </p>
          <ul className="mt-8 space-y-3">
            {[
              'Grounded in live data — never invents figures',
              'Retrieval + tool-calling agent, fully transparent',
              'Students only ever see their own records',
            ].map((t) => (
              <li key={t} className="flex items-start gap-3 text-cream/80">
                <span className="mt-1 text-pink">✓</span>
                {t}
              </li>
            ))}
          </ul>
          <a
            href={APP_URL}
            target="_blank"
            rel="noreferrer"
            className="mt-9 inline-block rounded-full bg-brand px-7 py-3.5 font-semibold text-white transition-transform hover:scale-105"
          >
            Ask JioPulse AI →
          </a>
        </motion.div>

        {/* animated chat mock */}
        <motion.div
          variants={stagger}
          initial="hidden"
          whileInView="show"
          viewport={inView}
          className="rounded-3xl border border-white/10 bg-ink-soft/80 p-5 shadow-2xl backdrop-blur"
        >
          <div className="mb-4 flex items-center gap-2 border-b border-white/5 pb-3">
            <span className="h-3 w-3 rounded-full bg-brand" />
            <span className="h-3 w-3 rounded-full bg-pink" />
            <span className="text-sm text-cream/50">JioPulse AI Assistant</span>
          </div>
          <div className="space-y-3">
            {CHAT.map((m, i) => (
              <motion.div
                key={i}
                variants={rise}
                className={m.from === 'user' ? 'flex justify-end' : 'flex justify-start'}
              >
                <div
                  className={
                    'max-w-[80%] rounded-2xl px-4 py-2.5 text-sm ' +
                    (m.from === 'user'
                      ? 'bg-brand text-white'
                      : 'bg-white/[0.06] text-cream/90')
                  }
                >
                  {m.text}
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  )
}
