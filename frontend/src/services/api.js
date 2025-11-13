import axios from "axios";

const API = axios.create({ 
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000" 
});

// Add JWT to headers
API.interceptors.request.use((req) => {
  const token = localStorage.getItem("token");
  if (token) {
    req.headers.Authorization = `Bearer ${token}`;
  }
  return req;
});

// Response interceptor for error handling
API.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

// Auth endpoints
export const loginUser = (data) => API.post("/user/login", data);
export const signupUser = (data) => API.post("/user/signup", data);
export const getCurrentUser = () => API.get("/user/me");

// Analysis endpoints
export const analyzeText = (data) => API.post("/analyze/", data);
export const summarizeText = (data) => API.post("/analyze/summarize", data);
export const generateQuestions = (data) => API.post("/analyze/questions", data);

// Chatbot endpoint
export const chatWithBot = (query) => API.post("/chatbot/ask", { query });

// Progress endpoint
export const getProgress = (days = 30) => API.get(`/progress/?days=${days}`);

// Recommendations endpoint
export const getRecommendations = () => API.get("/recommend/");

// Gamification endpoints
export const updateXP = (data) => API.post("/gamify/xp", data);
export const getBadges = () => API.get("/gamify/badges");
export const getLeaderboard = (limit = 10) => API.get(`/gamify/leaderboard?limit=${limit}`);

// Advanced AI Features endpoints
export const contextualCorrection = (data) => API.post("/advanced-ai/contextual-correction", data);
export const coherenceAnalysis = (data) => API.post("/advanced-ai/coherence-analysis", data);
export const toneTransfer = (data) => API.post("/advanced-ai/tone-transfer", data);
export const getAvailableTones = () => API.get("/advanced-ai/available-tones");
export const detectTone = (data) => API.post("/advanced-ai/detect-tone", data);
export const writingQualityScore = (data) => API.post("/advanced-ai/quality-score", data);
export const emotionIntentAnalysis = (data) => API.post("/advanced-ai/emotion-intent", data);
export const emotionAnalysis = (data) => API.post("/advanced-ai/emotion", data);
export const intentAnalysis = (data) => API.post("/advanced-ai/intent", data);
export const summarizeAndReview = (data) => API.post("/advanced-ai/summarize-review", data);
export const getGrammarLessons = (data) => API.post("/advanced-ai/grammar-lessons", data);
export const getGrammarTopics = () => API.get("/advanced-ai/grammar-topics");
export const generateGrammarDrill = (data) => API.post("/advanced-ai/grammar-drill", data);
export const generateDrillByType = (errorType, data) => API.post(`/advanced-ai/grammar-drill/${errorType}`, data);
export const getDailyChallenge = (category = null) => {
  const url = category ? `/advanced-ai/daily-challenge?category=${category}` : "/advanced-ai/daily-challenge";
  return API.get(url);
};
export const getChallengeCategories = () => API.get("/advanced-ai/challenge-categories");

// Evaluation Metrics endpoints
export const getGrammarAccuracy = (data) => API.post("/evaluation/grammar-accuracy", data);
export const getRephrasingQuality = (data) => API.post("/evaluation/rephrasing-quality", data);
export const getAIQuality = (data) => API.post("/evaluation/ai-quality", data);
export const getLearningEffectiveness = () => API.get("/evaluation/learning-effectiveness");
export const getProgressTrends = (days = 30) => API.get(`/evaluation/progress-trends?days=${days}`);
export const getSystemPerformance = () => API.get("/evaluation/system-performance");
export const getFeatureUsage = (days = 30) => API.get(`/evaluation/feature-usage?days=${days}`);
export const getQualityMetrics = () => API.get("/evaluation/quality");
export const getComprehensiveReport = (days = 30) => API.get(`/evaluation/comprehensive-report?days=${days}`);
export const getEvaluationDashboard = (days = 30) => API.get(`/evaluation/dashboard?days=${days}`);

// Advanced Features API
export const generateDialog = (data) => API.post('/advanced/dialog/generate', data);
export const generateDialogResponse = (data) => API.post('/advanced/dialog/respond', data);
export const evaluateDialog = (data) => API.post('/advanced/dialog/evaluate', data);
export const getErrorPatterns = (days = 30) => API.get(`/advanced/error-patterns?days=${days}`);
export const getPerformanceLevel = (days = 30) => API.get(`/advanced/performance-level?days=${days}`);
export const calculateDifficulty = (data) => API.post('/advanced/difficulty/calculate', data);
export const adjustDifficulty = (data) => API.post('/advanced/difficulty/adjust', data);
export const analyzeWritingStyle = (data) => API.post('/advanced/style/analyze', data);
export const compareSimilarity = (data) => API.post('/advanced/similarity/compare', data);
export const scoreEssay = (data) => API.post('/advanced/essay/score', data);
export const classifyDialogue = (data) => API.post('/advanced/dialogue/classify', data);
export const getLearningPath = (days = 30) => API.get(`/advanced/learning-path?days=${days}`);
export const checkPlagiarism = (data) => API.post('/advanced/plagiarism/check', data);
export const extractKeywords = (data) => API.post('/advanced/keywords/extract', data);

export default API;
