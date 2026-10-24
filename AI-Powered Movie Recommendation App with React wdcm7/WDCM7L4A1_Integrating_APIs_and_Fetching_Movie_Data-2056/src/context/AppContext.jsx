// ════════════════════════════════════════════════════════════════════════════
// AppContext.jsx — Global shared state
// ════════════════════════════════════════════════════════════════════════════

import { createContext, useContext, useState, useCallback, useRef, useEffect } from 'react';
import { STAGE, AGE } from '../constants';

// ─────────────────────────── LESSON 4 START ──────────────────────────────
// Integrating APIs and Fetching Movie Data
// Goal   : Connect OMDb API so search and movie detail modal work.
// Output : Search icon fetches real movies; clicking a card shows details.
import { omdbSearch, omdbDetails } from '../utils/api';
// ─────────────────────────── LESSON 4 END ────────────────────────────────


const AppContext = createContext(null);

export function AppProvider({ children }) {

  // ── Theme (Lesson 2) ────────────────────────────────────────────────────
  const [theme, setTheme] = useState(() => localStorage.getItem('cv_theme') || 'dark');
  useEffect(() => {
    document.body.className = theme === 'light' ? 'light-mode' : '';
    localStorage.setItem('cv_theme', theme);
  }, [theme]);

  // ── User profile (Lesson 2) ─────────────────────────────────────────────
  const [userName,       setUserName]       = useState('');
  const [userAge,        setUserAge]        = useState(AGE.ADULT);
  const [userMood,       setUserMood]       = useState('');
  const [userCategories, setUserCategories] = useState([]);
  const [userLanguage,   setUserLanguage]   = useState(['Any Language']);

  const userAgeRef = useRef(AGE.ADULT);
  useEffect(() => { userAgeRef.current = userAge; }, [userAge]);

  // ── Chat state (Lesson 2) ───────────────────────────────────────────────
  const [stage,       setStage]       = useState(STAGE.NAME);
  const [chatMsgs,    setChatMsgs]    = useState([]);
  const [isBotTyping, setIsBotTyping] = useState(false);

  const msgCounter = useRef(0);
  const newId = () => `msg-${++msgCounter.current}`;

  const addMsg = useCallback((role, content) =>
    setChatMsgs(prev => [...prev, { id: newId(), role, content }]), []);

  const resetModalRef = useRef(null);
  const resetChat = useCallback(() => {
    setChatMsgs([]);
    setUserName(''); setUserAge(AGE.ADULT); userAgeRef.current = AGE.ADULT;
    setUserMood(''); setUserCategories([]); setUserLanguage(['Any Language']);
    setIsBotTyping(false); setStage(STAGE.NAME);
    if (resetModalRef.current) resetModalRef.current();
  }, []);

  // ── callAI stub (Lesson 3) — scripted replies, no movie recommendations ─
  // Real Groq AI is wired in Lesson 5.
  const callAI = useCallback(async (userMessage) => {
    await new Promise(r => setTimeout(r, 500));
    if (userMessage.toLowerCase().includes('name'))
      return "Great to meet you! How are you feeling today?";
    if (userMessage.toLowerCase().includes('feeling') || userMessage.toLowerCase().includes('mood'))
      return "Sounds good! Let's set up your preferences.";
    return "Got it!";
  }, []);

  // ── switchAge (Lesson 3) ────────────────────────────────────────────────
  const switchAge = useCallback((newAge) => {
    setUserAge(newAge);
    userAgeRef.current = newAge;
    addMsg('bot', `Switched to ${{ [AGE.KIDS]: '🔥 Trending mode', [AGE.TEEN]: '🎞️ Nostalgic mode', [AGE.ADULT]: '⭐ Popular mode' }[newAge]}!`);
  }, [addMsg]);


  // ─────────────────────────── LESSON 4 START ──────────────────────────────
  // Integrating APIs and Fetching Movie Data
  // Goal   : Add omdbSearch + openMovie so the search modal and detail popup work.

  // searchForStrip — search OMDb and return up to 12 results
  const searchForStrip = useCallback(async (query) => {
    if (!query.trim()) return [];
    try { return (await omdbSearch(query)).slice(0, 12); }
    catch { return []; }
  }, []);

  // openMovie — fetch full details then open MovieModal
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [showModal,     setShowModal]     = useState(false);

  resetModalRef.current = () => setShowModal(false);

  const openMovie = useCallback((movie) => {
    setSelectedMovie(movie);
    setShowModal(true);
    if (movie?.imdbID) {
      omdbDetails(movie.imdbID)
        .then(full => { if (full) setSelectedMovie(full); })
        .catch(() => {});
    }
  }, []);

  // ─────────────────────────── LESSON 4 END ────────────────────────────────


  const value = {
    theme, setTheme,
    userName, setUserName, userAge, setUserAge,
    userMood, setUserMood, userCategories, setUserCategories,
    userLanguage, setUserLanguage,
    stage, setStage, chatMsgs, setChatMsgs, addMsg,
    isBotTyping, setIsBotTyping, resetChat,
    callAI, switchAge,
    // Lesson 4
    searchForStrip,
    selectedMovie, showModal, setShowModal, openMovie,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

export function useApp() {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error('useApp must be inside <AppProvider>');
  return ctx;
}
