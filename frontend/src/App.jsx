import { useState } from 'react'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('miscrits')

  return (
    <>
      <header className="header">
        <h1>🎮 Miscrits Nexus</h1>
        <p>Your comprehensive Miscrits database and tools</p>
      </header>
      
      <nav className="nav-tabs">
        <button 
          className={`tab ${activeTab === 'miscrits' ? 'active' : ''}`}
          onClick={() => setActiveTab('miscrits')}
        >
          Miscrits Database
        </button>
        <button 
          className={`tab ${activeTab === 'moves' ? 'active' : ''}`}
          onClick={() => setActiveTab('moves')}
        >
          Moves Database
        </button>
        <button 
          className={`tab ${activeTab === 'relics' ? 'active' : ''}`}
          onClick={() => setActiveTab('relics')}
        >
          Relics Calculator
        </button>
      </nav>

      <main className="main-content">
        {activeTab === 'miscrits' && (
          <div className="tab-content">
            <h2>Miscrits Database</h2>
            <p>Explore all Miscrits data including stats, abilities, and more!</p>
            <div className="placeholder-card">
              <p>🔍 Search and filter Miscrits coming soon...</p>
            </div>
          </div>
        )}
        
        {activeTab === 'moves' && (
          <div className="tab-content">
            <h2>Moves Database</h2>
            <p>Browse all available moves and their effects.</p>
            <div className="placeholder-card">
              <p>⚔️ Move database interface coming soon...</p>
            </div>
          </div>
        )}
        
        {activeTab === 'relics' && (
          <div className="tab-content">
            <h2>Relics Calculator</h2>
            <p>Calculate optimal relic combinations for your Miscrits.</p>
            <div className="placeholder-card">
              <p>🔮 Relic calculator coming soon...</p>
            </div>
          </div>
        )}
      </main>
    </>
  )
}

export default App
