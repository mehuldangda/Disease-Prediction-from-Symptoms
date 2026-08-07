import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import LoadingModal from './components/LoadingModal';
import HomePage from './pages/HomePage';
import PredictPage from './pages/PredictPage';
import ResultPage from './pages/ResultPage';
import AboutPage from './pages/AboutPage';
import { fetchSymptoms, predictDisease } from './services/api';
import { savePredictionToHistory, getPredictionHistory, clearPredictionHistory } from './utils/historyStorage';

export default function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [theme, setTheme] = useState(() => localStorage.getItem('diagnowise_theme') || 'dark');
  
  const [symptomsList, setSymptomsList] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedSymptoms, setSelectedSymptoms] = useState([]);
  const [selectedModel, setSelectedModel] = useState('random_forest');
  
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [predictionResult, setPredictionResult] = useState(null);
  const [history, setHistory] = useState([]);

  // Theme Syncing
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('diagnowise_theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => (prev === 'dark' ? 'light' : 'dark'));
  };

  // Load Symptoms & History
  useEffect(() => {
    async function loadSymptomsCatalog() {
      try {
        const data = await fetchSymptoms();
        setSymptomsList(data.symptoms || []);
        setCategories(data.categories || []);
      } catch (err) {
        console.error('Error loading symptoms:', err);
        setError('Failed to connect to backend prediction API. Ensure FastAPI server is running on port 8000.');
      }
    }
    loadSymptomsCatalog();
    setHistory(getPredictionHistory());
  }, []);

  const handleToggleSymptom = (key) => {
    setSelectedSymptoms(prev => 
      prev.includes(key) ? prev.filter(s => s !== key) : [...prev, key]
    );
  };

  const handleClearAll = () => {
    setSelectedSymptoms([]);
    setPredictionResult(null);
    setError(null);
  };

  const handleRunPredict = async () => {
    if (selectedSymptoms.length === 0) return;
    setIsLoading(true);
    setError(null);

    // Minimum delay for smooth loading animation
    const minDelay = new Promise(resolve => setTimeout(resolve, 1800));

    try {
      const [result] = await Promise.all([
        predictDisease(selectedSymptoms, selectedModel),
        minDelay
      ]);
      setPredictionResult(result);
      const updatedHist = savePredictionToHistory(result, selectedSymptoms);
      setHistory(updatedHist);
      setCurrentPage('result');
    } catch (err) {
      setError(err.message || 'An error occurred during disease prediction.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <Navbar 
        currentPage={currentPage} 
        setCurrentPage={setCurrentPage} 
        theme={theme}
        toggleTheme={toggleTheme}
      />
      
      <main className="main-content">
        {currentPage === 'home' && (
          <HomePage onStartClick={() => setCurrentPage('predict')} />
        )}

        {currentPage === 'predict' && (
          <PredictPage 
            symptomsList={symptomsList}
            categories={categories}
            selectedSymptoms={selectedSymptoms}
            onToggleSymptom={handleToggleSymptom}
            onClearAll={handleClearAll}
            onPredict={handleRunPredict}
            isLoading={isLoading}
            error={error}
            selectedModel={selectedModel}
            setSelectedModel={setSelectedModel}
            history={history}
            onLoadHistoryItem={(histItem) => {
              setPredictionResult(histItem.result);
              setCurrentPage('result');
            }}
            onClearHistory={() => setHistory(clearPredictionHistory())}
          />
        )}

        {currentPage === 'result' && (
          <ResultPage 
            result={predictionResult}
            onReset={() => setCurrentPage('predict')}
          />
        )}

        {currentPage === 'about' && (
          <AboutPage />
        )}
      </main>

      <LoadingModal isOpen={isLoading} />

      <Footer />
    </div>
  );
}
