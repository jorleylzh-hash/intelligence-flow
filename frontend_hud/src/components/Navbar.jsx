import React, { useState, useContext } from 'react';
import { LayoutDashboard, LogIn, UserPlus, LogOut, Menu } from 'lucide-react';
import AuthModal from './AuthModal';
import { AuthContext } from '../context/AuthContext';

export default function Navbar() {
    const { user, logout } = useContext(AuthContext); // Pega dados do usuário logado
    const [isAuthOpen, setAuthOpen] = useState(false);
    const [authMode, setAuthMode] = useState('login'); // 'login' ou 'signup'

    // Função para abrir o modal no modo certo
    const openAuth = (mode) => {
        setAuthMode(mode);
        setAuthOpen(true);
    };

    return (
        <>
            {/* BARRA DE NAVEGAÇÃO FIXA NO TOPO */}
            <nav className="w-full h-16 bg-slate-950/90 backdrop-blur-md border-b border-slate-800 flex items-center justify-between px-6 fixed top-0 z-40 shadow-lg shadow-black/50">
                
                {/* 1. LOGO E MARCA */}
                <div className="flex items-center gap-3 hover:opacity-80 transition-opacity cursor-pointer">
                    <div className="w-9 h-9 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-lg flex items-center justify-center shadow-[0_0_15px_rgba(6,182,212,0.4)]">
                        <span className="text-white font-bold font-mono text-lg">IF</span>
                    </div>
                    <div className="flex flex-col leading-none">
                        <span className="text-white font-bold tracking-widest text-sm">INTELLIGENCE</span>
                        <span className="text-cyan-400 font-bold tracking-widest text-sm">FLOW</span>
                    </div>
                </div>

                {/* 2. BOTÕES DE AÇÃO (DIREITA) */}
                <div className="flex items-center gap-4">
                    
                    {user ? (
                        // --- ESTADO LOGADO ---
                        <div className="flex items-center gap-4 animate-fadeIn">
                            {/* Saudação */}
                            <div className="hidden md:flex flex-col items-end text-xs mr-2">
                                <span className="text-slate-400">Bem-vindo,</span>
                                <span className="text-cyan-300 font-bold uppercase">{user.name || user.email}</span>
                            </div>

                            {/* Botão Sair */}
                            <button 
                                onClick={logout}
                                className="flex items-center gap-2 px-4 py-2 rounded-lg border border-red-500/20 text-red-400 hover:bg-red-500/10 hover:border-red-500/50 transition-all text-xs font-bold tracking-wide"
                            >
                                <LogOut size={16} />
                                SAIR
                            </button>
                        </div>
                    ) : (
                        // --- ESTADO DESLOGADO (VISITANTE) ---
                        <div className="flex items-center gap-3">
                            {/* Botão Demo (Apenas Visual) */}
                            <button className="hidden md:flex items-center gap-2 px-4 py-2 text-slate-400 hover:text-white transition-colors text-xs font-bold tracking-wide">
                                <LayoutDashboard size={16} />
                                VISUALIZAR DEMO
                            </button>

                            {/* Divisória Visual */}
                            <div className="h-6 w-px bg-slate-800 hidden md:block"></div>

                            {/* Botão Login */}
                            <button 
                                onClick={() => openAuth('login')}
                                className="flex items-center gap-2 px-4 py-2 rounded-lg border border-slate-700 text-slate-300 hover:border-cyan-500/50 hover:text-cyan-400 hover:bg-cyan-950/30 transition-all text-xs font-bold tracking-wide"
                            >
                                <LogIn size={16} />
                                LOGIN
                            </button>

                            {/* Botão Criar Conta (Destaque) */}
                            <button 
                                onClick={() => openAuth('signup')}
                                className="flex items-center gap-2 px-4 py-2 rounded-lg bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white shadow-[0_0_15px_rgba(6,182,212,0.3)] hover:shadow-[0_0_25px_rgba(6,182,212,0.5)] transition-all text-xs font-bold tracking-wide transform hover:-translate-y-0.5"
                            >
                                <UserPlus size={16} />
                                CRIAR CONTA
                            </button>
                        </div>
                    )}
                </div>
            </nav>

            {/* 3. MODAL DE AUTENTICAÇÃO (Invisível até ser chamado) */}
            <AuthModal 
                isOpen={isAuthOpen} 
                onClose={() => setAuthOpen(false)} 
                initialMode={authMode} 
            />
        </>
    );
}