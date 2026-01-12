import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from modulo import market_view
import os

app = dash.Dash(__name__)
server = app.server # Necessário para o Gunicorn no Render

app.layout = html.Div(style={'backgroundColor': 'black', 'minHeight': '100vh', 'padding': '10px'}, children=[
    
    # Título e Status
    html.Div([
        html.H2("Intelligence Flow - M5 Dashboard", style={'color': '#00FF7F', 'textAlign': 'center'}),
        html.P("Monitoramento Global & Arbitragem em Tempo Real (Delay YF)", style={'color': 'gray', 'textAlign': 'center'})
    ]),

    # Componente de Gráfico
    dcc.Graph(
        id='live-market-graph',
        style={'height': '85vh'},
        config={'displayModeBar': False} # Remove barra de ferramentas para visual limpo
    ),

    # Atualizador Automático (60 segundos)
    dcc.Interval(
        id='interval-update',
        interval=60*1000, 
        n_intervals=0
    )
])

@app.callback(Output('live-market-graph', 'figure'),
              Input('interval-update', 'n_intervals'))
def update_dashboard(n):
    return market_view.create_dashboard()

if __name__ == '__main__':
    app.run_server(debug=True)
