import React, { useRef, useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, Activity, Zap } from 'lucide-react';
import SourceBadge from './SourceBadge'; // Certifique-se que o caminho está certo

export default function AssetCard({ data }) {
    const prevPriceRef = useRef(data?.price);
    const [flashState, setFlashState] = useState(null);

    const { ticker, price, change, volume, source } = data || {}; // Desestrutura 'source'
    const safePrice = price ? Number(price) : 0;
    const safeChange = change ? Number(change) : 0;
    const isPositive = safeChange >= 0;

    useEffect(() => {
        if (!data || prevPriceRef.current === undefined) {
            prevPriceRef.current = safePrice;
            return;
        }
        if (safePrice > prevPriceRef.current) setFlashState('green');
        else if (safePrice < prevPriceRef.current) setFlashState('red');
        
        prevPriceRef.current = safePrice;
        const timer = setTimeout(() => setFlashState(null), 800);
        return () => clearTimeout(timer);
    }, [safePrice, data]); 

    if (!data) return <div className="animate-pulse bg-slate-800/50 h-[180px] rounded-2xl"></div>;

    let flashClass = "";
    if (flashState === 'green') flashClass = "border-emerald-400 shadow-[0_0_20px_rgba(52,211,153,0.6)] bg-emerald-900/30";
    else if (flashState === 'red') flashClass = "border-red-500 shadow-[0_0_20px_rgba(239,68,68,0.6)] bg-red-900/30";
    else flashClass = "border-slate-800 hover:border-cyan-500/50 hover:shadow-[0_0_15px_rgba(6,182,212,0.2)] bg-slate-900/50 backdrop-blur-md";

    return (
        <div className={`relative group p-6 rounded-2xl border h-[180px] flex flex-col justify-between transition-all duration-300 ${flashClass}`}>
            
            {flashState && (
                <div className="absolute top-2 right-2 animate-ping opacity-75">
                    <Zap size={16} className={flashState === 'green' ? "text-emerald-400" : "text-red-500"} fill="currentColor"/>
                </div>
            )}

            <div className="flex justify-between items-start">
                <div className="flex flex-col">
                    <h3 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
                        {ticker}
                    </h3>
                    {/* AQUI ESTÁ O BADGE DINÂMICO */}
                    <div className="mt-1"><SourceBadge source={source} /></div>
                </div>
                
                <div className={`flex items-center gap-1 px-2 py-1 rounded text-xs font-bold transition-colors duration-300 ${
                    isPositive ? 'bg-emerald-500/10 text-emerald-400' : 'bg-red-500/10 text-red-400'
                }`}>
                    {isPositive ? <TrendingUp size={14} /> : <TrendingDown size={14} />}
                    {safeChange > 0 ? '+' : ''}{safeChange.toFixed(2)}%
                </div>
            </div>

            <div className="my-2">
                <span className={`text-3xl font-mono font-bold transition-colors duration-300 ${
                    flashState === 'green' ? 'text-emerald-300' :
                    flashState === 'red' ? 'text-red-300' : 'text-slate-200'
                }`}>
                    {safePrice.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                </span>
            </div>

            <div className="flex items-center justify-between text-xs text-slate-500 border-t border-slate-700/50 pt-3 mt-auto">
                <div className="flex items-center gap-1 font-mono">
                    <Activity size={12} className="text-slate-600" />
                    VOL: {Number(volume).toLocaleString('pt-BR', { notation: 'compact' })}
                </div>
                <div className="opacity-0 group-hover:opacity-100 transition-opacity text-cyan-400 font-bold tracking-wider text-[10px]">
                    IA ANALYZE →
                </div>
            </div>
        </div>
    );
}