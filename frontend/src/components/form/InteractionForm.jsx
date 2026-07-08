import { useSelector } from 'react-redux';
import { selectFormData } from '../../features/interaction/interactionSlice';
import {
  User, CalendarDays, Clock, Users, MessageSquareText,
  FileText, Mic, Package, TrendingUp, ChevronDown
} from 'lucide-react';

function InteractionForm() {
  const formData = useSelector(selectFormData);

  const sentimentClass = formData.sentiment === 'Positive'
    ? 'badge-positive'
    : formData.sentiment === 'Negative'
      ? 'badge-negative'
      : 'badge-neutral';

  return (
    <div className="p-8 max-w-3xl mx-auto">
      {/* Section Header */}
      <div className="mb-8">
        <h1 className="text-xl font-bold text-slate-900 tracking-tight">Log HCP Interaction</h1>
        <p className="text-sm text-slate-400 mt-1">Fields are populated automatically by the AI assistant →</p>
      </div>

      {/* Interaction Details Section */}
      <div className="mb-6">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-1 h-5 bg-gradient-to-b from-blue-500 to-indigo-500 rounded-full"></div>
          <h2 className="text-sm font-semibold text-slate-700 uppercase tracking-wider">Interaction Details</h2>
        </div>

        {/* Row 1: HCP Name + Interaction Type */}
        <div className="grid grid-cols-2 gap-5 mb-5">
          <div className="group">
            <label className="flex items-center gap-1.5 text-xs font-medium text-slate-500 mb-1.5 uppercase tracking-wider">
              <User className="w-3 h-3" />
              HCP Name
            </label>
            <div className="relative">
              <input
                type="text"
                value={formData.hcp_name}
                readOnly
                placeholder="Populated by AI..."
                className={`w-full px-3.5 py-2.5 border border-slate-200 rounded-lg bg-slate-50/50 text-slate-900 text-sm placeholder:text-slate-300 focus:outline-none cursor-default transition-all ${formData.hcp_name ? 'border-blue-200 bg-blue-50/30' : ''}`}
              />
              {formData.hcp_name && (
                <div className="absolute right-2.5 top-1/2 -translate-y-1/2 w-2 h-2 bg-emerald-400 rounded-full"></div>
              )}
            </div>
          </div>

          <div>
            <label className="flex items-center gap-1.5 text-xs font-medium text-slate-500 mb-1.5 uppercase tracking-wider">
              <FileText className="w-3 h-3" />
              Interaction Type
            </label>
            <div className="relative">
              <select
                value={formData.interaction_type}
                disabled
                className={`w-full px-3.5 py-2.5 border border-slate-200 rounded-lg bg-slate-50/50 text-slate-900 text-sm appearance-none cursor-default transition-all ${formData.interaction_type !== 'Meeting' ? 'border-blue-200 bg-blue-50/30' : ''}`}
              >
                <option value="Meeting">Meeting</option>
                <option value="Call">Call</option>
                <option value="Email">Email</option>
                <option value="Video Conference">Video Conference</option>
              </select>
              <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-300 pointer-events-none" />
            </div>
          </div>
        </div>

        {/* Row 2: Date + Time */}
        <div className="grid grid-cols-2 gap-5 mb-5">
          <div>
            <label className="flex items-center gap-1.5 text-xs font-medium text-slate-500 mb-1.5 uppercase tracking-wider">
              <CalendarDays className="w-3 h-3" />
              Date
            </label>
            <input
              type="date"
              value={formData.date}
              readOnly
              className="w-full px-3.5 py-2.5 border border-slate-200 rounded-lg bg-slate-50/50 text-slate-900 text-sm cursor-default"
            />
          </div>
          <div>
            <label className="flex items-center gap-1.5 text-xs font-medium text-slate-500 mb-1.5 uppercase tracking-wider">
              <Clock className="w-3 h-3" />
              Time
            </label>
            <input
              type="time"
              value={formData.time}
              readOnly
              className="w-full px-3.5 py-2.5 border border-slate-200 rounded-lg bg-slate-50/50 text-slate-900 text-sm cursor-default"
            />
          </div>
        </div>

        {/* Attendees */}
        <div className="mb-5">
          <label className="flex items-center gap-1.5 text-xs font-medium text-slate-500 mb-1.5 uppercase tracking-wider">
            <Users className="w-3 h-3" />
            Attendees
          </label>
          <input
            type="text"
            value={formData.attendees}
            readOnly
            placeholder="Populated by AI..."
            className={`w-full px-3.5 py-2.5 border border-slate-200 rounded-lg bg-slate-50/50 text-slate-900 text-sm placeholder:text-slate-300 cursor-default ${formData.attendees ? 'border-blue-200 bg-blue-50/30' : ''}`}
          />
        </div>

        {/* Topics Discussed */}
        <div className="mb-4">
          <label className="flex items-center gap-1.5 text-xs font-medium text-slate-500 mb-1.5 uppercase tracking-wider">
            <MessageSquareText className="w-3 h-3" />
            Topics Discussed
          </label>
          <textarea
            value={formData.topics_discussed}
            readOnly
            placeholder="Populated by AI..."
            rows={3}
            className={`w-full px-3.5 py-2.5 border border-slate-200 rounded-lg bg-slate-50/50 text-slate-900 text-sm placeholder:text-slate-300 resize-none cursor-default ${formData.topics_discussed ? 'border-blue-200 bg-blue-50/30' : ''}`}
          />
        </div>

        {/* Voice Note CTA */}
        <div className="mb-6">
          <button className="flex items-center gap-1.5 text-xs text-blue-500 hover:text-blue-600 transition-colors font-medium">
            <Mic className="w-3.5 h-3.5" />
            Summarize from Voice Note (Requires Consent)
          </button>
        </div>
      </div>

      {/* Sentiment */}
      {formData.sentiment && (
        <div className="mb-6 animate-fade-in-up">
          <div className="flex items-center gap-2 mb-3">
            <div className="w-1 h-5 bg-gradient-to-b from-emerald-500 to-teal-500 rounded-full"></div>
            <h2 className="text-sm font-semibold text-slate-700 uppercase tracking-wider">Sentiment</h2>
          </div>
          <div className="flex items-center gap-2">
            <TrendingUp className="w-4 h-4 text-slate-400" />
            <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold ${sentimentClass}`}>
              {formData.sentiment === 'Positive' && '😊 '}
              {formData.sentiment === 'Negative' && '😟 '}
              {formData.sentiment === 'Neutral' && '😐 '}
              {formData.sentiment}
            </span>
          </div>
        </div>
      )}

      {/* Notes */}
      {formData.notes && (
        <div className="mb-6 animate-fade-in-up">
          <div className="flex items-center gap-2 mb-3">
            <div className="w-1 h-5 bg-gradient-to-b from-amber-500 to-orange-500 rounded-full"></div>
            <h2 className="text-sm font-semibold text-slate-700 uppercase tracking-wider">Notes</h2>
          </div>
          <div className="text-sm text-slate-700 bg-amber-50/50 border border-amber-100 p-4 rounded-lg whitespace-pre-wrap">
            {formData.notes}
          </div>
        </div>
      )}

      {/* Materials Section */}
      <div className="mb-6">
        <div className="flex items-center gap-2 mb-3">
          <div className="w-1 h-5 bg-gradient-to-b from-violet-500 to-purple-500 rounded-full"></div>
          <h2 className="text-sm font-semibold text-slate-700 uppercase tracking-wider">Materials Shared</h2>
        </div>

        {formData.materials && formData.materials.length > 0 ? (
          <div className="space-y-2">
            {formData.materials.map((mat, i) => (
              <div
                key={i}
                className="flex items-center gap-2.5 px-3.5 py-2.5 bg-gradient-to-r from-violet-50 to-indigo-50 border border-violet-100 rounded-lg animate-fade-in-up"
              >
                <Package className="w-4 h-4 text-violet-400 shrink-0" />
                <span className="text-sm text-slate-700 font-medium">{mat}</span>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-sm text-slate-300 italic pl-1">No materials added yet.</p>
        )}
      </div>

      {/* Follow-up Actions */}
      {formData.follow_up && (
        <div className="mb-6 animate-fade-in-up">
          <div className="flex items-center gap-2 mb-3">
            <div className="w-1 h-5 bg-gradient-to-b from-sky-500 to-cyan-500 rounded-full"></div>
            <h2 className="text-sm font-semibold text-slate-700 uppercase tracking-wider">Follow-up Actions</h2>
          </div>
          <div className="text-sm text-slate-700 bg-sky-50/50 border border-sky-100 p-4 rounded-lg whitespace-pre-wrap leading-relaxed">
            {formData.follow_up}
          </div>
        </div>
      )}
    </div>
  );
}

export default InteractionForm;
