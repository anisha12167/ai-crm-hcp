import { Bot, Wrench } from 'lucide-react';

function ChatMessage({ message }) {
  const isUser = message.role === 'user';

  const toolLabels = {
    log_interaction: '📝 Logged Interaction',
    edit_interaction: '✏️ Edited Fields',
    suggest_followup: '📋 Follow-up Suggestions',
    search_hcp: '🔍 HCP Search',
    summarize_interaction: '📄 Interaction Summary',
  };

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} animate-fade-in-up`}>
      {/* AI Avatar */}
      {!isUser && (
        <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shrink-0 mr-2.5 mt-0.5">
          <Bot className="w-3.5 h-3.5 text-white" />
        </div>
      )}

      <div
        className={`max-w-[82%] px-4 py-3 text-sm leading-relaxed ${
          isUser
            ? 'bg-gradient-to-br from-blue-500 to-indigo-500 text-white rounded-2xl rounded-br-sm shadow-sm'
            : 'bg-white text-slate-700 rounded-2xl rounded-bl-sm border border-slate-100 shadow-sm'
        }`}
      >
        <p className="whitespace-pre-wrap">{message.content}</p>

        {/* Tool badge */}
        {message.tool_used && (
          <div className={`flex items-center gap-1 mt-2 pt-2 border-t ${isUser ? 'border-blue-400/30' : 'border-slate-100'}`}>
            <Wrench className={`w-3 h-3 ${isUser ? 'text-blue-200' : 'text-slate-400'}`} />
            <span className={`text-xs font-medium ${isUser ? 'text-blue-200' : 'text-blue-500'}`}>
              {toolLabels[message.tool_used] || message.tool_used}
            </span>
          </div>
        )}
      </div>
    </div>
  );
}

export default ChatMessage;
