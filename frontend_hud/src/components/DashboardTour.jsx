import React from 'react';
import Joyride, { STATUS } from 'react-joyride';

export default function DashboardTour({ run, onFinish }) {
    
    const steps = [
        {
            target: '.tour-status', 
            content: 'Aqui o sistema monitora se o mercado está Aberto, Fechado ou em Leilão. Sincronização em tempo real com a B3.',
            title: '📡 STATUS DO SISTEMA',
            disableBeacon: true,
            placement: 'bottom'
        },
        {
            target: '.tour-arbitrage',
            content: 'O coração do HFT. Monitoramos o spread matemático entre EWZ (Nova York) e o Dólar/Ibovespa local. Divergências > 500 geram alertas.',
            title: '⚖️ SCANNER DE ARBITRAGEM',
            placement: 'bottom'
        },
        {
            target: '.tour-overview',
            content: 'Mapa de Calor Vertical. Identifique instantaneamente quem está puxando o índice para cima (Verde) ou para baixo (Vermelho).',
            title: '📊 PANORAMA DE MERCADO',
            placement: 'bottom'
        },
        {
            target: '.tour-grid',
            content: 'Seus ativos monitorados. Clique em qualquer card para acionar a Inteligência Artificial e receber uma análise técnica SMC imediata.',
            title: '💎 GRADE DE ATIVOS',
            placement: 'top'
        }
    ];

    return (
        <Joyride
            steps={steps}
            run={run}
            continuous={true}
            showProgress={true}
            showSkipButton={true}
            disableOverlayClose={true} // Não fecha se clicar fora
            spotlightClicks={false}    // Não deixa clicar no item durante o tour
            
            // ESTILIZAÇÃO AGRESSIVA PARA APARECER
            styles={{
                options: {
                    zIndex: 9999, // Fica acima de TUDO
                    arrowColor: '#0f172a',
                    backgroundColor: '#0f172a',
                    overlayColor: 'rgba(0, 0, 0, 0.85)',
                    primaryColor: '#06b6d4',
                    textColor: '#e2e8f0',
                    width: 380,
                },
                tooltip: {
                    border: '1px solid #22d3ee', // Borda Neon
                    borderRadius: '8px',
                    boxShadow: '0 0 40px rgba(6, 182, 212, 0.4)' // Brilho forte
                },
                buttonNext: {
                    backgroundColor: '#0891b2',
                    fontWeight: 'bold',
                    outline: 'none',
                    borderRadius: '4px'
                }
            }}
            
            callback={(data) => {
                const { status } = data;
                if ([STATUS.FINISHED, STATUS.SKIPPED].includes(status)) {
                    onFinish();
                }
            }}
            
            locale={{ 
                back: 'VOLTAR', 
                close: 'FECHAR', 
                last: 'VAMOS LÁ', 
                next: 'PRÓXIMO', 
                skip: 'PULAR' 
            }}
        />
    );
}