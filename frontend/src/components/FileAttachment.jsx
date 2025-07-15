import React from 'react';

export default function FileAttachment({ onFile }) {
  function handleDrop(e) {
    e.preventDefault();
    onFile(e.dataTransfer.files[0]);
  }
  return (
    <div
      onDragOver={(e) => e.preventDefault()}
      onDrop={handleDrop}
      className="p-2 rounded-xl border border-gray-300 cursor-pointer"
    >
      📎
      <input type="file" hidden onChange={(e) => onFile(e.target.files[0])} />
    </div>
  );
}
