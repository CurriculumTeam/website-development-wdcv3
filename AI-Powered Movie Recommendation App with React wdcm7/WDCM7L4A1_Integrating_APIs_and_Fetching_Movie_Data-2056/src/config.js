// ════════════════════════════════════════════════════════════════════════════
// config.js — API keys and model settings
// ════════════════════════════════════════════════════════════════════════════

// ─────────────────────────── LESSON 4 START ──────────────────────────────
// Integrating APIs and Fetching Movie Data
// Goal   : Store API keys safely in a .env file and read them here.
// Output : The app can connect to OMDb to fetch real movie data.
//
// HOW TO SET UP YOUR .env FILE:
//   1. Open the .env file in this folder
//   2. Replace the placeholder values with your real keys:
//        VITE_OMDB_API_KEY=your_omdb_key_here
//        VITE_GROQ_API_KEY=your_groq_key_here
//   Get a free OMDb key at: https://www.omdbapi.com/apikey.aspx

// OMDb API key — used to search and fetch movie data
export const OMDB_API_KEY = import.meta.env.VITE_OMDB_API_KEY || '';

// Groq API key — used in Lesson 5 for AI chat (not needed yet)
export const GROQ_API_KEY = import.meta.env.VITE_GROQ_API_KEY || '';

// AI models — used in Lesson 5
export const GROQ_MODELS = [
  'llama-3.1-8b-instant',
  'llama-3.3-70b-versatile',
  'gemma2-9b-it',
];

// ─────────────────────────── LESSON 4 END ────────────────────────────────
