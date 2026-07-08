import { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { sendChatMessage, selectIsLoading } from '../../features/chat/chatSlice';
import { selectFormData, selectInteractionId } from '../../features/interaction/interactionSlice';
import { Send } from 'lucide-react';

function ChatInput() {
  const [input, setInput] = useState('');
  const dispatch = useDispatch();
  const isLoading = useSelector(selectIsLoading);
  const formData = useSelector(selectFormData);
  const interactionId = useSelector(selectInteractionId);

  const handleSend = () => {
    const trimmed = input.trim();
    if (!trimmed || isLoading) return;

    dispatch(sendChatMessage({
      message: trimmed,
      formData,
      interactionId,
    }));
    setInput('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="p-4 border-t border-slate-200 bg-white shrink-0">
      <div className="flex items-end gap-2.5">
        <div className="flex-1 relative">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Describe your interaction with an HCP..."
            rows={1}
            className="w-full px-4 py-3 pr-12 border border-slate-200 rounded-xl text-sm resize-none focus:outline-none focus:ring-2 focus:ring-blue-400/40 focus:border-blue-300 transition-all placeholder:text-slate-300"
            disabled={isLoading}
            style={{ minHeight: '44px', maxHeight: '120px' }}
            onInput={(e) => {
              e.target.style.height = '44px';
              e.target.style.height = Math.min(e.target.scrollHeight, 120) + 'px';
            }}
          />
        </div>
        <button
          onClick={handleSend}
          disabled={!input.trim() || isLoading}
          className="flex items-center justify-center w-11 h-11 bg-gradient-to-r from-blue-500 to-indigo-500 text-white rounded-xl hover:from-blue-600 hover:to-indigo-600 disabled:opacity-30 disabled:cursor-not-allowed transition-all shadow-sm hover:shadow-md active:scale-95"
          title="Send message"
        >
          <Send className="w-4 h-4" />
        </button>
      </div>
      <p className="text-xs text-slate-300 mt-2 text-center">
        Press Enter to send · Shift+Enter for new line
      </p>
    </div>
  );
}

export default ChatInput;
