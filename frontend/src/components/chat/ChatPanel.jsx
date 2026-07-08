import { useRef, useEffect } from 'react';
import { useSelector } from 'react-redux';
import { selectMessages, selectIsLoading } from '../../features/chat/chatSlice';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import { Bot, Zap } from 'lucide-react';

function ChatPanel() {
  const messages = useSelector(selectMessages);
  const isLoading = useSelector(selectIsLoading);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="p-4 border-b border-slate-200 bg-white shrink-0">
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shadow-sm">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <div className="absolute -bottom-0.5 -right-0.5 w-3.5 h-3.5 bg-emerald-400 rounded-full border-2 border-white pulse-glow"></div>
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <h2 className="text-sm font-bold text-slate-900">AI Assistant</h2>
              <Zap className="w-3.5 h-3.5 text-amber-400" />
            </div>
            <p className="text-xs text-slate-400">Powered by Groq · gemma2-9b-it</p>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {messages.map((msg) => (
          <ChatMessage key={msg.id} message={msg} />
        ))}

        {/* Typing indicator */}
        {isLoading && (
          <div className="flex items-start gap-2.5 animate-fade-in-up">
            <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shrink-0 mt-0.5">
              <Bot className="w-3.5 h-3.5 text-white" />
            </div>
            <div className="bg-white border border-slate-100 rounded-xl rounded-bl-sm px-4 py-3 shadow-sm">
              <div className="flex items-center gap-1.5">
                <div className="w-2 h-2 bg-blue-400 rounded-full dot-bounce-1"></div>
                <div className="w-2 h-2 bg-blue-400 rounded-full dot-bounce-2"></div>
                <div className="w-2 h-2 bg-blue-400 rounded-full dot-bounce-3"></div>
                <span className="text-xs text-slate-400 ml-2">Analyzing...</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <ChatInput />
    </div>
  );
}

export default ChatPanel;
