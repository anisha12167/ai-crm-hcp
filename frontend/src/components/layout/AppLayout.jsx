import { useSelector, useDispatch } from 'react-redux';
import { selectFormData, selectIsSaved, resetForm } from '../../features/interaction/interactionSlice';
import { clearChat } from '../../features/chat/chatSlice';
import { createInteraction } from '../../services/api';
import InteractionForm from '../form/InteractionForm';
import ChatPanel from '../chat/ChatPanel';
import { RotateCcw, Save, Sparkles } from 'lucide-react';
import { useState } from 'react';

function AppLayout() {
  const dispatch = useDispatch();
  const formData = useSelector(selectFormData);
  const isSaved = useSelector(selectIsSaved);
  const [saving, setSaving] = useState(false);
  const [saveMsg, setSaveMsg] = useState('');

  const handleNewInteraction = () => {
    dispatch(resetForm());
    dispatch(clearChat());
    setSaveMsg('');
  };

  const handleSave = async () => {
    if (!formData.hcp_name) {
      setSaveMsg('Please log an interaction first via the AI chat.');
      setTimeout(() => setSaveMsg(''), 3000);
      return;
    }
    setSaving(true);
    try {
      await createInteraction(formData);
      setSaveMsg('✓ Interaction saved to database!');
      setTimeout(() => setSaveMsg(''), 3000);
    } catch (err) {
      setSaveMsg('Failed to save. Try again.');
      setTimeout(() => setSaveMsg(''), 3000);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="flex flex-col h-screen">
      {/* Top Navigation Bar */}
      <header className="h-14 border-b border-slate-200 bg-white flex items-center justify-between px-6 shrink-0">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center">
            <Sparkles className="w-4 h-4 text-white" />
          </div>
          <h1 className="text-base font-bold tracking-tight">
            <span className="gradient-text">AI-First CRM</span>
            <span className="text-slate-400 font-normal ml-2 text-sm">HCP Module</span>
          </h1>
        </div>

        <div className="flex items-center gap-3">
          {saveMsg && (
            <span className={`text-xs font-medium px-3 py-1 rounded-full animate-fade-in-up ${saveMsg.includes('✓') ? 'bg-emerald-50 text-emerald-600' : 'bg-red-50 text-red-500'}`}>
              {saveMsg}
            </span>
          )}
          <button
            onClick={handleSave}
            disabled={saving || !formData.hcp_name}
            className="flex items-center gap-1.5 px-4 py-1.5 bg-gradient-to-r from-blue-500 to-indigo-500 text-white text-sm font-medium rounded-lg hover:from-blue-600 hover:to-indigo-600 transition-all disabled:opacity-40 disabled:cursor-not-allowed shadow-sm"
          >
            <Save className="w-3.5 h-3.5" />
            {saving ? 'Saving...' : 'Save'}
          </button>
          <button
            onClick={handleNewInteraction}
            className="flex items-center gap-1.5 px-4 py-1.5 text-sm font-medium text-slate-600 border border-slate-200 rounded-lg hover:bg-slate-50 transition-colors"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            New
          </button>
        </div>
      </header>

      {/* Main Content — Split Screen */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left Panel — Form (60% width) */}
        <div className="w-3/5 border-r border-slate-200 overflow-y-auto bg-white">
          <InteractionForm />
        </div>

        {/* Right Panel — Chat (40% width) */}
        <div className="w-2/5 flex flex-col bg-slate-50">
          <ChatPanel />
        </div>
      </div>
    </div>
  );
}

export default AppLayout;
