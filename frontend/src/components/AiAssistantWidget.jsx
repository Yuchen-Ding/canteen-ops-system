import { useEffect, useRef, useState } from 'react';
import { Bot, GripHorizontal, Minus, Send, X } from 'lucide-react';

import { getLatestAiSession, sendAiChatMessage } from '../services/api.js';

export function AiAssistantWidget() {
  const [position, setPosition] = useState({ x: 24, y: 120 });
  const [open, setOpen] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const dragRef = useRef(null);
  const suppressClickRef = useRef(false);
  const messageEndRef = useRef(null);

  useEffect(() => {
    setPosition({ x: Math.max(20, window.innerWidth - 82), y: Math.max(80, window.innerHeight - 90) });
    getLatestAiSession()
      .then((data) => {
        setSessionId(data.session.id);
        setMessages(data.messages || []);
      })
      .catch((err) => setError(err.message || 'AI 会话加载失败'));
  }, []);

  useEffect(() => {
    messageEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, open]);

  const startDrag = (event) => {
    dragRef.current = {
      startX: event.clientX,
      startY: event.clientY,
      originX: position.x,
      originY: position.y,
      moved: false,
    };

    const move = (moveEvent) => {
      if (!dragRef.current) return;
      const dx = moveEvent.clientX - dragRef.current.startX;
      const dy = moveEvent.clientY - dragRef.current.startY;
      if (Math.abs(dx) + Math.abs(dy) > 4) dragRef.current.moved = true;
      setPosition({
        x: Math.min(window.innerWidth - 58, Math.max(12, dragRef.current.originX + dx)),
        y: Math.min(window.innerHeight - 58, Math.max(70, dragRef.current.originY + dy)),
      });
    };
    const stop = () => {
      suppressClickRef.current = Boolean(dragRef.current?.moved);
      dragRef.current = null;
      window.removeEventListener('pointermove', move);
      window.removeEventListener('pointerup', stop);
      window.setTimeout(() => { suppressClickRef.current = false; }, 50);
    };
    window.addEventListener('pointermove', move);
    window.addEventListener('pointerup', stop);
  };

  const toggleOpen = () => {
    if (!suppressClickRef.current) setOpen((value) => !value);
  };

  const submit = async (event) => {
    event.preventDefault();
    const content = input.trim();
    if (!content || loading) return;
    setInput('');
    setError('');
    setLoading(true);
    setMessages((current) => [...current, { id: `local-${Date.now()}`, role: 'USER', content }]);
    try {
      const result = await sendAiChatMessage(sessionId, content);
      setSessionId(result.session_id);
      setMessages(result.messages || []);
    } catch (err) {
      setError(err.message || 'AI 回复失败');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <button
        className="ai-float-button"
        style={{ left: position.x, top: position.y }}
        title="AI 运营助手"
        type="button"
        onClick={toggleOpen}
        onPointerDown={startDrag}
      >
        <Bot size={24} />
      </button>

      {open ? (
        <section className="ai-chat-panel">
          <header className="ai-chat-header">
            <div><Bot size={18} /><strong>AI 运营助手</strong></div>
            <div>
              <GripHorizontal size={17} />
              <button title="最小化" type="button" onClick={() => setOpen(false)}><Minus size={17} /></button>
              <button title="关闭" type="button" onClick={() => setOpen(false)}><X size={17} /></button>
            </div>
          </header>
          <div className="ai-chat-messages">
            {messages.length === 0 ? (
              <p className="ai-empty">可以询问今日收入、退款、热门档口或年度运营情况。</p>
            ) : null}
            {messages.map((message) => (
              <div className={`ai-message ${message.role === 'USER' ? 'user' : 'assistant'}`} key={message.id}>
                <span>{message.role === 'USER' ? '你' : '助手'}</span>
                <p>{message.content}</p>
              </div>
            ))}
            {loading ? <div className="ai-loading">正在分析运营数据...</div> : null}
            <div ref={messageEndRef} />
          </div>
          {error ? <div className="ai-error">{error}</div> : null}
          <form className="ai-chat-form" onSubmit={submit}>
            <textarea
              placeholder="例如：今天哪个档口收入最高？"
              rows="2"
              value={input}
              onChange={(event) => setInput(event.target.value)}
            />
            <button disabled={loading || !input.trim()} title="发送" type="submit"><Send size={18} /></button>
          </form>
        </section>
      ) : null}
    </>
  );
}
