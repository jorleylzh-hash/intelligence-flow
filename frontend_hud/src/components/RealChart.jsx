import React, { useEffect, useRef } from 'react';
import { createChart, ColorType } from 'lightweight-charts';

export default function RealChart({ data, ticker, isDark = true }) {
    const chartContainerRef = useRef(null);
    const chartRef = useRef(null);

    // Definição das Paletas (Mantivemos as cores corporativas vs cyber)
    const themes = {
        cyber: {
            backgroundColor: '#0b0b0b',
            textColor: '#94a3b8',
            gridColor: '#1e293b',
            upColor: '#10b981',
            downColor: '#ef4444',
            wickUp: '#10b981',
            wickDown: '#ef4444',
            priceLine: '#22d3ee'
        },
        corporate: {
            backgroundColor: '#ffffff',
            textColor: '#334155',
            gridColor: '#e2e8f0',
            upColor: '#059669', // Verde Sóbrio
            downColor: '#dc2626', // Vermelho Sóbrio
            wickUp: '#059669',
            wickDown: '#dc2626',
            priceLine: '#2563eb'
        }
    };

    const currentTheme = isDark ? themes.cyber : themes.corporate;

    useEffect(() => {
        if (!chartContainerRef.current) return;

        // 1. Cria o Gráfico
        const chart = createChart(chartContainerRef.current, {
            layout: {
                background: { type: ColorType.Solid, color: currentTheme.backgroundColor },
                textColor: currentTheme.textColor,
                fontFamily: "'Roboto Mono', monospace",
            },
            grid: {
                vertLines: { color: currentTheme.gridColor },
                horzLines: { color: currentTheme.gridColor },
            },
            width: chartContainerRef.current.clientWidth || 600, // Fallback de largura
            height: chartContainerRef.current.clientHeight || 300, // Fallback de altura
            timeScale: {
                borderColor: currentTheme.gridColor,
                timeVisible: true,
                secondsVisible: false,
            },
            rightPriceScale: {
                borderColor: currentTheme.gridColor,
                autoScale: true, // Garante que o preço se ajuste verticalmente
            },
        });

        // 2. Adiciona a Série de Candles
        const newSeries = chart.addCandlestickSeries({
            upColor: currentTheme.upColor,
            downColor: currentTheme.downColor,
            borderVisible: false,
            wickUpColor: currentTheme.wickUp,
            wickDownColor: currentTheme.wickDown,
        });

        // 3. Tratamento e Injeção de Dados
        let chartData = [];

        // Se vier dados reais da API/Prop
        if (data && Array.isArray(data) && data.length > 0) {
            console.log("IFMD Chart: Processando dados reais...", data.length);
            
            // Ordena e Sanear
            chartData = [...data]
                .sort((a, b) => a.time - b.time)
                .map(d => {
                    const open = Number(d.open);
                    const high = Number(d.high);
                    const low = Number(d.low);
                    const close = Number(d.close);
                    
                    if (isNaN(open) || isNaN(close) || !d.time) return null;
                    
                    return { time: d.time, open, high, low, close };
                })
                .filter(item => item !== null);
        } 
        
        // Se não houver dados válidos, usa MOCKUP para não ficar tela branca
        if (chartData.length === 0) {
            console.log("IFMD Chart: Usando dados simulados (Mockup).");
            let time = Math.floor(Date.now() / 1000) - (100 * 300); // Começa no passado (segundos)
            let close = 50.0; // Preço base
            
            for(let i=0; i<100; i++){
                time += 300; // 5 minutos
                let open = close;
                let high = open + Math.random() * 0.5;
                let low = open - Math.random() * 0.5;
                close = (open + Math.random() - 0.5);
                if(low > close) low = close - 0.1;
                if(high < open) high = open + 0.1;
                
                chartData.push({ time, open, high, low, close });
            }
        }

        // 4. Injeta os dados na série
        newSeries.setData(chartData);

        // 5. O SEGREDO DO "APARECER": Fit Content
        // Força a câmera do gráfico a focar exatamente onde os candles estão
        chart.timeScale().fitContent(); 

        // 6. Resize Observer (Garante que se a janela mudar, o gráfico ajusta)
        const handleResize = () => {
            if (chartContainerRef.current) {
                chart.applyOptions({ 
                    width: chartContainerRef.current.clientWidth,
                    height: chartContainerRef.current.clientHeight 
                });
                // Refoca após resize
                chart.timeScale().fitContent();
            }
        };

        const resizeObserver = new ResizeObserver(() => handleResize());
        resizeObserver.observe(chartContainerRef.current);

        chartRef.current = chart;

        // Limpeza
        return () => {
            resizeObserver.disconnect();
            chart.remove();
        };

    }, [data, isDark]); // Recria se os dados ou o tema mudarem

    return (
        <div className="w-full h-full relative" style={{ minHeight: '100%' }}>
            {/* Container do Gráfico */}
            <div ref={chartContainerRef} className="w-full h-full absolute inset-0" />
            
            {/* Marca D'água */}
            <div className={`absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 
                text-4xl font-bold opacity-5 pointer-events-none select-none tracking-widest z-0
                ${isDark ? 'text-slate-700' : 'text-slate-300'}`
            }>
                IFMD {ticker}
            </div>
        </div>
    );
}