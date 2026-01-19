import React, { useState, useEffect } from 'react';
import { RefreshCcw, Wifi, AlertTriangle } from 'lucide-react';
import RealChart from '../RealChart';

export default function TechAnalysisView() {
    const [selectedTicker, setSelectedTicker] = useState('PETR4');
    const [chartData, setChartData] = useState([]); // Inicia sempre como array vazio []
    const [arbitrageData, setArbitrageData] = useState([]);
    const [errorMsg, setErrorMsg] = useState(null);

    const refreshData = async () => {
        setErrorMsg(null);
        try {
            // 1. Tenta buscar Histórico
            const histRes = await fetch(`http://localhost:8000/market/history/${selectedTicker}`);
            if (!histRes.ok) throw new Error(`Erro API Histórico: ${histRes.status}`);
            
            const histData = await histRes.json();
            
            // Verifica se é array antes de setar
            if (Array.isArray(histData)) {
                setChartData(histData);
            } else {
                console.warn("API retornou dados inválidos (não é lista):", histData);
                setChartData([]);
            }

            // 2. Tenta buscar Arbitragem
            const arbRes = await fetch('http://localhost:8000/market/arbitrage');
            if (arbRes.ok) {
                const arbData = await arbRes.json();
                if (Array.isArray(arbData)) setArbitrageData(arbData);
            }

        } catch (e) {
            console.error("Falha no refresh:", e);
            setErrorMsg("Falha de conexão com Backend.");
        }
    };

    useEffect(() => {
        refreshData();
        const interval = setInterval(refreshData, 5000);
        return () => clearInterval(interval);
    }, [selectedTicker]);

    return (
        <div className="space-y-6 animate-fadeIn pb-10">
            {/* MENSAGEM DE ERRO (SE HOUVER) */}
            {errorMsg && (
                <div className="bg-red-900/20 border border-red-900/50 p-3 rounded text-red-400 text-sm flex items-center gap-2">
                    <AlertTriangle size={16}/> {errorMsg}
                </div>
            )}

            {/* CARDS ARBITRAGEM */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {arbitrageData.length === 0 && !errorMsg && (
                     <div className="p-4 border border-dashed border-slate-800 rounded-xl text-slate-500 text-sm flex items-center gap-2">
                        <Wifi size={16} className="animate-pulse"/> Sincronizando paridade...
                     </div>
                )}
                {arbitrageData.map((item, idx) => (
                    <div key={idx} className="bg-[#0f0f0f] border border-slate-800 p-4 rounded-xl flex justify-between items-center shadow-lg">
                        <div>
                            <div className="flex items-center gap-2">
                                <h3 className="font-bold text-white">{item.asset}</h3>
                                <span className={`text-[10px] px-2 py-0.5 rounded font-bold ${item.spread_pct > 0 ? 'bg-red-900/30 text-red-400' : 'bg-emerald-900/30 text-emerald-400'}`}>
                                    {item.status}
                                </span>
                            </div>
                        </div>
                        <div className="text-right">
                            <span className={`text-2xl font-black ${item.spread_pct > 0 ? 'text-red-400' : 'text-emerald-400'}`}>
                                {item.spread_pct > 0 ? '+' : ''}{item.spread_pct}%
                            </span>
                        </div>
                    </div>
                ))}
            </div>

            {/* GRÁFICO */}
            <div className="bg-[#0f0f0f] border border-slate-800 rounded-xl p-1 shadow-2xl">
                <div className="flex gap-2 p-2 border-b border-slate-800/50">
                    {['PETR4', 'VALE3', 'ITUB4'].map(t => (
                        <button key={t} onClick={() => setSelectedTicker(t)}
                            className={`px-4 py-1 rounded text-xs font-bold transition-all ${selectedTicker === t ? 'bg-cyan-600 text-white' : 'text-slate-500 hover:text-white'}`}>
                            {t}
                        </button>
                    ))}
                    <div className="flex-1"/>
                    <button onClick={refreshData} className="text-slate-500 hover:text-white"><RefreshCcw size={14}/></button>
                </div>
                
                <RealChart data={chartData} ticker={selectedTicker} />
            </div>
        </div>
    );
}