import React from 'react';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis } from 'recharts';
import { Wallet, ShieldAlert, TrendingUp, TrendingDown, Activity, Layers } from 'lucide-react';

export default function PortfolioView() {
    // --- DADOS MOCKADOS (Futuramente virão da API) ---
    const allocationData = [
        { name: 'Ações BR', value: 45000, color: '#06b6d4' }, // Cyan-500
        { name: 'FIIs', value: 25000, color: '#8b5cf6' },     // Violet-500
        { name: 'Forex (USD)', value: 15000, color: '#10b981' }, // Emerald-500
        { name: 'Crypto', value: 10000, color: '#f59e0b' },  // Amber-500
    ];

    const riskData = [
        { subject: 'Volatilidade', A: 80, fullMark: 100 },
        { subject: 'Liquidez', A: 90, fullMark: 100 },
        { subject: 'Correlação', A: 40, fullMark: 100 },
        { subject: 'Yield', A: 60, fullMark: 100 },
        { subject: 'Hedge', A: 30, fullMark: 100 },
    ];

    const assets = [
        { ticker: 'PETR4', type: 'Stock', side: 'LONG', profit: 12.5, flow: 'Bullish' },
        { ticker: 'VALE3', type: 'Stock', side: 'LONG', profit: -3.2, flow: 'Bearish' },
        { ticker: 'EURUSD', type: 'Forex', side: 'SHORT', profit: 5.8, flow: 'Neutral' },
        { ticker: 'XAUUSD', type: 'Cmdty', side: 'LONG', profit: 1.2, flow: 'Bullish' },
    ];

    // Formata valor em BRL
    const formatCurrency = (value) => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value);

    return (
        <div className="space-y-6 animate-fade-in pb-20">
            {/* CABEÇALHO */}
            <div className="flex flex-col md:flex-row justify-between items-end border-b border-slate-800 pb-4">
                <div>
                    <h2 className="text-3xl font-black text-white flex items-center gap-3">
                        <Wallet className="text-cyan-400" /> SMART PORTFOLIO
                    </h2>
                    <p className="text-slate-500 font-mono text-xs mt-1">ANÁLISE DE RISCO E EFICIÊNCIA</p>
                </div>
                <div className="text-right">
                    <p className="text-xs text-slate-400">NET WORTH ESTIMADO</p>
                    <p className="text-3xl font-mono font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-400">
                        R$ 95.000,00
                    </p>
                </div>
            </div>

            {/* GRÁFICOS SUPERIORES */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                
                {/* 1. Alocação (Donut Chart) */}
                <div className="bg-[#0f0f0f] border border-slate-800 rounded-xl p-6 relative overflow-hidden group hover:border-cyan-500/30 transition-colors">
                    <h3 className="text-slate-300 font-bold text-sm mb-4 flex items-center gap-2">
                        <Layers size={16} className="text-cyan-400"/> ALOCAÇÃO POR CLASSE
                    </h3>
                    <div className="h-56 w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie 
                                    data={allocationData} 
                                    innerRadius={60} 
                                    outerRadius={80} 
                                    paddingAngle={5} 
                                    dataKey="value"
                                    stroke="none"
                                >
                                    {allocationData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={entry.color} />
                                    ))}
                                </Pie>
                                <Tooltip 
                                    contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', color: '#fff' }} 
                                    itemStyle={{ color: '#fff' }}
                                    formatter={(value) => formatCurrency(value)}
                                />
                            </PieChart>
                        </ResponsiveContainer>
                        {/* Texto Central */}
                        <div className="absolute inset-0 flex items-center justify-center pointer-events-none mt-8">
                            <span className="text-slate-500 text-xs font-mono">DIVERSIFICAÇÃO</span>
                        </div>
                    </div>
                </div>

                {/* 2. Radar de Risco (Spider Chart) */}
                <div className="bg-[#0f0f0f] border border-slate-800 rounded-xl p-6 hover:border-purple-500/30 transition-colors">
                    <h3 className="text-slate-300 font-bold text-sm mb-2 flex items-center gap-2">
                        <Activity size={16} className="text-purple-400"/> MATRIZ DE RISCO
                    </h3>
                    <div className="h-60 w-full text-xs">
                        <ResponsiveContainer width="100%" height="100%">
                            <RadarChart cx="50%" cy="50%" outerRadius="70%" data={riskData}>
                                <PolarGrid stroke="#334155" />
                                <PolarAngleAxis dataKey="subject" tick={{ fill: '#94a3b8', fontSize: 10 }} />
                                <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                                <Radar name="Carteira" dataKey="A" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={0.3} />
                                <Tooltip />
                            </RadarChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* 3. Sugestão de IA (Hedge) */}
                <div className="bg-[#0f0f0f] border border-slate-800 rounded-xl p-6 flex flex-col justify-between relative overflow-hidden">
                    <div className="absolute top-0 right-0 p-2 bg-yellow-500/10 text-yellow-500 text-[10px] font-bold border-l border-b border-yellow-500/20 rounded-bl-lg">
                        AI INSIGHT
                    </div>
                    
                    <div>
                        <h3 className="text-slate-300 font-bold text-sm mb-4 flex items-center gap-2">
                            <ShieldAlert size={16} className="text-yellow-400"/> ALERTA DE HEDGE
                        </h3>
                        <p className="text-slate-400 text-sm leading-relaxed">
                            Detectada alta correlação entre <span className="text-white font-bold">PETR4</span> e <span className="text-white font-bold">IBOV</span>. 
                            Sua proteção em Dólar está abaixo do ideal para o cenário macro atual.
                        </p>
                    </div>

                    <div className="mt-6 p-4 bg-slate-800/50 rounded border-l-2 border-cyan-500">
                        <p className="text-xs text-cyan-300 font-mono mb-1">SUGESTÃO TÁTICA:</p>
                        <p className="text-sm text-white font-bold">Aumentar posição em USD ou Short em EWZ.</p>
                    </div>
                </div>
            </div>

            {/* TABELA DE POSIÇÕES COM FLUXO */}
            <div className="bg-[#0f0f0f] border border-slate-800 rounded-xl overflow-hidden">
                <div className="p-4 border-b border-slate-800 bg-slate-900/30 flex justify-between items-center">
                    <h3 className="font-bold text-slate-200">POSIÇÕES ABERTAS</h3>
                    <span className="text-[10px] text-cyan-500 font-mono border border-cyan-900 px-2 py-1 rounded bg-cyan-950/20 animate-pulse">
                        LIVE TRACKING
                    </span>
                </div>
                
                <div className="overflow-x-auto">
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr className="text-xs text-slate-500 border-b border-slate-800 bg-slate-900/20">
                                <th className="p-4 font-normal">ATIVO</th>
                                <th className="p-4 font-normal">TIPO</th>
                                <th className="p-4 font-normal">LADO</th>
                                <th className="p-4 font-normal text-right">PNL %</th>
                                <th className="p-4 font-normal text-right">INST. FLOW</th>
                            </tr>
                        </thead>
                        <tbody className="text-sm">
                            {assets.map((asset, i) => (
                                <tr key={i} className="border-b border-slate-800/50 hover:bg-slate-800/30 transition-colors">
                                    <td className="p-4 font-bold text-white">{asset.ticker}</td>
                                    <td className="p-4 text-slate-400">{asset.type}</td>
                                    <td className={`p-4 font-mono font-bold ${asset.side === 'LONG' ? 'text-emerald-400' : 'text-red-400'}`}>
                                        {asset.side}
                                    </td>
                                    <td className={`p-4 text-right font-bold ${asset.profit >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                                        {asset.profit > 0 ? '+' : ''}{asset.profit}%
                                    </td>
                                    <td className="p-4 text-right">
                                        <span className={`px-2 py-1 rounded text-[10px] font-bold uppercase ${
                                            asset.flow === 'Bullish' ? 'bg-emerald-900/30 text-emerald-400 border border-emerald-800' :
                                            asset.flow === 'Bearish' ? 'bg-red-900/30 text-red-400 border border-red-800' :
                                            'bg-slate-700/30 text-slate-400'
                                        }`}>
                                            {asset.flow}
                                        </span>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}