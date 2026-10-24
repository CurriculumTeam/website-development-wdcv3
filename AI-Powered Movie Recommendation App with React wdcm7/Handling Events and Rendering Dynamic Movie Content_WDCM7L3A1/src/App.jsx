// ════════════════════════════════════════════════════════════════════════════
// App.jsx — Root component
// ════════════════════════════════════════════════════════════════════════════

// ─────────────────────────── LESSON 2 (from previous lesson) ─────────────
// Lesson 2 rendered: <Navbar /> + <UserPreferenceForm />
// Lesson 3 replaces UserPreferenceForm with the full ChatPage.
// ─────────────────────────────────────────────────────────────────────────

// ─────────────────────────── LESSON 3 START ──────────────────────────────
// Handling Events and Rendering Dynamic Movie Content
// Goal   : Replace the preference form with the full interactive chat.
// Output : The complete 6-step onboarding chat flow is visible and works.

import { AppProvider, useApp } from './context/AppContext';
import Navbar from './components/Navbar';
import ChatPage from './components/HeroSection';

function AppInner() {
  return (
    <div className="app-root">
      <Navbar />    {/* Lesson 2 — theme toggle + reset */}
      <ChatPage />  {/* Lesson 3 — full onboarding chat */}
    </div>
  );
}

export default function App() {
  return (
    <AppProvider>
      <AppInner />
    </AppProvider>
  );
}

// ─────────────────────────── LESSON 3 END ────────────────────────────────
