// ════════════════════════════════════════════════════════════════════════════
// Navbar.jsx — Top navigation bar
// ════════════════════════════════════════════════════════════════════════════

// ─────────────────────────── LESSON 1 (from previous lesson) ─────────────
// This was the Lesson 1 static Navbar — no state, no context:
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


// ─────────────────────────── LESSON 2 START ──────────────────────────────
// Managing Data with Props, State, and User Input
// Goal   : Connect Navbar to AppContext to get theme toggle and reset.
// Output : Clicking the logo resets the form; moon/sun toggles dark mode.

import { useApp } from '../context/AppContext';

export default function Navbar() {
  const { theme, setTheme, resetChat } = useApp();
  const isLight = theme === 'light';

  return (
    <nav className="app-navbar">
      <div className="navbar-inner">

        {/* Clicking the brand resets the whole form */}
        <button className="navbar-brand" onClick={resetChat} title="Start over">
          <i className="bi bi-film" />
          AI Powered CineVerse
        </button>

        <div className="navbar-right">
          <span className="nav-badge">
            <i className="bi bi-stars" style={{ marginRight: 5 }} />
            AI Powered
          </span>

          {/* Dark / light mode toggle — reads theme from context, writes via setTheme */}
          <button
            className="btn-icon"
            title={isLight ? 'Switch to dark mode' : 'Switch to light mode'}
            onClick={() => setTheme(isLight ? 'dark' : 'light')}
          >
            <i className={`bi ${isLight ? 'bi-sun-fill' : 'bi-moon-stars-fill'}`} />
          </button>
        </div>

      </div>
    </nav>
  );
}

// ─────────────────────────── LESSON 2 END ────────────────────────────────
