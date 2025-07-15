import React, { useState, useEffect } from 'react';

export default function VoiceInput({ onVoice }) {
  const [recognizing, setRecognizing] = useState(false);
  const [rec, setRec] = useState(null);

  useEffect(() => {
    if (!('webkitSpeechRecognition' in window)) return;
    const r = new window.webkitSpeechRecognition();
    r.continuous = false;
    r.interimResults = false;
    r.lang = 'ru-RU';
    r.onstart = () => setRecognizing(true);
    r.onend = () => setRecognizing(false);
    r.onresult = (e) => onVoice(e.results[0][0].transcript);
    setRec(r);
  }, []);

  return (
    <button
      onMouseDown={() => rec && rec.start()}
      onMouseUp={() => rec && rec.stop()}
      className={`p-2 rounded-full ${recognizing ? 'animate-pulse' : ''}`}
    >
      🎤
    </button>
  );
}
