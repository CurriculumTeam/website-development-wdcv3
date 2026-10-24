// ════════════════════════════════════════════════════════════════════════════
// constants.js
// ════════════════════════════════════════════════════════════════════════════

// ─────────────────────────── LESSON 2 START ──────────────────────────────
// Managing Data with Props, State, and User Input
// Goal   : Define the age modes used by AppContext and the preference form.
// Output : The app knows which age group the user selected.

// Age modes — controls which movies the AI is allowed to recommend
export const AGE = {
  KIDS:  'kids',   // Under 13
  TEEN:  'teen',   // 13–17
  ADULT: 'adult',  // 18+
};

// Conversation stages — used by AppContext to track onboarding progress
export const STAGE = {
  NAME:       'name',
  GREET_MOOD: 'greet_mood',
  AGE:        'age',
  CATEGORIES: 'categories',
  MOVIE_MOOD: 'movie_mood',
  LANGUAGE:   'language',
  CHAT:       'chat',
};

// ─────────────────────────── LESSON 2 END ────────────────────────────────
