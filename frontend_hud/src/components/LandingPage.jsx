import React, { useState } from 'react';
import { Cpu, Zap, Globe, Lock, ChevronRight, Activity, Eye, BarChart2 } from 'lucide-react';

export default function LandingPage({ onEnter }) {
    const [hoveredIndex, setHoveredIndex] = useState(null);

    const features = [
        {
            icon: <Cpu size={32} />,
            title: "MOTOR DE I.A.",
            color: "text-cyan-400",
            border: "hover:border-cyan-400/50",
            shadow: "hover:shadow-cyan-500/20",
            desc: "Integração nativa com Gemini 2.5 Flash. Processa contexto de mercado, notícias e sentimento em milissegundos."
        },
        {
            icon: <Eye size={32} />,
            title: "VISÃO SMC",
            color: "text-purple-400",
            border: "hover:border-purple-400/50",
            shadow: "hover:shadow-purple-500/20",
            desc: "Análise institucional pura. Identifica Order Blocks, Zonas de Liquidez e FVG (Fair Value Gaps) automaticamente."
        },
        {
            icon: <Globe size={32} />,
            title: "ARBITRAGEM HFT",
            color: "text-yellow-400",
            border: "hover:border-yellow-400/50",
            shadow: "hover:shadow-yellow-500/20",
            desc: "Cálculo de paridade em tempo real (Dólar/EWZ vs Ibovespa). Detecta ágio ou desconto (Spread) matemático."
        },
        {
            icon: <BarChart2 size={32} />,
            title: "CORRELAÇÃO MACRO",
            color: "text-emerald-400",
            border: "hover:border-emerald-400/50",
            shadow: "hover:shadow-emerald-500/20",
            desc: "Monitoramento cruzado de 10+ ativos globais (China, S&P500, DXY) para validar a direção do fluxo local."
        }
    ];

    return (
        <div className="min-h-screen bg-[#050b14] text-white flex flex-col items-center justify-center relative overflow-hidden font-sans selection:bg-cyan-500/30">
            
            {/* BACKGROUND VIVO (GRID ANIMADO) */}
            <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 z-0"></div>
            <div className="absolute inset-0 z-0 opacity-20" 
                 style={{
                     backgroundImage: 'linear-gradient(#1e293b 1px, transparent 1px), linear-gradient(to right, #1e293b 1px, transparent 1px)',
                     backgroundSize: '40px 40px'
                 }}>
            </div>

            {/* CONTEÚDO CENTRAL */}
            <div className="z-10 w-full max-w-6xl px-6 flex flex-col items-center">
                
                {/* HERO SECTION */}
                <div className="text-center mb-16 animate-fade-in-up">
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-900/30 border border-cyan-800 text-cyan-400 text-xs font-bold tracking-widest mb-6">
                        <Activity size={14} className="animate-pulse"/> SISTEMA ONLINE v2.0
                    </div>
                    <h1 className="text-5xl md:text-7xl font-bold tracking-tighter mb-4 bg-clip-text text-transparent bg-gradient-to-b from-white to-slate-500">
                        INTELLIGENCE FLOW
                    </h1>
                    <p className="text-slate-400 text-lg md:text-xl max-w-2xl mx-auto leading-relaxed">
                        A fusão definitiva entre <span className="text-cyan-400 font-bold">Inteligência Artificial</span> e <span className="text-purple-400 font-bold">Price Action Institucional</span>. 
                        Decifre o rastro do dinheiro esperto.
                    </p>
                </div>

                {/* GRID INTERATIVO (ONDE O MOUSE BRILHA) */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full mb-16">
                    {features.map((item, index) => (
                        <div 
                            key={index}
                            onMouseEnter={() => setHoveredIndex(index)}
                            onMouseLeave={() => setHoveredIndex(null)}
                            className={`
                                group relative p-8 rounded-2xl border border-slate-800 bg-slate-900/40 backdrop-blur-sm
                                transition-all duration-500 ease-out cursor-default
                                hover:-translate-y-2 ${item.border} ${item.shadow} hover:shadow-2xl
                            `}
                        >
                            {/* Efeito de Glow Interno ao passar o mouse */}
                            <div className={`absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-10 transition-opacity duration-500 bg-gradient-to-r from-transparent via-white to-transparent`}></div>

                            <div className="flex items-start justify-between mb-4">
                                <div className={`p-3 rounded-lg bg-slate-800/50 ${item.color} group-hover:scale-110 transition-transform duration-300`}>
                                    {item.icon}
                                </div>
                                <div className={`text-xs font-mono text-slate-600 transition-colors duration-300 ${item.color.replace('text', 'group-hover:text')}`}>
                                    MODULO 0{index + 1}
                                </div>
                            </div>

                            <h3 className="text-2xl font-bold text-slate-200 mb-2 group-hover:text-white transition-colors">
                                {item.title}
                            </h3>
                            <p className="text-slate-500 leading-relaxed group-hover:text-slate-300 transition-colors">
                                {item.desc}
                            </p>
                        </div>
                    ))}
                </div>

                {/* BOTÃO DE ENTRADA (BOOT) */}
                <button 
                    onClick={onEnter}
                    className="group relative px-10 py-4 bg-cyan-600 hover:bg-cyan-500 text-white font-bold tracking-widest rounded-lg overflow-hidden transition-all duration-300 hover:scale-105 shadow-[0_0_40px_rgba(8,145,178,0.3)]"
                >
                    <div className="absolute inset-0 w-full h-full bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover:animate-shimmer"></div>
                    <span className="flex items-center gap-3">
                        INICIALIZAR DASHBOARD <ChevronRight />
                    </span>
                </button>
            
            </div>

            {/* FOOTER */}
            <div className="absolute bottom-6 text-slate-600 text-xs font-mono">
                DESENVOLVIDO POR INTELLIGENCE FLOW LTDA. © 2026
            </div>
        </div>
    );
}