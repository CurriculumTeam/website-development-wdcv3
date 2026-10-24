// ════════════════════════════════════════════════════════════════════════════
// AppContext.jsx — Global shared state
// ════════════════════════════════════════════════════════════════════════════

// ─────────────────────────── LESSON 2 (from previous lesson) ─────────────
import { createContext, useContext, useState, useCallback, useRef, useEffect } from 'react';
import { STAGE, AGE } from '../constants';

const AppContext = createContext(null);

export function AppProvider({ children }) {

  const [theme, setTheme] = useState(() => localStorage.getItem('cv_theme') || 'dark');
  useEffect(() => {
    document.body.className = theme === 'light' ? 'light-mode' : '';
    localStorage.setItem('cv_theme', theme);
  }, [theme]);

  const [userName,       setUserName]       = useState('');
  const [userAge,        setUserAge]        = useState(AGE.ADULT);
  const [userMood,       setUserMood]       = useState('');
  const [userCategories, setUserCategories] = useState([]);
  const [userLanguage,   setUserLanguage]   = useState(['Any Language']);

  const userAgeRef = useRef(AGE.ADULT);
  useEffect(() => { userAgeRef.current = userAge; }, [userAge]);

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
// ─────────────────────────────────────────────────────────────────────────


// ─────────────────────────── LESSON 3 START ──────────────────────────────
// Handling Events and Rendering Dynamic Movie Content
// Goal   : Add callAI stub so the chat flow runs without a real API key.
// Output : The full 6-step onboarding chat works with placeholder replies.
//
// NOTE: callAI here returns a hardcoded reply — real AI is wired in Lesson 5.

  // callAI stub — returns a scripted reply so the chat flow works now.
  // Replace this entire function in Lesson 5 with the real Groq API call.
  const callAI = useCallback(async (userMessage) => {
    // Simulate a short network delay so the typing dots appear
    await new Promise(r => setTimeout(r, 600));
    if (userMessage.toLowerCase().includes('name'))
      return "Great to meet you! How are you feeling today?";
    if (userMessage.toLowerCase().includes('feeling') || userMessage.toLowerCase().includes('mood'))
      return "Sounds good! Let's find the perfect movie for you.";
    return "Here are some great movies I think you'll enjoy!";
  }, []);

  // callAIWithSearch stub — returns a reply with no movie results yet.
  // Movie posters are added in Lesson 4 when OMDb is connected.
  const callAIWithSearch = useCallback(async (userMessage) => {
    const reply = await callAI(userMessage);
    return { reply, movieResults: [], hasAgeSwitchOffer: false };
  }, [callAI]);

  // searchForStrip stub — returns empty array until Lesson 4 (OMDb API).
  const searchForStrip = useCallback(async () => [], []);

  // switchAge — change age mode mid-chat
  const switchAge = useCallback((newAge) => {
    setUserAge(newAge);
    userAgeRef.current = newAge;
    addMsg('bot', `Switched to ${{ [AGE.KIDS]: 'Kids mode', [AGE.TEEN]: 'Teen mode', [AGE.ADULT]: 'Adult mode' }[newAge]}!`);
  }, [addMsg]);

  // isRestricted stub — always returns false until Lesson 5 adds the filter
  const isRestricted = useCallback(() => false, []);

// ─────────────────────────── LESSON 3 END ────────────────────────────────


  const value = {
    // Lesson 2
    theme, setTheme,
    userName, setUserName, userAge, setUserAge,
    userMood, setUserMood, userCategories, setUserCategories,
    userLanguage, setUserLanguage,
    stage, setStage, chatMsgs, setChatMsgs, addMsg,
    isBotTyping, setIsBotTyping, resetChat,
    // Lesson 3
    callAI, callAIWithSearch, searchForStrip, switchAge, isRestricted,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

export function useApp() {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error('useApp must be inside <AppProvider>');
  return ctx;
}
