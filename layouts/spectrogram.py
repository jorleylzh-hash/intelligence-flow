# layouts/spectrogram.py
import plotly.graph_objects as go

def create_chart(data):
    if not data: return go.Figure()
    
    items = []
    for label, info in data.items():
        if label == '_META': continue 
        if not info.get('hidden') and info.get('curr') is not None and info.get('prev') is not None:
            curr = float(info['curr'])
            prev = float(info['prev'])
            # Cálculo da variação
            change = ((curr - prev) / prev) * 100 if prev != 0 else 0
            items.append({'label': label, 'change': change})
    
    # Ordenação para o efeito cascata
    items.sort(key=lambda x: x['change'])
    
    vals = [i['change'] for i in items]
    names = [i['label'] for i in items]
    # Cores: Verde para alta, Vermelho para baixa
    cols = ['#00ff41' if v >= 0 else '#ff003c' for v in vals]

    fig = go.Figure(go.Bar(
        x=vals, 
        y=names, 
        orientation='h',
        marker=dict(color=cols, line=dict(width=1, color='rgba(0,243,255,0.2)')),
        text=[f"{v:+.2f}%" for v in vals],
        texttemplate='%{text}',
        # SOLUÇÃO: 'auto' decide se coloca dentro ou fora baseado no espaço
        textposition='auto', 
        # Garante que o texto tenha contraste mesmo fora da barra
        insidetextfont=dict(size=12, color='black'),
        outsidetextfont=dict(size=12, color='#e0f2fe'),
        cliponaxis=False # Impede que o texto seja cortado nas bordas
    ))

    fig.update_layout(
        title=dict(text="🔥 RELATIVE STRENGTH SPECTRUM", font=dict(color='#00f3ff', size=14)),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=40, b=30, l=90, r=50), # Aumentado margem direita para o texto não sumir
        # REMOVIDO uniformtext para permitir que o texto mantenha o tamanho 12 sempre
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.05)',
            tickfont=dict(color='#e0f2fe', size=10),
            zerolinecolor='rgba(0, 243, 255, 0.5)',
            # Expande um pouco o eixo X para o texto "fora" ter espaço
            range=[min(vals)*1.3 - 0.5, max(vals)*1.3 + 0.5] 
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.05)',
            tickfont=dict(color='#e0f2fe', size=11),
            automargin=True
        ),
        showlegend=False,
        uirevision='constant'
    )

    return fig