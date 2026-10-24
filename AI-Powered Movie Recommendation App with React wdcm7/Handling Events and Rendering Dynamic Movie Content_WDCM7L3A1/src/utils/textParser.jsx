// ─────────────────────────── LESSON 3 START ──────────────────────────────
// Handling Events and Rendering Dynamic Movie Content
// Goal   : Safely render AI text and turn **bold titles** into buttons.
// Output : Movie titles in chat are clickable chips.

import React from 'react';

/**
 * Convert AI reply text into safe React elements.
 * **Movie Title** → clickable <button> chip
 */
export function parseAIText(text, onMovieClick) {
  if (!text || typeof text !== 'string') return null;

  const parts = text.split(/(\*\*[^*\n]{1,80}?\*\*)/g);

  return parts.map((part, i) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      const title = part.slice(2, -2).trim();
      if (onMovieClick && title.length > 1) {
        return (
          <button key={i} className="movie-title-chip"
            onClick={() => onMovieClick(title)} title={`Tap to search for "${title}"`}>
            🎬 {title}
          </button>
        );
      }
      return <strong key={i}>{title}</strong>;
    }
    const lines = part.split('\n');
    return lines.map((line, j) => (
      <React.Fragment key={`${i}-${j}`}>
        {line}
        {j < lines.length - 1 && <br />}
      </React.Fragment>
    ));
  });
}

/**
 * Extract all **bold** movie titles from an AI reply.
 */
export function extractTitles(text) {
  if (!text) return [];
  const titles = [];
  const re = /\*\*([^*\n]{2,60}?)\*\*/g;
  let m;
  while ((m = re.exec(text)) !== null) {
    const t = m[1].trim();
    if (t && !titles.includes(t)) titles.push(t);
  }
  return titles.slice(0, 6);
}

// ─────────────────────────── LESSON 3 END ────────────────────────────────
