import dash
import plotly.graph_objects as go
from dash import dcc, html, Input, Output
from modules import market_data
from layouts import spectrogram, gauges

app = dash.Dash(__name__, update_title=None)
server = app.server

app.layout = html.Div([
    html.Div(className='boot-cross'),
    html.Div([html.H1("↻"), html.H2("GIRE PARA MODO PAISAGEM", className='neon-text')], id='orientation-lock'),

    html.Div([
        # Header
        html.Div([
            html.H2("INTELLIGENCE FLOW", className='neon-text', style={'fontSize': '18px', 'margin': 0}),
            html.Div(id='system-status-badge')
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'padding': '15px 10px', 'alignItems': 'center'}),

        # Grid Tron
        html.Div([
            html.Div([dcc.Graph(id='spectrum', style={'height': '100%'}, config={'displayModeBar': False})], 
                     className='glass-card', style={'gridArea': 'top-left'}),
            
            html.Div([
                html.H4("MARKET SIGNALS - ARBITRAGE SCATTER", className='neon-text', style={'fontSize': '10px', 'textAlign': 'center', 'margin': '5px'}),
                html.Div([
                    html.Span("Δ % = [ ", style={'fontSize':'16px'}),
                    html.Div([html.Div("(ADR / R) × USD", className='numerator'), html.Div("Local Price")], className='fraction'),
                    html.Span(" ] − 1", style={'fontSize':'16px'})
                ], className='math-formula'),
                dcc.Graph(id='arbitrage-scatter', style={'height': '75%'}, config={'displayModeBar': False}),
            ], className='glass-card', style={'gridArea': 'top-right'}),

            html.Div([html.Div(id='ticker-content', className='ticker-content')], className='ticker-wrap'),

            html.Div([dcc.Graph(id='gauges', style={'height': '100%'}, config={'displayModeBar': False})], 
                     className='glass-card', style={'gridArea': 'bottom', 'minHeight': '550px'}),
        ], className='dashboard-grid'),

        # RODAPÉ INSTITUCIONAL (DADOS CNPJ)
        html.Footer([
            html.Div([
                html.Div("CORPORATE ENTITY", className='footer-title'),
                html.Div("INTELLIGENCE FLOW TRATAMENTO DE DADOS LTDA"),
                html.Div("CNPJ: 63.698.191/0001-27"),
                html.Div("Matriz: Curitiba - PR"),
            ], className='footer-section'),
            
            html.Div([
                html.Div("DATA PROTOCOL", className='footer-title'),
                html.Div("Feed A: MetaTrader 5 (B3 High Frequency)"),
                html.Div("Feed B: Yahoo Finance (NYSE Global Macro)"),
                html.Div("Status: Secure Connection (SSL/TLS)"),
            ], className='footer-section'),
            
            html.Div([
                html.Div("HEADQUARTERS", className='footer-title'),
                html.Div("AV JOÃO GUALBERTO, 1721 - CONJ 52"),
                html.Div("JUVEVÊ | CEP: 80.030-001"),
                html.Div("Curitiba, Brazil"),
            ], className='footer-section'),
        ], className='dashboard-footer'),

        dcc.Interval(id='timer', interval=4000, n_intervals=0)
    ], id='app-container', style={'padding': '10px'})
])

@app.callback(
    [Output('gauges', 'figure'), Output('spectrum', 'figure'), Output('arbitrage-scatter', 'figure'),
     Output('ticker-content', 'children'), Output('system-status-badge', 'children')],
    [Input('timer', 'n_intervals')]
)
def update_engine(n):
    data = market_data.get_data()
    if not data: return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
    
    usd = data.get('USD_BRL', {}).get('curr', 5.0) or 5.0
    def calc_arb(adr_k, loc_k, r=1.0):
        a, l = data.get(adr_k, {}).get('curr'), data.get(loc_k, {}).get('curr')
        if not a or not l or l <= 0: return 0.0, 0.0, 0.0
        p = (a / r) * usd
        return l, p, ((p/l)-1)*100

    v_l, v_p, v_s = calc_arb('VALE_ADR', 'VALE3', 1.0)
    p_l, p_p, p_s = calc_arb('PETR_ADR', 'PETR4', 2.0)

    fig_scat = go.Figure()
    fig_scat.add_trace(go.Scatter(x=[min(v_l, p_l)*0.95, max(v_l, p_l)*1.05], y=[min(v_l, p_l)*0.95, max(v_l, p_l)*1.05], mode='lines', line=dict(color='rgba(255,255,255,0.05)', dash='dash'), showlegend=False))
    fig_scat.add_trace(go.Scatter(x=[v_l], y=[v_p], mode='markers+text', text=[f"VALE<br>{v_s:+.2f}%"], textposition="top left", marker=dict(size=14, color='#00f3ff', symbol='diamond', line=dict(width=1, color='#fff'))))
    fig_scat.add_trace(go.Scatter(x=[p_l], y=[p_p], mode='markers+text', text=[f"PETR<br>{p_s:+.2f}%"], textposition="bottom right", marker=dict(size=14, color='#ff003c', symbol='square', line=dict(width=1, color='#fff'))))
    fig_scat.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#e0f2fe', size=10), margin=dict(t=50, b=50, l=60, r=60), showlegend=False)

    ticker_items = [html.Span([f" • {k}: {v['curr']:.2f} ", html.Span(f"({((v['curr']-(v.get('prev') or v['curr']))/(v.get('prev') or v['curr']))*100:+.2f}%)", className='ticker-up' if v['curr']>=(v.get('prev') or v['curr']) else 'ticker-down')], style={'paddingRight': '40px'}) for k,v in data.items() if k!='_META' and isinstance(v,dict) and not v.get('hidden') and v.get('curr')]

    st = data.get('_META', {}).get('status', 'SIM')
    badge = html.Div(st, className='status-live' if st == 'LIVE ON' else 'status-sim')

    f_g = gauges.create_chart(data)
    f_g.update_layout(margin=dict(t=60, b=30, l=30, r=30))
    f_s = spectrogram.create_chart(data)
    f_s.update_layout(margin=dict(t=40, b=40, l=60, r=30))

    return f_g, f_s, fig_scat, ticker_items, badge

if __name__ == '__main__':
    app.run(debug=True)