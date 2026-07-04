import Nav from './components/Nav'
import Hero from './components/Hero'
import Features from './components/Features'
import HowItWorks from './components/HowItWorks'
import AISection from './components/AISection'
import Footer from './components/Footer'

export default function App() {
  return (
    <div className="min-h-screen bg-ink text-cream">
      <Nav />
      <main>
        <Hero />
        <Features />
        <HowItWorks />
        <AISection />
      </main>
      <Footer />
    </div>
  )
}
