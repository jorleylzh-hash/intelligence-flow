import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { X, RefreshCcw, Network, BrainCircuit } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from 'recharts';

export default function AnalysisHub({ asset, onClose }) {
    if (!asset) return null;

    const [insight, setInsight] = useState("");
    const [chartExplanation, setChartExplanation] = useState(""); // NOVA VARIÁVEL
    const [chartData, setChartData] = useState([]);
    const [drivers, setDrivers] = useState([]);
    const [loading, setLoading] = useState(false);
    const [activeTab, setActiveTab] = useState('ia');
    const hasCalledAPI = useRef(false);

    const lineColors = ["#22d3ee", "#facc15", "#f87171", "#a3e635"];

    useEffect(() => {
        const loadData = async () => {
            if (hasCalledAPI.current) return;
            hasCalledAPI.current = true;
            setLoading(true);

            try {
                const response = await axios.post('http://127.0.0.1:8000/market/study', {
                    ticker: asset.ticker,
                    price: asset.price
                });

                if (response.data) {
                    setInsight(response.data.study || "Sem análise disponível.");
                    // CAPTURA A EXPLICAÇÃO DO GRÁFICO
                    setChartExplanation(response.data.chart_explanation || "Correlação padrão.");
                    setChartData(Array.isArray(response.data.chart_data) ? response.data.chart_data : []);
                    setDrivers(Array.isArray(response.data.drivers) ? response.data.drivers : []);
                }
            } catch (error) {
                console.error("Erro IA:", error);
                setInsight("Erro de conexão: " + error.message);
            } finally {
                setLoading(false);
            }
        };
        loadData();
    }, [asset]);

    return (
        <div style={{ zIndex: 9999 }} className="fixed inset-0 bg-black/95 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-[#0f172a] border border-slate-700 w-full max-w-5xl rounded-xl shadow-2xl flex flex-col h-[85vh]">
                
                {/* HEADER */}
                <div className="p-4 border-b border-slate-800 flex justify-between items-center bg-slate-900/50">
                    <h2 className="font-bold text-white text-xl flex items-center gap-2">
                        {asset.ticker} <span className="text-slate-500 text-sm border border-slate-700 px-2 rounded">M5 AI</span>
                    </h2>
                    
                    <div className="flex bg-black/40 rounded-lg p-1 border border-slate-800">
                        <button onClick={() => setActiveTab('ia')} className={`px-4 py-1 rounded text-xs font-bold ${activeTab === 'ia' ? 'bg-cyan-600 text-white' : 'text-slate-400'}`}>ESTUDO TÉCNICO</button>
                        <button onClick={() => setActiveTab('chart')} className={`px-4 py-1 rounded text-xs font-bold ${activeTab === 'chart' ? 'bg-yellow-600 text-white' : 'text-slate-400'}`}>FORÇA RELATIVA</button>
                    </div>

                    <button onClick={onClose} className="text-slate-400 hover:text-red-400 p-2"><X size={24} /></button>
                </div>

                {/* CONTEÚDO */}
                <div className="flex-1 p-6 overflow-hidden bg-[#0b1120]">
                    {loading ? (
                        <div className="flex flex-col items-center justify-center h-full text-cyan-500 gap-4">
                            <RefreshCcw className="animate-spin" size={40} />
                            <span className="text-sm font-bold uppercase tracking-widest animate-pulse">Processando Inteligência...</span>
                        </div>
                    ) : (
                        <>
                            {/* ABA 1: ANÁLISE ESCRITA */}
                            {activeTab === 'ia' && (
                                <div className="h-full overflow-y-auto">
                                    <div className="p-4 bg-slate-900/50 border border-slate-800 rounded-lg mb-4">
                                        <div className="flex items-center gap-2 text-cyan-400 mb-2">
                                            <BrainCircuit size={18} />
                                            <span className="font-bold text-sm uppercase">Institutional Insight</span>
                                        </div>
                                        <pre className="whitespace-pre-wrap font-sans text-sm text-slate-300 leading-relaxed">{insight}</pre>
                                    </div>
                                </div>
                            )}

                            {/* ABA 2: GRÁFICO + EXPLICAÇÃO (O QUE FALTAVA) */}
                            {activeTab === 'chart' && (
                                <div className="h-full w-full flex flex-col">
                                    {/* --- AQUI ESTÁ O TEXTO QUE FALTAVA --- */}
                                    <div className="mb-4 p-3 bg-yellow-500/10 border border-yellow-500/20 rounded-lg flex items-start gap-3">
                                        <Network className="text-yellow-500 mt-1" size={20} />
                                        <div>
                                            <h4 className="text-yellow-500 text-xs font-bold uppercase tracking-wider mb-1">Racional da Correlação</h4>
                                            <p className="text-slate-300 text-sm">{chartExplanation}</p>
                                        </div>
                                    </div>

                                    <div className="flex-1 min-h-0 border border-slate-800 rounded-lg bg-slate-900/30 p-2">
                                        {chartData.length > 0 ? (
                                            <ResponsiveContainer width="100%" height="100%">
                                                <LineChart data={chartData}>
                                                    <XAxis dataKey="time" stroke="#475569" fontSize={10} tick={{fill: '#475569'}} />
                                                    <YAxis stroke="#475569" fontSize={10} domain={['auto', 'auto']} tick={{fill: '#475569'}} />
                                                    <Tooltip 
                                                        contentStyle={{backgroundColor: '#0f172a', borderColor: '#334155', color: '#f8fafc'}} 
                                                        itemStyle={{fontSize: '12px'}}
                                                    />
                                                    <Legend wrapperStyle={{paddingTop: '10px'}}/>
                                                    
                                                    {/* Ativo Principal (Linha Grossa) */}
                                                    <Line type="monotone" dataKey={asset.ticker} stroke="#22d3ee" strokeWidth={3} dot={false} activeDot={{r: 6}} />
                                                    
                                                    {/* Drivers (Linhas Finas) */}
                                                    {drivers.map((d, i) => (
                                                        <Line key={d} type="monotone" dataKey={d} stroke={lineColors[i+1] || "#888"} strokeWidth={1.5} dot={false} strokeDasharray="4 4" />
                                                    ))}
                                                </LineChart>
                                            </ResponsiveContainer>
                                        ) : (
                                            <div className="text-center text-slate-500 mt-20">
                                                Dados insuficientes para correlação intraday.
                                            </div>
                                        )}
                                    </div>
                                </div>
                            )}
                        </>
                    )}
                </div>
            </div>
        </div>
    );
}