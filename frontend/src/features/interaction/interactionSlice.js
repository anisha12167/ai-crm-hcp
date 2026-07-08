import { createSlice } from '@reduxjs/toolkit';

const today = new Date().toISOString().split('T')[0]; // YYYY-MM-DD
const now = new Date().toTimeString().slice(0, 5);     // HH:MM

const initialState = {
  formData: {
    hcp_name: '',
    interaction_type: 'Meeting',
    date: today,
    time: now,
    attendees: '',
    topics_discussed: '',
    sentiment: '',
    materials: [],
    notes: '',
    follow_up: '',
  },
  interactionId: null,
  isSaved: false,
  isLoading: false,
};

const interactionSlice = createSlice({
  name: 'interaction',
  initialState,
  reducers: {
    // Update a single field
    setField: (state, action) => {
      const { field, value } = action.payload;
      state.formData[field] = value;
      state.isSaved = false;
    },

    // Update multiple fields at once (from AI tool response)
    setMultipleFields: (state, action) => {
      const updates = action.payload;
      Object.keys(updates).forEach((key) => {
        if (key in state.formData) {
          state.formData[key] = updates[key];
        }
      });
      state.isSaved = false;
    },

    // Replace entire form (from log_interaction tool)
    setAllFields: (state, action) => {
      state.formData = { ...state.formData, ...action.payload };
      state.isSaved = false;
    },

    // Reset form to blank
    resetForm: (state) => {
      const today = new Date().toISOString().split('T')[0];
      const now = new Date().toTimeString().slice(0, 5);
      state.formData = {
        hcp_name: '',
        interaction_type: 'Meeting',
        date: today,
        time: now,
        attendees: '',
        topics_discussed: '',
        sentiment: '',
        materials: [],
        notes: '',
        follow_up: '',
      };
      state.interactionId = null;
      state.isSaved = false;
    },

    // Set interaction ID after save
    setInteractionId: (state, action) => {
      state.interactionId = action.payload;
      state.isSaved = true;
    },

    setLoading: (state, action) => {
      state.isLoading = action.payload;
    },
  },
});

export const {
  setField,
  setMultipleFields,
  setAllFields,
  resetForm,
  setInteractionId,
  setLoading,
} = interactionSlice.actions;

// Selectors
export const selectFormData = (state) => state.interaction.formData;
export const selectInteractionId = (state) => state.interaction.interactionId;
export const selectIsSaved = (state) => state.interaction.isSaved;
export const selectIsLoading = (state) => state.interaction.isLoading;

export default interactionSlice.reducer;
