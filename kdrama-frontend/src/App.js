import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  // --- 1. ALL STATES ---
  const [view, setView] = useState('search'); 
  const [query, setQuery] = useState('');
  const [searchType, setSearchType] = useState('Cast'); // Restored for toggle
  const [genre, setGenre] = useState('');              // Added
  const [minRating, setMinRating] = useState(8.5);      // Added
  const [results, setResults] = useState([]);
  const [bingeResult, setBingeResult] = useState(null);

  // --- 2. ALL FUNCTIONS ---

  // FEATURE 1: Search (Restored with type)
  const handleSearch = async (e) => {
    e.preventDefault();
    const response = await axios.get(`http://127.0.0.1:8000/dramas/search`, {
      params: { query: query, type: searchType }
    });
    setResults(response.data);
    setView('search');
  };

  // FEATURE 2: Top 10
  const getTop10 = async () => {
    const response = await axios.get(`http://127.0.0.1:8000/dramas/top10`);
    setResults(response.data);
    setView('search'); 
  };

  // FEATURE 3: Smart Recommender (Restored UI connection)
  const handleRecommend = async (e) => {
    e.preventDefault();
    const response = await axios.get(`http://127.0.0.1:8000/dramas/recommend`, {
      params: { genre: genre, min_rating: minRating }
    });
    setResults(response.data);
    setView('search'); 
  };

  // FEATURE 4: Binge Planner
  const calculateBinge = async (e) => {
    e.preventDefault();
    const response = await axios.get(`http://127.0.0.1:8000/dramas/binge`, {
      params: { name: e.target.drama.value, episodes_per_day: e.target.pace.value }
    });
    setBingeResult(response.data);
    setView('binge');
  };

  // --- 3. THE UI (JSX) ---
  return (
    <div className="App">
      <nav className="navbar">
        <button onClick={() => setView('search')}>🔍 Search Person</button>
        <button onClick={() => setView('recommend')}>⭐ Genre Filter</button>
        <button onClick={getTop10}>🏆 Top 10</button>
        <button onClick={() => setView('binge')}>📅 Binge Planner</button>
      </nav>

      <header className="header">
        <h1>✨ K-Drama Master Tool</h1>
        
        {/* Search View Form */}
        {view === 'search' && (
          <form onSubmit={handleSearch} className="search-box">
            <select value={searchType} onChange={(e) => setSearchType(e.target.value)} className="search-dropdown">
              <option value="Cast">Cast</option>
              <option value="Director">Director</option>
            </select>
            <input type="text" placeholder={`Search ${searchType}...`} value={query} onChange={(e) => setQuery(e.target.value)} />
            <button type="submit">Search</button>
          </form>
        )}

        {/* Recommend View Form */}
        {view === 'recommend' && (
          <form onSubmit={handleRecommend} className="search-box">
            <input type="text" placeholder="Enter Genre..." value={genre} onChange={(e) => setGenre(e.target.value)} />
            <input type="number" step="0.1" value={minRating} onChange={(e) => setMinRating(e.target.value)} style={{width: '80px'}} />
            <button type="submit">Get Recommendations</button>
          </form>
        )}
      </header>

      <main className="content">
        {/* Results Grid (Shared by Search, Top 10, and Recommend) */}
        {view !== 'binge' && results.length > 0 && (
          <div className="results-container">
            {results.map((drama, i) => (
              <div key={i} className="drama-card">
                <h3>{drama.Name}</h3>
                <p className="rating">⭐ {drama.Rating}</p>
                <p className="genres">🎭 {drama.Genre}</p>
                <small>{drama.Cast}</small>
              </div>
            ))}
          </div>
        )}

        {/* Binge View */}
        {view === 'binge' && (
          <div className="binge-container">
            <form onSubmit={calculateBinge} className="binge-form">
              <input name="drama" placeholder="Drama Name" required />
              <input name="pace" type="number" placeholder="Episodes per day" required />
              <button type="submit">Calculate</button>
            </form>
            {bingeResult && !bingeResult.error && (
              <div className="binge-card">
                <h2>{bingeResult.name}</h2>
                <p>Total time: <strong>{bingeResult.total_hours} hours</strong></p>
                <p>Finish in: <strong>{bingeResult.days} days</strong></p>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;