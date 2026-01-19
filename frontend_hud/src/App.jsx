import React, { useState, useEffect, useContext } from 'react';
import { LayoutDashboard, Wallet, LineChart, Settings, Power, Wifi, Activity } from 'lucide-react';

// --- IMPORTAÇÕES ---
import Navbar from './components/Navbar';
import LandingPage from './components/LandingPage'; 
import PortfolioView from './components/views/PortfolioView'; 
import TechAnalysisView from './components/views/TechAnalysisView'; 
import MarketOverview from './components/views/MarketOverview'; // <--- Importação correta

import { AuthProvider, AuthContext } from './context/AuthContext'; 

const API_URL = 'http://localhost:8000/market/all'; 

// 1. ENVELOPE
export default function App() {
  return (
    <AuthProvider>
      <MainLayout />
    </AuthProvider>
  );
}

// 2. LAYOUT
function MainLayout() {
  const { user, logout } = useContext(AuthContext); 
  const [currentTab, setCurrentTab] = useState('overview'); 
  const [lastUpdate, setLastUpdate] = useState(new Date());
  const [demoMode, setDemoMode] = useState(false); 

  // (Removi o fetchData daqui pois o MarketOverview agora cuida dos proprios dados)
  
  // LOGIN / LANDING PAGE
  if (!user && !demoMode) {
    return (
      <div className="bg-slate-950 min-h-screen">
        <Navbar /> 
        <LandingPage onEnter={() => setDemoMode(true)} />
      </div>
    );
  }

  // DASHBOARD
  return (
    <div className="min-h-screen bg-[#0a0a0a] text-slate-200 font-sans flex overflow-hidden">
      
      {/* SIDEBAR */}
      <aside className="w-72 h-screen bg-[#050505] border-r border-slate-800 flex flex-col z-20 shadow-xl">
        <div className="p-8 border-b border-slate-800/50">
           <h1 className="text-3xl font-black text-white tracking-tighter">
             IF<span className="text-cyan-500">MD</span>
           </h1>
           <p className="text-[10px] text-slate-500 tracking-widest mt-1">
             {user ? `PRO TERMINAL v2.2` : `DEMO MODE (VISITOR)`}
           </p>
           {user && (
             <p className="text-xs text-cyan-400 mt-2 font-mono">USER: {user.name?.split(' ')[0].toUpperCase()}</p>
           )}
        </div>

        <nav className="flex-1 p-6 space-y-4">
          <NavItem 
            icon={<LayoutDashboard size={20}/>} 
            label="Market Overview" 
            active={currentTab === 'overview'}
            onClick={() => setCurrentTab('overview')}
          />
          <NavItem 
            icon={<Wallet size={20}/>} 
            label="Smart Portfolio" 
            active={currentTab === 'portfolio'}
            onClick={() => setCurrentTab('portfolio')}
          />
          <NavItem 
            icon={<LineChart size={20}/>} 
            label="Technical Analysis" 
            active={currentTab === 'tech'}
            onClick={() => setCurrentTab('tech')}
          />
        </nav>

        <div className="p-6 border-t border-slate-800/50">
          <button 
            onClick={() => {
              if (user) logout();
              setDemoMode(false);
            }} 
            className="flex items-center gap-3 text-red-400 hover:text-red-300 text-sm font-bold w-full p-4 rounded-lg hover:bg-red-900/10 transition-colors"
          >
            <Power size={18} /> {user ? "DESCONECTAR" : "SAIR DA DEMO"}
          </button>
        </div>
      </aside>

      {/* ÁREA PRINCIPAL */}
      <main className="flex-1 flex flex-col h-screen overflow-hidden bg-[#0a0a0a] relative">
        
        {/* HEADER (CORRIGIDO: Só mostra texto aqui, não o componente) */}
        <header className="flex items-center justify-between px-10 py-6 border-b border-slate-800/50 bg-[#0a0a0a]/90 backdrop-blur z-10">
          <div>
            <h2 className="text-2xl font-bold text-white tracking-tight flex items-center gap-3">
              {currentTab === 'overview' && 'Market Overview'}
              {currentTab === 'portfolio' && 'Smart Portfolio'}
              {currentTab === 'tech' && 'Technical Analysis'}
              
              <span className="text-xs bg-cyan-900/30 text-cyan-400 px-2 py-1 rounded border border-cyan-800 animate-pulse">LIVE</span>
            </h2>
            <div className="flex items-center gap-2 text-xs text-slate-500 font-mono mt-1">
              <Activity size={12} className="text-emerald-500" />
              INTELLIGENCE FLOW OPERATIONAL
            </div>
          </div>
        </header>

        {/* CONTEÚDO PRINCIPAL (CORRIGIDO: Aqui sim entra o Componente) */}
        <div className="flex-1 overflow-y-auto p-2 md:p-6 scrollbar-thin scrollbar-thumb-slate-800 scrollbar-track-transparent">
          
          {/* Carrega o NOVO Dashboard Profissional */}
          {currentTab === 'overview' && <MarketOverview />}

          {/* Outras Views */}
          {currentTab === 'portfolio' && <PortfolioView />}
          {currentTab === 'tech' && <TechAnalysisView />}

        </div>
      </main>
    </div>
  );
}

function NavItem({ icon, label, active, onClick }) {
  return (
    <button 
      onClick={onClick}
      className={`
        flex items-center gap-4 w-full p-3 rounded-lg text-sm font-medium transition-all duration-200 group
        ${active 
          ? 'bg-gradient-to-r from-cyan-500/10 to-transparent text-cyan-400 border-l-2 border-cyan-400 shadow-[0_0_15px_rgba(34,211,238,0.1)]' 
          : 'text-slate-400 hover:bg-white/5 hover:text-white hover:pl-5'}
    `}>
      <span className={active ? "text-cyan-400" : "text-slate-500 group-hover:text-white transition-colors"}>
        {icon}
      </span>
      {label}
    </button>
  );
}