// ════════════════════════════════════════════════════════════════════════════
// App.jsx — Root component
// ════════════════════════════════════════════════════════════════════════════

import { AppProvider, useApp } from './context/AppContext';
import Navbar from './components/Navbar';
import ChatPage from './components/HeroSection';

// ─────────────────────────── LESSON 4 START ──────────────────────────────
// Integrating APIs and Fetching Movie Data
// Goal   : Add MovieModal so clicking a search result opens the detail view.
// Output : Search icon → search overlay → click poster → full detail popup.
import MovieModal from './components/MovieModal';
// ─────────────────────────── LESSON 4 END ────────────────────────────────


function AppInner() {
  const { showModal } = useApp();
  return (
    <div className="app-root">
      <Navbar />
      <ChatPage />

      {/* ─────────────────────────── LESSON 4 START ──────────────────── */}
      {showModal && <MovieModal />}
      {/* ─────────────────────────── LESSON 4 END ────────────────────── */}
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
