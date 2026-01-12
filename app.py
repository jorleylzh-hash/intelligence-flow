import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from modulo import market_view
import os

# Inicializa o App
app = dash.Dash(__name__)
app.title = "Intelligence Flow M5"

# --- IMPORTANTE PARA O RENDER ---
# O Gunicorn precisa desta variável 'server' exposta
server = app.server 

# Layout (Dark Mode)
app.layout = html.Div(style={'backgroundColor': 'black', 'minHeight': '100vh', 'padding': '10px'}, children=[
    
    html.H2("Intelligence Flow 🦅 | Painel M5", 
            style={'color': '#00FF7F', 'textAlign': 'center', 'fontFamily': 'Arial'}),
    
    # O Gráfico
    dcc.Graph(
        id='live-graph',
        style={'height': '85vh'},
        config={'displayModeBar': False} # Visual limpo
    ),

    # Atualizador Automático (5 segundos)
    dcc.Interval(
        id='interval-component',
        interval=5*1000, 
        n_intervals=0
    )
])

# Callback (Lógica de atualização)
@app.callback(Output('live-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph(n):
    # Chama o módulo para redesenhar os velocímetros
    return market_view.create_dashboard()

if __name__ == '__main__':
    # Roda localmente para teste (mas no Render quem roda é o Gunicorn)
    app.run_server(debug=True)
