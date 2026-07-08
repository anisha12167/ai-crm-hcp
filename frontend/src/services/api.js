import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Chat
export const sendChatMessage = (message, formData, interactionId) =>
  api.post('/chat', {
    message,
    current_form_data: formData,
    interaction_id: interactionId,
  });

// HCPs
export const fetchHCPs = (search = '') =>
  api.get('/hcps', { params: { search } });

// Interactions
export const fetchInteractions = () => api.get('/interactions');
export const fetchInteraction = (id) => api.get(`/interactions/${id}`);
export const createInteraction = (data) => api.post('/interactions', data);
export const updateInteraction = (id, data) => api.put(`/interactions/${id}`, data);
export const deleteInteraction = (id) => api.delete(`/interactions/${id}`);

// Materials
export const fetchMaterials = (search = '') =>
  api.get('/materials', { params: { search } });

export default api;
