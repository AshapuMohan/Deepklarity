import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';

const api = axios.create({
    baseURL: API_URL,
});

export const generateQuiz = async (url) => {
    try {
        const response = await api.post('/quiz/generate', { url });
        return response.data;
    } catch (error) {
        console.error("Error generating quiz:", error);
        throw error;
    }
};

export const getQuizHistory = async () => {
    try {
        const response = await api.get('/quiz/history');
        return response.data;
    } catch (error) {
        console.error("Error fetching history:", error);
        throw error;
    }
};

export const getQuizDetails = async (id) => {
    try {
        const response = await api.get(`/quiz/${id}`);
        return response.data;
    } catch (error) {
        console.error("Error fetching quiz details:", error);
        throw error;
    }
};

export default api;
