// ════════════════════════════════════════════════════════════════════════════
// api.js — All external API calls in one place
// ════════════════════════════════════════════════════════════════════════════

import { OMDB_API_KEY } from '../config';

// ─────────────────────────── LESSON 4 START ──────────────────────────────
// Integrating APIs and Fetching Movie Data
// Goal   : Use fetch() to call the OMDb API and get real movie data.
// Output : Movie posters and titles appear in the chat after onboarding.

// Safe ratings only — encoded as Base64. Anything not in this list is blocked.
// G=Rw==  TV-G=VFYtRw==  TV-PG=VFYtUEc=  TV-14=VFYtMTQ=
const _sr = ['Rw==','VFYtRw==','VFYtUEc=','VFYtMTQ='].map(atob);
const _isSafe = r => !!r && _sr.some(s => r.toUpperCase() === s.toUpperCase());

// omdbSearch — search OMDb, fetch details for each result, filter out 18+ content.
export async function omdbSearch(query) {
  if (!OMDB_API_KEY) { console.warn('[OMDb] No API key — add VITE_OMDB_API_KEY to .env'); return []; }

  const original = query.trim();
  const cleaned = original
    .replace(/\.(?=[A-Za-z])/g, '')
    .replace(/[:.]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();

  const terms = [...new Set([original, cleaned])];

  const fetchTerm = term =>
    fetch(`https://www.omdbapi.com/?apikey=${OMDB_API_KEY}&s=${encodeURIComponent(term)}&type=movie`)
      .then(r => r.json())
      .then(d => d.Response === 'True' ? d.Search : [])
      .catch(() => []);

  const seen = new Set(), merged = [];
  for (const arr of await Promise.all(terms.map(fetchTerm)))
    for (const m of arr)
      if (!seen.has(m.imdbID)) { seen.add(m.imdbID); merged.push(m); }

  // Fetch ratings for each result and filter out 18+ content
  const withRatings = await Promise.all(
    merged.map(m =>
      fetch(`https://www.omdbapi.com/?apikey=${OMDB_API_KEY}&i=${m.imdbID}`)
        .then(r => r.json())
        .then(d => {
          console.log(`[OMDb] ${m.Title} (${m.imdbID}): Rated="${d.Rated}"`);
          return { ...m, Rated: d.Rated || '' };
        })
        .catch(() => m)
    )
  );

  const filtered = withRatings.filter(m => _isSafe(m.Rated));
  console.log(`[OMDb] Search "${query}": ${merged.length} total, ${filtered.length} after filter`);
  return filtered;
}

// omdbDetails — fetch full details; returns null if content is 18+.
export async function omdbDetails(imdbID) {
  if (!OMDB_API_KEY || !imdbID) return null;
  try {
    const d = await fetch(
      `https://www.omdbapi.com/?apikey=${OMDB_API_KEY}&i=${imdbID}&plot=full`
    ).then(r => r.json());
    if (d.Response !== 'True') return null;
    if (!_isSafe(d.Rated)) return null;
    return d;
  } catch { return null; }
}

// ─────────────────────────── LESSON 4 END ────────────────────────────────
