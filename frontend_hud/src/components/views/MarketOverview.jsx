import React, { useState, useEffect } from 'react';
import { 
    TrendingUp, Activity, Globe, Zap, Anchor, DollarSign, 
    Layers, BrainCircuit, Scale, Crosshair, Calculator, ArrowRightLeft, 
    Moon, Sun, Briefcase
} from 'lucide-react';
import RealChart from '../RealChart'; 

// ==========================================
// CONFIGURAÇÃO DOS TEMAS (SKINS)
// ==========================================
const themes = {
    cyber: {
        id: 'cyber',
        bg: 'bg-[#0b0b0b]',
        cardBg: 'bg-[#0f0f0f]',
        borderColor: 'border-slate-800',
        textPrimary: 'text-white',
        textSecondary: 'text-slate-500',
        accent: 'text-cyan-400',
        accentBg: 'bg-cyan-950/30',
        accentBorder: 'border-cyan-500',
        chartBg: 'bg-[#0b0b0b]',
        fontHead: 'font-sans',
        fontMono: 'font-mono',
        shadow: 'shadow-lg shadow-cyan-900/10',
        radius: 'rounded-xl',
        button: 'bg-slate-800 text-cyan-400 hover:bg-slate-700',
        glow: true
    },
    corporate: {
        id: 'corporate',
        bg: 'bg-[#f0f2f5]', // Cinza Gelo (Papel)
        cardBg: 'bg-white', // Branco Puro
        borderColor: 'border-slate-200',
        textPrimary: 'text-slate-900', // Preto Suave
        textSecondary: 'text-slate-500',
        accent: 'text-blue-700', // Royal Blue
        accentBg: 'bg-blue-50',
        accentBorder: 'border-blue-600',
        chartBg: 'bg-white',
        fontHead: 'font-sans tracking-tight', // Mais sóbrio
        fontMono: 'font-mono text-slate-700',
        shadow: 'shadow-sm border-b-2 border-slate-200', // Estilo "Card Físico"
        radius: 'rounded-md', // Cantos mais retos (Sério)
        button: 'bg-white border border-slate-300 text-slate-700 hover:bg-slate-50 shadow-sm',
        glow: false
    }
};

// ==========================================
// SUB-COMPONENTES ADAPTATIVOS
// ==========================================

const ArbitrageEquation = ({ theme }) => (
    <div className={`${theme.cardBg} ${theme.borderColor} border ${theme.radius} p-2 h-full flex flex-col items-center justify-center relative overflow-hidden group ${theme.shadow}`}>
        <div className={`absolute top-2 left-2 text-[8px] ${theme.textSecondary} font-bold uppercase tracking-widest flex items-center gap-1`}>
            <Calculator size={8} /> FAIR VALUE MODEL
        </div>
        
        <div className="flex items-center gap-2 mb-2 mt-2">
             <div className="text-center">
                 <span className={`block text-2xl ${theme.fontMono} font-bold ${theme.id === 'cyber' ? 'text-cyan-400' : 'text-blue-800'}`}>P<span className="text-[10px]">local</span></span>
                 <span className={`text-[8px] ${theme.textSecondary}`}>B3 (BRL)</span>
             </div>
             <span className="text-slate-400 text-xl">=</span>
             <div className="text-center">
                 <span className={`block text-xl ${theme.fontMono} font-bold ${theme.id === 'cyber' ? 'text-purple-400' : 'text-indigo-700'}`}>P<span className="text-[10px]">adr</span></span>
                 <span className={`text-[8px] ${theme.textSecondary}`}>NYSE</span>
             </div>
             <span className="text-slate-400 text-sm">×</span>
             <div className="text-center">
                 <span className={`block text-xl ${theme.fontMono} font-bold ${theme.id === 'cyber' ? 'text-emerald-400' : 'text-emerald-700'}`}>FX</span>
                 <span className={`text-[8px] ${theme.textSecondary}`}>USD</span>
             </div>
             <span className="text-slate-400 text-sm">+</span>
             <div className="text-center">
                 <span className={`block text-xl ${theme.fontMono} font-bold ${theme.id === 'cyber' ? 'text-red-400' : 'text-rose-700'}`}>GAP</span>
                 <span className={`text-[8px] ${theme.textSecondary}`}>Spread</span>
             </div>
        </div>

        <div className={`${theme.id === 'cyber' ? 'bg-slate-900/50' : 'bg-slate-100'} px-3 py-1 rounded-full border ${theme.borderColor} flex items-center gap-2`}>
            <div className={`w-1.5 h-1.5 rounded-full ${theme.id === 'cyber' ? 'bg-emerald-500 animate-pulse' : 'bg-emerald-600'}`}></div>
            <span className={`text-[9px] ${theme.textSecondary} font-mono`}>ALGO: CALCULANDO</span>
        </div>
    </div>
);

const ArbitrageScatterPlot = ({ data, theme }) => {
    return (
        <div className={`${theme.cardBg} ${theme.borderColor} border ${theme.radius} p-3 h-full flex flex-col relative overflow-hidden ${theme.shadow}`}>
            <div className={`flex justify-between items-center mb-2 z-10 border-b ${theme.borderColor} pb-2`}>
                <span className={`text-[10px] font-bold ${theme.textSecondary} flex items-center gap-2`}>
                    <Crosshair size={12} className={theme.accent}/> DISPERSÃO DE GAP
                </span>
            </div>
            <div className={`flex-1 relative border-l border-b ${theme.borderColor} m-2`}>
                <div className={`absolute top-1/2 left-0 w-full h-[1px] ${theme.id === 'cyber' ? 'bg-slate-700' : 'bg-slate-300'} border-t border-dashed ${theme.id === 'cyber' ? 'border-slate-600' : 'border-slate-400'}`}></div>
                <span className="absolute -left-4 top-0 text-[8px] text-emerald-500 font-bold">Profit</span>
                <span className="absolute -left-4 bottom-0 text-[8px] text-red-500 font-bold">Risk</span>

                {data.map((item, i) => {
                    const spread = item.spread_pct || 0;
                    const isOpp = spread < -0.5 || spread > 0.5; 
                    const topPos = 50 - (spread * 20); 
                    const leftPos = 15 + (i * 15) + (Math.random() * 5);

                    return (
                        <div key={i} 
                             className={`absolute w-2.5 h-2.5 rounded-full border border-black/10 cursor-pointer hover:scale-150 transition-transform group 
                             ${isOpp 
                                ? (theme.id === 'cyber' ? 'bg-cyan-400 shadow-[0_0_8px_rgba(34,211,238,0.8)]' : 'bg-blue-600 shadow-sm') 
                                : (theme.id === 'cyber' ? 'bg-slate-600' : 'bg-slate-400')}`} 
                             style={{ top: `${Math.min(Math.max(topPos, 10), 90)}%`, left: `${leftPos}%` }}>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

const AIInsightPanel = ({ theme }) => {
    const report = {
        sentiment: "CAUTELA / DISTORÇÃO CAMBIAL",
        summary: "Modelo aponta spread em VALE3. ADR (VALE) cai -1.2% enquanto papel local sustenta alta. Correção provável.",
        drivers: [
            { asset: "VALE (NYSE)", impact: "-1.2%", detail: "Fluxo Vendedor" },
            { asset: "USD/BRL", impact: "0.0%", detail: "Estável" },
        ]
    };

    return (
        <div className={`${theme.cardBg} ${theme.borderColor} border ${theme.radius} p-3 flex flex-col h-full relative overflow-hidden ${theme.shadow}`}>
            <div className={`flex justify-between items-center mb-2 z-10 border-b ${theme.borderColor} pb-2`}>
                <div className="flex items-center gap-2">
                    <BrainCircuit size={14} className={theme.id === 'cyber' ? "text-purple-400" : "text-indigo-700"} />
                    <span className={`text-[10px] font-bold ${theme.textPrimary} tracking-wider`}>IFMD CORTEX AI</span>
                </div>
                <span className={`text-[8px] px-1.5 py-0.5 rounded border ${theme.id === 'cyber' ? 'bg-purple-900/20 text-purple-300 border-purple-800' : 'bg-indigo-50 text-indigo-800 border-indigo-200'}`}>v2.4</span>
            </div>
            <div className="flex-1 overflow-y-auto custom-scrollbar z-10">
                <div className={`border-l-2 ${theme.id === 'cyber' ? 'border-purple-500' : 'border-indigo-600'} pl-2 mb-3`}>
                    <span className={`text-[9px] font-bold uppercase block mb-1 ${theme.id === 'cyber' ? 'text-purple-400' : 'text-indigo-700'}`}>{report.sentiment}</span>
                    <p className={`text-[10px] ${theme.textPrimary} leading-relaxed text-justify`}>{report.summary}</p>
                </div>
                <div className="space-y-1">
                    {report.drivers.map((d, i) => (
                        <div key={i} className={`flex justify-between items-center text-[9px] p-1 rounded ${theme.id === 'cyber' ? 'bg-slate-900/30' : 'bg-slate-100'}`}>
                            <span className={`${theme.textSecondary} font-mono`}>{d.asset}</span>
                            <span className={`font-bold ${d.impact.includes('-') ? 'text-red-500' : 'text-emerald-600'}`}>{d.impact}</span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

const IndexWeightMonitor = ({ theme }) => {
    const weights = [
        { ticker: "VALE3", weight: 12.5, change: 1.2 },
        { ticker: "PETR4", weight: 11.2, change: -0.5 },
        { ticker: "ITUB4", weight: 6.8, change: 0.1 },
        { ticker: "ELET3", weight: 3.5, change: 2.1 }
    ];

    return (
        <div className={`${theme.cardBg} ${theme.borderColor} border ${theme.radius} p-3 h-full ${theme.shadow}`}>
            <div className={`flex justify-between items-center mb-2 border-b ${theme.borderColor} pb-2`}>
                 <span className={`text-[10px] font-bold ${theme.textSecondary} flex items-center gap-2`}>
                    <Scale size={12} /> IBOV WEIGHTS
                </span>
            </div>
            <div className="space-y-2">
                {weights.map((w, i) => (
                    <div key={i} className="flex items-center justify-between text-[10px]">
                        <div className="flex items-center gap-2">
                            <div className={`w-1.5 h-1.5 rounded-full ${w.change > 0 ? 'bg-emerald-500' : 'bg-red-500'}`}></div>
                            <span className={`font-bold ${theme.textPrimary}`}>{w.ticker}</span>
                        </div>
                        <div className={`flex-1 mx-2 h-1.5 rounded-full overflow-hidden ${theme.id === 'cyber' ? 'bg-slate-800' : 'bg-slate-200'}`}>
                            <div className={`h-full ${w.change > 0 ? 'bg-emerald-500' : 'bg-red-500'}`} style={{ width: `${w.weight * 3}%` }} />
                        </div>
                        <span className={`${theme.fontMono} ${theme.textSecondary}`}>{w.weight}%</span>
                    </div>
                ))}
            </div>
        </div>
    );
};

const MountainDOM = ({ ticker, theme }) => {
    return (
        <div className={`${theme.cardBg} ${theme.borderColor} border ${theme.radius} p-3 h-full flex flex-col relative overflow-hidden ${theme.shadow}`}>
            <div className="flex justify-between items-center mb-1 z-10">
                <span className={`text-[10px] font-bold ${theme.textSecondary} flex items-center gap-2`}>
                    <Layers size={10} /> DEPTH (DOM)
                </span>
                <span className={`text-[10px] font-mono ${theme.accent}`}>{ticker}</span>
            </div>
            <div className="flex-1 flex items-end justify-center relative mt-1">
                <div className={`w-1/2 h-full flex items-end relative border-r ${theme.borderColor}`}>
                    <svg viewBox="0 0 100 100" className="w-full h-full preserve-3d">
                        <path d="M0,100 L0,40 Q50,60 100,20 L100,100 Z" fill={theme.id === 'cyber' ? 'url(#gradGreenCy)' : 'url(#gradGreenCo)'} opacity="0.6" />
                        <defs>
                            <linearGradient id="gradGreenCy" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#10b981" stopOpacity="0.5"/><stop offset="1" stopColor="#10b981" stopOpacity="0.1"/></linearGradient>
                            <linearGradient id="gradGreenCo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#059669" stopOpacity="0.4"/><stop offset="1" stopColor="#059669" stopOpacity="0.05"/></linearGradient>
                        </defs>
                    </svg>
                    <span className="absolute bottom-1 left-1 text-[8px] text-emerald-600 font-bold">BID 45K</span>
                </div>
                <div className="w-1/2 h-full flex items-end relative">
                    <svg viewBox="0 0 100 100" className="w-full h-full transform scale-x-[-1]">
                        <path d="M0,100 L0,50 Q40,70 100,30 L100,100 Z" fill={theme.id === 'cyber' ? 'url(#gradRedCy)' : 'url(#gradRedCo)'} opacity="0.6" />
                        <defs>
                            <linearGradient id="gradRedCy" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#ef4444" stopOpacity="0.5"/><stop offset="1" stopColor="#ef4444" stopOpacity="0.1"/></linearGradient>
                            <linearGradient id="gradRedCo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#dc2626" stopOpacity="0.4"/><stop offset="1" stopColor="#dc2626" stopOpacity="0.05"/></linearGradient>
                        </defs>
                    </svg>
                    <span className="absolute bottom-1 right-1 text-[8px] text-red-600 font-bold">ASK 38K</span>
                </div>
            </div>
        </div>
    );
};

const ArbitrageMatrixCard = ({ data, isSimulated, theme }) => {
    const displayData = isSimulated ? {
        asset: data.asset || "PBR/PETR4",
        spread_pct: data.spread_pct || -0.85,
        status: data.status || "OPORTUNIDADE",
        price: data.price || 14.32
    } : data;

    const isOpportunity = Math.abs(displayData.spread_pct) > 0.5;

    // Lógica de Cores Condicional ao Tema e Status
    const cardStyle = isOpportunity 
        ? (theme.id === 'cyber' ? 'bg-cyan-950/20 border-cyan-500/50' : 'bg-blue-50 border-blue-200 shadow-sm')
        : `${theme.cardBg} ${theme.borderColor}`;

    const accentColor = isOpportunity
        ? (theme.id === 'cyber' ? 'text-cyan-400' : 'text-blue-800')
        : theme.textSecondary;

    return (
        <div className={`relative p-2 rounded-lg border flex flex-col justify-between overflow-hidden transition-all h-full ${cardStyle}`}>
            {isOpportunity && theme.glow && <div className="absolute top-0 right-0 w-12 h-12 bg-cyan-500/10 rounded-full blur-xl -mr-5 -mt-5"></div>}
            
            <div className="flex justify-between items-start z-10 mb-1">
                <h4 className={`text-[10px] font-bold uppercase tracking-wider flex items-center gap-1 ${accentColor}`}>
                    <ArrowRightLeft size={10} /> {displayData.asset}
                </h4>
                <div className={`text-right ${displayData.spread_pct > 0 ? 'text-red-500' : 'text-emerald-600'}`}>
                    <div className="text-[11px] font-mono font-bold">{displayData.spread_pct > 0 ? '+' : ''}{displayData.spread_pct}%</div>
                </div>
            </div>
            
            <div className="flex justify-between items-center z-10 mt-auto">
                 <div className={`text-sm font-mono leading-none ${theme.textPrimary}`}>
                    {typeof displayData.price === 'number' ? displayData.price.toFixed(2) : displayData.price}
                 </div>
                 <span className={`text-[8px] px-1.5 py-0.5 rounded font-bold uppercase 
                    ${isOpportunity 
                        ? (theme.id === 'cyber' ? 'bg-cyan-500 text-black' : 'bg-blue-600 text-white') 
                        : (theme.id === 'cyber' ? 'bg-slate-800 text-slate-500' : 'bg-slate-200 text-slate-500')}`}>
                    {isOpportunity ? 'DETECTADO' : 'NEUTRO'}
                 </span>
            </div>
        </div>
    );
};

const AssetContainer = ({ title, icon, list, onSelect, currentSelected, theme }) => (
    <div className={`${theme.cardBg} ${theme.borderColor} border ${theme.radius} p-2 flex flex-col h-40 ${theme.shadow}`}>
        <div className={`flex items-center gap-2 px-1 border-b ${theme.borderColor} pb-2 mb-2`}>
            <div className={`p-1 rounded ${theme.id === 'cyber' ? 'bg-slate-900 text-cyan-500' : 'bg-slate-100 text-blue-700'}`}>{icon}</div>
            <h3 className={`text-[10px] font-bold uppercase tracking-wider ${theme.textSecondary}`}>{title}</h3>
        </div>
        <div className="grid grid-cols-2 gap-2 overflow-y-auto custom-scrollbar pr-1">
            {list.slice(0, 10).map((asset, i) => (
                <div 
                    key={i} 
                    onClick={() => onSelect(asset.ticker)}
                    className={`border p-1.5 rounded cursor-pointer transition-all group relative
                        ${currentSelected === asset.ticker 
                            ? (theme.id === 'cyber' ? 'border-cyan-500 bg-slate-900' : 'border-blue-500 bg-blue-50') 
                            : (theme.id === 'cyber' ? 'border-slate-800/60 hover:bg-slate-800' : 'border-slate-100 bg-slate-50 hover:bg-white hover:shadow-sm')}
                    `}
                >
                    <div className="flex justify-between items-center">
                        <span className={`font-bold text-[9px] ${theme.id === 'cyber' ? 'text-slate-300 group-hover:text-cyan-400' : 'text-slate-700 group-hover:text-blue-700'}`}>{asset.ticker}</span>
                        <span className={`text-[9px] font-mono ${asset.change >= 0 ? 'text-emerald-600' : 'text-red-500'}`}>
                            {asset.change > 0 ? '+' : ''}{asset.change}%
                        </span>
                    </div>
                </div>
            ))}
        </div>
    </div>
);

// ==========================================
// 8. COMPONENTE PRINCIPAL (COM THEME STATE)
// ==========================================
export default function MarketOverview() {
    // State para dados
    const [assets, setAssets] = useState([]);
    const [arbitrage, setArbitrage] = useState([]);
    const [selectedAsset, setSelectedAsset] = useState('PETR4');
    const [chartData, setChartData] = useState([]);
    const [lastUpdate, setLastUpdate] = useState(new Date());
    
    // State para TEMA
    const [currentThemeId, setCurrentThemeId] = useState('cyber'); // 'cyber' ou 'corporate'
    const theme = themes[currentThemeId]; // Atalho para o tema atual

    const toggleTheme = () => {
        setCurrentThemeId(prev => prev === 'cyber' ? 'corporate' : 'cyber');
    };

    const fetchAll = async () => {
        try {
            const resMkt = await fetch('http://localhost:8000/market/all');
            const dataMkt = await resMkt.json();
            const cleanMkt = Array.isArray(dataMkt) ? dataMkt : (dataMkt.data || []);
            setAssets(cleanMkt);
            // Simulação de dados se falhar
            if(cleanMkt.length === 0) setAssets([
                {ticker: 'PETR4', price: 38.50, change: 1.2},
                {ticker: 'VALE3', price: 62.10, change: -0.5},
                {ticker: 'ITUB4', price: 32.40, change: 0.8},
                {ticker: 'WIN', price: 128500, change: 0.2},
                {ticker: 'WDO', price: 5.15, change: -0.1},
            ]);

            const resArb = await fetch('http://localhost:8000/market/arbitrage');
            const dataArb = await resArb.json();
            const cleanArb = Array.isArray(dataArb) ? dataArb : [];
            setArbitrage(cleanArb);

            setLastUpdate(new Date());
        } catch (e) { console.error("Erro fetch overview:", e); }
    };

    const fetchChart = async () => {
        try {
            const res = await fetch(`http://localhost:8000/market/history/${selectedAsset}`);
            const data = await res.json();
            if(Array.isArray(data)) setChartData(data);
        } catch (e) { console.error("Erro chart:", e); }
    };

    useEffect(() => {
        fetchAll();
        const interval = setInterval(fetchAll, 3000); 
        return () => clearInterval(interval);
    }, []);

    useEffect(() => {
        fetchChart();
    }, [selectedAsset]);

    const arbData = arbitrage.length > 0 ? arbitrage : [
        {asset: "PBR/PETR4", price: 14.32, spread_pct: -0.85, status: "OPORTUNIDADE"},
        {asset: "VALE/VALE3", price: 11.50, spread_pct: -1.2, status: "OPORTUNIDADE"},
        {asset: "EWZ/IBOV", price: 29.10, spread_pct: 0.12, status: "NEUTRO"},
        {asset: "WDO/DOL", price: 5.15, spread_pct: -0.1, status: "NEUTRO"},
        {asset: "DI/US10Y", price: 104.2, spread_pct: 0.05, status: "NEUTRO"},
        {asset: "BTC/FUT", price: 65000, spread_pct: 0.3, status: "NEUTRO"},
    ];

    const filterBy = (list, terms) => list.filter(a => terms.some(t => a.ticker.includes(t)));
    const indices = filterBy(assets, ['WIN', 'IND', 'IBOV', 'ES', 'NDX', 'DXY']);
    const commodities = filterBy(assets, ['WDO', 'DOL', 'CL', 'XAU', 'SOY', 'BTC', 'ETH']);
    const b3_stocks = filterBy(assets, ['PETR', 'VALE', 'ITUB', 'BBDC', 'WEGE', 'PRIO']).filter(a => !a.ticker.includes('PBR'));
    const nyse_stocks = filterBy(assets, ['AAPL', 'MSFT', 'PBR', 'VALE3', 'TSLA', 'NVDA']);

    return (
        <div className={`animate-fadeIn space-y-4 pb-20 p-4 transition-colors duration-500 ${theme.bg} min-h-screen`}>
            
            {/* CABEÇALHO COM SELETOR DE SKIN */}
            <div className={`flex justify-between items-end border-b ${theme.borderColor} pb-2 px-1`}>
                <div>
                    <h1 className={`text-xl font-black tracking-tighter flex items-center gap-2 ${theme.textPrimary}`}>
                        MARKET <span className={theme.accent}>OVERVIEW</span>
                        {currentThemeId === 'corporate' && <Briefcase size={16} className="text-slate-400" />}
                    </h1>
                    <p className={`text-[10px] font-mono ${theme.textSecondary}`}>
                        INTELLIGENCE FLOW • {currentThemeId === 'cyber' ? 'DEEP RESEARCH ENGINE' : 'INSTITUTIONAL TERMINAL'}
                    </p>
                </div>
                <div className="text-right flex items-center gap-3">
                     {/* Botão de Skin */}
                     <button 
                        onClick={toggleTheme}
                        className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-[10px] font-bold transition-all ${theme.button}`}
                     >
                        {currentThemeId === 'cyber' ? <Sun size={12}/> : <Moon size={12}/>}
                        {currentThemeId === 'cyber' ? 'MODO CORPORATIVO' : 'MODO CYBER'}
                     </button>

                     <div className="text-right">
                         <div className={`flex items-center gap-2 text-[9px] font-bold px-2 py-1 rounded border mb-1 ${theme.accentBg} ${theme.accent} ${theme.accentBorder}`}>
                            <Zap size={8} fill="currentColor" /> DMA: ON
                         </div>
                         <span className={`text-[9px] font-mono ${theme.textSecondary}`}>{lastUpdate.toLocaleTimeString()}</span>
                     </div>
                </div>
            </div>

            {/* SEÇÃO 1: CONTAINERS DE ATIVOS */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <AssetContainer title="MACRO & ÍNDICES" icon={<Globe size={14}/>} list={indices} onSelect={setSelectedAsset} currentSelected={selectedAsset} theme={theme}/>
                <AssetContainer title="COMMODITIES & FX" icon={<Anchor size={14}/>} list={commodities} onSelect={setSelectedAsset} currentSelected={selectedAsset} theme={theme}/>
                <AssetContainer title="EQUITY B3 (BRASIL)" icon={<TrendingUp size={14}/>} list={b3_stocks} onSelect={setSelectedAsset} currentSelected={selectedAsset} theme={theme}/>
                <AssetContainer title="NYSE & ADRs" icon={<DollarSign size={14}/>} list={nyse_stocks} onSelect={setSelectedAsset} currentSelected={selectedAsset} theme={theme}/>
            </div>

            {/* SEÇÃO 2: CENTRO DE COMANDO */}
            <div className="grid grid-cols-12 gap-4 h-[500px]">
                {/* GRÁFICO */}
                <div className={`col-span-12 lg:col-span-9 ${theme.cardBg} border ${theme.borderColor} ${theme.radius} p-1 relative ${theme.shadow} flex flex-col`}>
                    <div className={`absolute top-2 left-2 z-20 flex items-center gap-2 px-2 py-1 rounded backdrop-blur-sm border ${theme.id === 'cyber' ? 'bg-slate-900/80 border-slate-700' : 'bg-white/90 border-slate-200'}`}>
                        <span className={`font-bold text-sm ${theme.textPrimary}`}>{selectedAsset}</span>
                        <span className={`text-[9px] ${theme.accent}`}>M5 • SMC</span>
                    </div>
                    {/* Passamos o tema para o gráfico se ele suportar, ou apenas container */}
                    <div className="flex-1 w-full h-full rounded overflow-hidden">
                         <RealChart data={chartData} ticker={selectedAsset} isDark={currentThemeId === 'cyber'} />
                    </div>
                </div>

                {/* PAINEL DE INTELIGÊNCIA */}
                <div className="col-span-12 lg:col-span-3 flex flex-col gap-3 h-full">
                    <div className="h-1/3"><MountainDOM ticker={selectedAsset} theme={theme} /></div>
                    <div className="h-1/3"><IndexWeightMonitor theme={theme} /></div>
                    <div className="h-1/3"><AIInsightPanel theme={theme} /></div>
                </div>
            </div>

            {/* SEÇÃO 3: LABORATÓRIO DE ARBITRAGEM */}
            <div className={`${theme.cardBg} border ${theme.borderColor} ${theme.radius} p-3 ${theme.shadow}`}>
                <div className={`flex items-center gap-2 mb-3 border-b ${theme.borderColor} pb-2`}>
                    <Activity size={16} className={theme.accent} />
                    <h3 className={`text-xs font-bold uppercase tracking-widest ${theme.textPrimary}`}>ARBITRAGE LAB (RISCO x RETORNO)</h3>
                </div>
                
                <div className="grid grid-cols-12 gap-4 h-48">
                    <div className="col-span-12 md:col-span-5 grid grid-cols-2 gap-2 overflow-y-auto custom-scrollbar pr-2">
                        {arbData.map((arb, i) => (
                            <ArbitrageMatrixCard key={i} data={arb} isSimulated={arbitrage.length === 0} theme={theme} />
                        ))}
                    </div>

                    <div className="col-span-12 md:col-span-3">
                        <ArbitrageEquation theme={theme} />
                    </div>

                    <div className="col-span-12 md:col-span-4">
                        <ArbitrageScatterPlot data={arbData} theme={theme} />
                    </div>
                </div>
            </div>

        </div>
    );
}