import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { sendChatMessage as apiSendChat } from '../../services/api';
import { setAllFields, setMultipleFields, setInteractionId } from '../interaction/interactionSlice';

// Async thunk: send message to AI agent
export const sendChatMessage = createAsyncThunk(
  'chat/sendMessage',
  async ({ message, formData, interactionId }, { dispatch, rejectWithValue }) => {
    try {
      const response = await apiSendChat(message, formData, interactionId);
      const { reply, form_updates, tool_used, interaction_id } = response.data;

      // If the AI returned form updates, update the interaction slice
      if (form_updates) {
        if (tool_used === 'log_interaction') {
          dispatch(setAllFields(form_updates));
        } else if (tool_used === 'edit_interaction') {
          dispatch(setMultipleFields(form_updates));
        }
      }

      // If we got an interaction_id back (after save), store it
      if (interaction_id) {
        dispatch(setInteractionId(interaction_id));
      }

      return { reply, tool_used };
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to send message');
    }
  }
);

const initialState = {
  messages: [
    {
      id: 'system-1',
      role: 'assistant',
      content: 'Hello! I\'m your AI assistant for logging HCP interactions. Describe your interaction (e.g., "Met Dr. Smith today, discussed Product X efficacy, positive sentiment, shared brochure") and I\'ll fill the form for you.',
      timestamp: new Date().toISOString(),
    },
  ],
  isLoading: false,
  error: null,
};

const chatSlice = createSlice({
  name: 'chat',
  initialState,
  reducers: {
    addMessage: (state, action) => {
      state.messages.push(action.payload);
    },
    clearChat: (state) => {
      state.messages = [initialState.messages[0]];
    },
    setError: (state, action) => {
      state.error = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(sendChatMessage.pending, (state, action) => {
        state.isLoading = true;
        state.error = null;
        // Add user message immediately
        state.messages.push({
          id: `user-${Date.now()}`,
          role: 'user',
          content: action.meta.arg.message,
          timestamp: new Date().toISOString(),
        });
      })
      .addCase(sendChatMessage.fulfilled, (state, action) => {
        state.isLoading = false;
        // Add AI response
        state.messages.push({
          id: `ai-${Date.now()}`,
          role: 'assistant',
          content: action.payload.reply,
          tool_used: action.payload.tool_used,
          timestamp: new Date().toISOString(),
        });
      })
      .addCase(sendChatMessage.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
        state.messages.push({
          id: `error-${Date.now()}`,
          role: 'assistant',
          content: `Sorry, an error occurred: ${action.payload}. Please try again.`,
          timestamp: new Date().toISOString(),
        });
      });
  },
});

export const { addMessage, clearChat, setError } = chatSlice.actions;

// Selectors
export const selectMessages = (state) => state.chat.messages;
export const selectIsLoading = (state) => state.chat.isLoading;
export const selectError = (state) => state.chat.error;

export default chatSlice.reducer;
