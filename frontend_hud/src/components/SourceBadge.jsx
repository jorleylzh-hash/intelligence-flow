import React from 'react';

const SourceBadge = ({ source }) => {
    // Normaliza para garantir que a comparação funcione (ex: 'Global' vira 'global')
    const safeSource = source ? source.toLowerCase() : 'local';

    const styles = {
        local: {
            label: 'B3 / CLEAR',
            color: 'text-cyan-400',
            borderColor: 'border-cyan-500',
            glow: 'shadow-[0_0_8px_rgba(34,211,238,0.5)]',
            bg: 'bg-cyan-950/40'
        },
        global: {
            // ATUALIZADO AQUI
            label: 'INVESTRADES / NYSE', 
            color: 'text-fuchsia-400',
            borderColor: 'border-fuchsia-500',
            glow: 'shadow-[0_0_8px_rgba(232,121,249,0.5)]',
            bg: 'bg-fuchsia-950/40'
        },
        yahoo: {
            label: 'YFINANCE',
            color: 'text-amber-400',
            borderColor: 'border-amber-500',
            glow: 'shadow-[0_0_8px_rgba(251,191,36,0.5)]',
            bg: 'bg-amber-950/40'
        }
    };

    // Seleciona o estilo ou usa 'local' como fallback de segurança
    const active = styles[safeSource] || styles.local;

    return (
        <div className={`
            inline-flex items-center gap-1.5 px-2 py-0.5 rounded border-l-2 ml-2
            ${active.bg} ${active.borderColor} ${active.glow}
            transition-all duration-300
        `}>
            {/* Indicador de Status (Ponto Pulsante) */}
            <span className={`w-1.5 h-1.5 rounded-full animate-pulse ${active.color.replace('text-', 'bg-')}`} />
            
            {/* Texto do Badge */}
            <span className={`text-[9px] font-mono font-bold tracking-widest ${active.color}`}>
                {active.label}
            </span>
        </div>
    );
};

export default SourceBadge;