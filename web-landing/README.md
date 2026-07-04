# JioPulse — Landing page (web-landing)

The new marketing/landing site for JioPulse, rebuilt from scratch as a modern animated single-page
site. Replaces the old Flask landing in `../landing/`.

## Stack
- **Vite** + **React 19** + **TypeScript**
- **Tailwind CSS v4** (via `@tailwindcss/vite`)
- **Framer Motion** for entrance + scroll-reveal + interactive motion

## Develop
```bash
npm install
npm run dev      # http://localhost:5273 (see ../.claude/launch.json)
```

## Build
```bash
npm run build    # type-checks + outputs static site to dist/
npm run preview  # preview the production build
```

## Deploy (Vercel — free)
Point a Vercel project at this folder (`web-landing/`). Vite is auto-detected:
- Build command: `npm run build`
- Output directory: `dist`

The "Launch App" / demo CTAs point at the live Streamlit app, configured in
`src/lib/motion.ts` (`APP_URL`).

## Structure
```
src/
  components/   Nav, Hero, Features, HowItWorks, AISection, Footer
  lib/motion.ts shared animation variants + APP_URL
  index.css     Tailwind + design tokens (brand colors, fonts)
```
