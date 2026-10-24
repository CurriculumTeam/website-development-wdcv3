// ════════════════════════════════════════════════════════════════════════════
// HeroSection.jsx — Main chat interface (ChatPage)
// ════════════════════════════════════════════════════════════════════════════

// ─────────────────────────── LESSON 3 START ──────────────────────────────
// Handling Events and Rendering Dynamic Movie Content
// Goal   : Build the full onboarding chat flow with buttons and input.
// Output : Users complete all 6 setup steps and reach free chat.

import { useState, useEffect, useRef } from 'react';
import { useApp } from '../context/AppContext';
import { parseAIText } from '../utils/textParser';
import { STAGE, AGE, CATEGORIES_BY_AGE, MOODS_BY_AGE, LANGUAGES } from '../constants';

// ─────────────────────────── LESSON 4 START ──────────────────────────────
// Integrating APIs and Fetching Movie Data
// Goal   : Add a search icon that opens a movie search overlay.
// Output : 🔍 icon opens SearchModal; clicking a result shows MovieModal.
import SearchModal from './SearchModal';
// ─────────────────────────── LESSON 4 END ────────────────────────────────

function TypingDots() {
  return (
    <div className="chat-row bot-row">
      <div className="bot-avatar"><i className="bi bi-stars" /></div>
      <div className="bubble bot-bubble">
        <div className="typing-dots"><span /><span /><span /></div>
      </div>
    </div>
  );
}

function SpecialContent({ content }) {
  const { addMsg, switchAge } = useApp();
  const [cats,  setCats]  = useState([]);
  const [langs, setLangs] = useState(['Any Language']);
  const { type } = content;

  if (type === 'mood-greeting') return (
    <div className="choice-row">
      {[['Great day!','Having a great day!'],['Meh day','Just a meh day'],['Rescue me!','I need a movie to rescue me!']]
        .map(([label, val]) => (
          <button key={val} className="choice-btn" onClick={() => content.onSelect(val)}>{label}</button>
        ))}
      {content.enableTyping && <button className="choice-btn type-btn" onClick={content.enableTyping}>Type</button>}
    </div>
  );

  if (type === 'age-picker') return (
    <div className="choice-row">
      {[[AGE.KIDS,'Kids','Under 13'],[AGE.TEEN,'Teen','13-17'],[AGE.ADULT,'Adult','18+']]
        .map(([age, label, sub]) => (
          <button key={age} className="choice-btn" onClick={() => content.onSelect(age)}>
            {label} <span className="choice-sub">{sub}</span>
          </button>
        ))}
    </div>
  );

  if (type === 'category-picker') {
    const items = CATEGORIES_BY_AGE[content.age] || CATEGORIES_BY_AGE.adult;
    return (
      <div>
        <div className="category-grid">
          {items.map(c => (
            <button key={c.id}
              className={`category-btn ${cats.includes(c.id) ? 'selected' : ''}`}
              onClick={() => setCats(p => p.includes(c.id) ? p.filter(x => x !== c.id) : [...p, c.id])}>
              {c.label}
            </button>
          ))}
        </div>
        <button className="confirm-btn" disabled={!cats.length} onClick={() => content.onConfirm(cats)}>
          Let's find your movies!
        </button>
      </div>
    );
  }

  if (type === 'mood-picker') {
    const moods = content.age === AGE.KIDS ? MOODS_BY_AGE.kids : MOODS_BY_AGE.other;
    return (
      <div className="choice-row">
        {moods.map(m => (
          <button key={m.value} className="choice-btn" onClick={() => content.onSelect(m.value)}>{m.label}</button>
        ))}
        {content.enableTyping && <button className="choice-btn type-btn" onClick={content.enableTyping}>Type</button>}
      </div>
    );
  }

  if (type === 'language-picker') {
    const toggle = lang => {
      if (lang === 'Any Language') { setLangs(['Any Language']); return; }
      setLangs(prev => {
        const without = prev.filter(l => l !== 'Any Language');
        const next = prev.includes(lang) ? without.filter(l => l !== lang) : [...without, lang];
        return next.length ? next : ['Any Language'];
      });
    };
    return (
      <div>
        <div className="category-grid">
          {LANGUAGES.map(lang => (
            <button key={lang}
              className={`category-btn ${langs.includes(lang) ? 'selected' : ''}`}
              onClick={() => toggle(lang)}>
              {lang}
            </button>
          ))}
        </div>
        <button className="confirm-btn" disabled={!langs.length} onClick={() => content.onConfirm(langs)}>
          Let's go!
        </button>
      </div>
    );
  }

  if (type === 'age-switch-offer') return (
    <div className="choice-row">
      <button className="choice-btn" onClick={() => switchAge(AGE.TEEN)}>Switch to Teen</button>
      <button className="choice-btn" onClick={() => switchAge(AGE.ADULT)}>Switch to Adult</button>
      <button className="choice-btn" onClick={() => addMsg('user', 'Keep Kids mode')}>Stay Kids</button>
    </div>
  );

  return null;
}

function ChatRow({ msg, onMovieClick }) {
  const isBot = msg.role === 'bot';
  const { content } = msg;
  if (content?.type) return (
    <div className="chat-row bot-row">
      <div className="bot-avatar"><i className="bi bi-stars" /></div>
      <div className="bubble bot-bubble interactive-bubble"><SpecialContent content={content} /></div>
    </div>
  );
  return (
    <div className={`chat-row ${isBot ? 'bot-row' : 'user-row'}`}>
      {isBot && <div className="bot-avatar"><i className="bi bi-stars" /></div>}
      <div className={`bubble ${isBot ? 'bot-bubble' : 'user-bubble'}`}>
        {typeof content === 'string' ? parseAIText(content, onMovieClick) : content}
      </div>
    </div>
  );
}

export default function ChatPage() {
  const {
    stage, setStage, chatMsgs, addMsg, isBotTyping, setIsBotTyping,
    userName, setUserName, userAge, setUserAge, userMood, setUserMood,
    userCategories, setUserCategories, setUserLanguage,
    callAI, switchAge,
  } = useApp();

  const [inputVal,    setInputVal]    = useState('');
  const [inputActive, setInputActive] = useState(false);
  const [placeholder, setPlaceholder] = useState('Type your name to begin...');

  // ─────────────────────────── LESSON 4 START ──────────────────────────────
  const [showSearch, setShowSearch] = useState(false);
  // ─────────────────────────── LESSON 4 END ────────────────────────────────

  const msgsEndRef  = useRef(null);
  const welcomeSent = useRef(false);

  useEffect(() => { msgsEndRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [chatMsgs, isBotTyping]);

  useEffect(() => {
    if (stage !== STAGE.NAME || chatMsgs.length > 0) return;
    welcomeSent.current = false;
    const t = setTimeout(() => {
      if (welcomeSent.current) return;
      welcomeSent.current = true;
      setInputActive(false); setInputVal('');
      setPlaceholder('Type your name to begin...');
      addMsg('bot', "Welcome to CineVerse! I'm CineBot, your personal AI movie companion. What should I call you?");
      setInputActive(true);
    }, 400);
    return () => clearTimeout(t);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [stage, chatMsgs.length]);

  async function handleNameSubmit(name) {
    const first = name.trim().split(' ')[0];
    setUserName(first); setInputActive(false); addMsg('user', name.trim());
    setStage(STAGE.GREET_MOOD); setIsBotTyping(true);
    try {
      addMsg('bot', await callAI(`The user's name is ${first}. Greet them warmly in 1 sentence, then ask how they're feeling today.`));
    } catch { addMsg('bot', `Nice to meet you, ${first}! How are you feeling today?`); }
    finally { setIsBotTyping(false); }
    addMsg('bot', {
      type: 'mood-greeting', onSelect: handleGreetingMood,
      enableTyping: () => { setInputActive(true); setPlaceholder('Tell me how you feel...'); },
    });
  }

  async function handleGreetingMood(mood) {
    addMsg('user', mood); setInputActive(false); setStage(STAGE.AGE); setIsBotTyping(true);
    try { addMsg('bot', await callAI(`${userName} said: "${mood}". Respond with 1 warm sentence, then ask for their age group.`)); }
    catch { addMsg('bot', 'Got it! How old are you?'); }
    finally { setIsBotTyping(false); }
    addMsg('bot', { type: 'age-picker', onSelect: handleAgeSelect });
  }

  function handleAgeSelect(age) {
    setUserAge(age);
    addMsg('user', { kids: 'Kids (Under 13)', teen: 'Teen (13-17)', adult: 'Adult (18+)' }[age]);
    setStage(STAGE.CATEGORIES);
    addMsg('bot', 'Great! Pick the genres you love');
    addMsg('bot', { type: 'category-picker', age, onConfirm: handleCategoriesConfirm });
  }

  function handleCategoriesConfirm(cats) {
    const allCats = Object.values(CATEGORIES_BY_AGE).flat();
    addMsg('user', `I love: ${cats.map(c => allCats.find(x => x.id === c)?.label || c).join(', ')}`);
    setUserCategories(cats); setStage(STAGE.MOVIE_MOOD);
    addMsg('bot', "Fantastic taste! What's your vibe right now?");
    addMsg('bot', {
      type: 'mood-picker', age: userAge, onSelect: handleMoodSelect,
      enableTyping: () => { setInputActive(true); setPlaceholder('What mood are you in?'); },
    });
  }

  function handleMoodSelect(mood) {
    setUserMood(mood); addMsg('user', mood); setStage(STAGE.LANGUAGE);
    addMsg('bot', 'Love it! Last thing — what language do you prefer?');
    addMsg('bot', { type: 'language-picker', onConfirm: handleLanguageConfirm });
  }

  function handleLanguageConfirm(langs) {
    setUserLanguage(langs);
    addMsg('user', langs.includes('Any Language') ? 'Any language' : langs.join(', '));
    setStage(STAGE.CHAT); setPlaceholder(`Ask me anything, ${userName || 'friend'}...`);
    setInputActive(true);
    addMsg('bot', `You're all set, ${userName || 'friend'}! 🎬 Use the 🔍 search icon to find any movie.`);
  }

  function handleSend() {
    const msg = inputVal.trim();
    if (!msg || isBotTyping) return;
    setInputVal('');
    if (stage === STAGE.NAME)       { handleNameSubmit(msg); return; }
    if (stage === STAGE.GREET_MOOD) { setInputActive(false); addMsg('user', msg); handleGreetingMood(msg); return; }
    if (stage !== STAGE.CHAT)       return;
    addMsg('user', msg);
    addMsg('bot', 'Use the 🔍 search icon in the header to find movies by title!');
  }

  return (
    <div className="chat-page">

      <div className="chat-header-bar">
        <div className="d-flex align-items-center gap-3">
          <div className="chat-bot-avatar"><i className="bi bi-stars" /></div>
          <div>
            <div className="chat-bot-name">CineBot</div>
            <div className="ai-status"><span className="ai-status-dot" />Your AI Movie Guide</div>
          </div>
        </div>
        <div className="d-flex align-items-center gap-2">
          {stage === STAGE.CHAT && (
            <div className="age-mode-bar">
              {[[AGE.KIDS,'🔥','Trending'],[AGE.TEEN,'🎞️','Nostalgic'],[AGE.ADULT,'⭐','Popular']].map(([key, emoji, label]) => (
                <button key={key}
                  className={`age-mode-btn ${userAge === key ? `active active-${key}` : ''}`}
                  onClick={() => switchAge(key)}>
                  <span className="age-emoji">{emoji}</span>
                  <span className="age-label">{label}</span>
                </button>
              ))}
            </div>
          )}
          {/* ─────────────────────────── LESSON 4 START ──────────────── */}
          <button className="search-icon-btn" onClick={() => setShowSearch(true)}
            aria-label="Search movies" title="Search movies">
            <i className="bi bi-search" />
          </button>
          {/* ─────────────────────────── LESSON 4 END ────────────────── */}
          <span className="live-pill"><span className="live-dot" />Live AI</span>
        </div>
      </div>

      <div className="chat-messages-area">
        {chatMsgs.map(msg => <ChatRow key={msg.id} msg={msg} onMovieClick={null} />)}
        {isBotTyping && <TypingDots />}
        <div ref={msgsEndRef} />
      </div>

      <div className="chat-input-bar">
        <input type="text" className="chat-text-input"
          placeholder={placeholder} value={inputVal}
          disabled={!inputActive || isBotTyping}
          onChange={e => setInputVal(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleSend()}
          autoComplete="off" />
        <button className="send-btn" onClick={handleSend}
          disabled={!inputActive || isBotTyping || !inputVal.trim()}
          aria-label="Send">
          <i className="bi bi-send-fill" />
        </button>
      </div>

      {/* ─────────────────────────── LESSON 4 START ──────────────────── */}
      {showSearch && <SearchModal onClose={() => setShowSearch(false)} />}
      {/* ─────────────────────────── LESSON 4 END ────────────────────── */}

    </div>
  );
}

// ─────────────────────────── LESSON 3 END ────────────────────────────────
