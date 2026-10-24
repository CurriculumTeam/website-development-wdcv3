// ════════════════════════════════════════════════════════════════════════════
// Navbar.jsx — Top navigation bar
// ════════════════════════════════════════════════════════════════════════════

// ─────────────────────────── LESSON 2 + 3 (from previous lessons) ────────
// Lesson 1 static version:
//
//   export default function Navbar() {
//     return (
//       <nav className="app-navbar">
//         <div className="navbar-inner">
//           <span className="navbar-brand">🎬 AI Powered CineVerse</span>
//           <span className="nav-badge">AI Powered</span>
//         </div>
//       </nav>
//     );
//   }
// ─────────────────────────────────────────────────────────────────────────

// ─────────────────────────── LESSON 4 (unchanged from Lesson 2) ──────────
// No changes to Navbar in Lesson 4 — search icon lives in HeroSection header.

import { useApp } from '../context/AppContext';

export default function Navbar() {
  const { theme, setTheme, resetChat } = useApp();
  const isLight = theme === 'light';
  return (
    <nav className="app-navbar">
      <div className="navbar-inner">
        <button className="navbar-brand" onClick={resetChat} title="Start over">
          <i className="bi bi-film" />
          AI Powered CineVerse
        </button>
        <div className="navbar-right">
          <span className="nav-badge">
            <i className="bi bi-stars" style={{ marginRight: 5 }} />
            AI Powered
          </span>
          <button className="btn-icon"
            title={isLight ? 'Dark mode' : 'Light mode'}
            onClick={() => setTheme(isLight ? 'dark' : 'light')}>
            <i className={`bi ${isLight ? 'bi-sun-fill' : 'bi-moon-stars-fill'}`} />
          </button>
        </div>
      </div>
    </nav>
  );
}
