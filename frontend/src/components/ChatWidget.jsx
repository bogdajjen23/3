import React, { useState, useRef } from 'react';
import VoiceInput from './VoiceInput';
import FileAttachment from './FileAttachment';

export default function ChatWidget() {
  const [messages, setMessages] = useState([]);
  const [text, setText] = useState('');
  const bottomRef = useRef();
  const [threadId, setThreadId] = useState('');

  async function sendMessage(file) {
    const payload = { text, thread_id: threadId };
    const form = new FormData();
    form.append('data', JSON.stringify(payload));
    if (file) form.append('file', file);

    setMessages(prev => [...prev, { role: 'user', content: text }]);
    setText('');

    const res = await fetch(file ? '/files/upload' : '/chat', {
      method: 'POST',
      headers: file ? {} : { 'Content-Type': 'application/json' },
      body: file ? form : JSON.stringify(payload)
    });
    const data = await res.json();
    setThreadId(data.thread_id);
    setMessages(prev => [...prev, { role: 'assistant', content: data.text }]);
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }

  return (
    <div className="w-full max-w-md mx-auto p-4 bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-shadow">
      <div className="h-64 overflow-y-auto mb-4">
        {messages.map((m, i) => (
          <div
            key={i}
            className={`my-2 p-2 rounded-xl ${m.role === 'user' ? 'bg-[#01579B] text-white text-right' : 'bg-white border border-black/13'}`
            }>
            <div>{m.content}</div>
            <div className="text-xs text-gray-500 mt-1">{new Date().toLocaleTimeString()}</div>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>
      <div className="flex space-x-2">
        <VoiceInput onVoice={t => setText(t)} />
        <FileAttachment onFile={f => sendMessage(f)} />
        <textarea
          className="flex-1 p-2 rounded-xl border border-gray-300 resize-none"
          placeholder="введите сообщение"
          rows={2}
          value={text}
          onChange={e => setText(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && !e.shiftKey && (e.preventDefault(), sendMessage())}
        />
        <button onClick={() => sendMessage()} className="p-2 rounded-full hover:bg-gray-100">➤</button>
      </div>
    </div>
  );
}
