'use client';
import { useState } from 'react';

export default function Home() {
  const [messages, setMessages] = useState([{ role: 'assistant', content: 'Hey! I\'m your UAE mortgage buddy. Tell me about your situation.' }]);
  const [input, setInput] = useState('');

  const sendMessage = async () => {
    if (!input) return;
    const newMessages = [...messages, { role: 'user', content: input }];
    setMessages(newMessages);
    setInput('');
    const res = await fetch('/api/chat/stream', {  // Proxy or update to backend URL
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages: newMessages })
    });
    const reader = res.body.getReader();
    let assistantMsg = '';
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      const text = new TextDecoder().decode(value);
      const lines = text.split('\n');
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6);
          if (data.includes('result')) {
            const result = JSON.parse(data).result;
            if (result.schedule) {
              assistantMsg += `\nAmortization: Total Interest ${result.total_interest} AED\nFirst 6 months:\n`;
              result.schedule.slice(0, 6).forEach((m) => assistantMsg += `Month ${m.month}: Payment ${m.payment}, Principal ${m.principal}\n`);
            } else {
              assistantMsg += `\n${JSON.stringify(result, null, 2)}`;
            }
          } else {
            assistantMsg += data;
          }
          setMessages([...newMessages, { role: 'assistant', content: assistantMsg }]);
        }
      }
    }
  };

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '20px' }}>
      <h1>UAE Mortgage Friend</h1>
      <div style={{ height: '400px', overflowY: 'scroll', marginBottom: '20px' }}>
        {messages.map((msg, i) => (
          <div key={i} style={{ textAlign: msg.role === 'user' ? 'right' : 'left', marginBottom: '10px' }}>
            <div style={{ display: 'inline-block', padding: '10px', borderRadius: '10px', background: msg.role === 'user' ? '#007bff' : '#f1f1f1', color: msg.role === 'user' ? 'white' : 'black' }}>
              {msg.content}
            </div>
          </div>
        ))}
      </div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
        style={{ width: '100%', padding: '10px', borderRadius: '5px', border: '1px solid #ccc' }}
        placeholder="Ask about buying vs renting..."
      />
    </div>
  );
}