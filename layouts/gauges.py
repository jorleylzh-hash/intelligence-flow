# layouts/gauges.py
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from layouts.theme import COLORS

def create_chart(data):
    # --- FILTRO DE SEGURANÇA ---
    # Pegamos apenas os ativos, ignorando chaves de controle como '_META'
    items = []
    for k, v in data.items():
        if k != '_META' and isinstance(v, dict) and not v.get('hidden', False):
            items.append(k)
    
    # 2. Calcula Arbitragens (Mesma lógica anterior)
    try:
        usd = data.get('USD_BRL', {}).get('curr')
        v_adr = data.get('VALE_ADR', {}).get('curr')
        v_loc = data.get('VALE3', {}).get('curr')
        arb_vale = (((v_adr * usd) / v_loc) - 1) * 100 if (usd and v_adr and v_loc) else 0
        
        p_adr = data.get('PETR_ADR', {}).get('curr')
        p_loc = data.get('PETR4', {}).get('curr')
        arb_petr = ((((p_adr/2) * usd) / p_loc) - 1) * 100 if (usd and p_adr and p_loc) else 0
        arb_list = [('Arb VALE', arb_vale), ('Arb PETRO', arb_petr)]
    except:
        arb_list = []

    # 3. Configuração da Grade
    all_gauges = items + arb_list
    cols = 3 
    rows = (len(all_gauges) + cols - 1) // cols if len(all_gauges) > 0 else 1

    fig = make_subplots(
        rows=rows, cols=cols,
        specs=[[{'type': 'indicator'}]*cols]*rows,
        vertical_spacing=0.10, horizontal_spacing=0.05
    )

    r, c = 1, 1
    for item in all_gauges:
        if isinstance(item, tuple): 
            label, val, ref, is_arb = item[0], item[1], 0, True
        else: 
            label = item
            val = data[item].get('curr')
            ref = data[item].get('prev')
            is_arb = False

        if val is not None:
            color = COLORS['cyan'] if is_arb else (COLORS['up'] if (ref and val >= ref) else COLORS['down'])
            rng = 0.05 if not is_arb else 0.02
            ref_val = ref if ref else val
            min_g, max_g = (ref_val*(1-rng), ref_val*(1+rng)) if not is_arb else (-2, 2)

            fig.add_trace(go.Indicator(
                mode="gauge+number+delta" if not is_arb else "gauge+number",
                value=val,
                title={'text': label, 'font': {'size': 14, 'color': COLORS['text']}},
                delta={'reference': ref, 'relative': True, 'valueformat': ".2%"} if not is_arb else None,
                gauge={
                    'axis': {'range': [min_g, max_g], 'tickcolor': COLORS['grid'], 'tickwidth': 1},
                    'bar': {'color': color},
                    'bgcolor': "rgba(0,0,0,0)",
                    'borderwidth': 0,
                    'threshold': {'line': {'color': COLORS['text'], 'width': 2}, 'thickness': 0.8, 'value': ref_val}
                },
                number={'font': {'color': 'white', 'size': 18}, 'suffix': "%" if is_arb else ""}
            ), row=r, col=c)

            c += 1
            if c > cols: c=1; r+=1

   # Dentro de layouts/gauges.py

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=30, b=10), # Margens reduzidas para ganhar espaço
        # A altura agora é baseada no número de linhas para não achatar os círculos
        height=max(500, rows * 200), 
        autosize=True,
        font=dict(family="Segoe UI", size=10, color=COLORS['text'])
    )
    
    return fig