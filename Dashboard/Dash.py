from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd


df = pd.read_csv('ecommerce_estatistica.csv')
lista_dados = df['Marca'].unique()  # Lista todos os valores únicos da coluna
options = [{'label': Marca, 'value': Marca} for Marca in lista_dados]

def cria_graficos(selecao):
    filtro_df = df[df['Marca'].isin(selecao)]

    # Grafico de Barras
    fig1 = px.bar(filtro_df, x='Nota', y='N_Avaliações', color='Marca', barmode='group', color_discrete_sequence=px.colors.qualitative.Plotly)
    fig1.update_layout(
        title='Gráfico de Barras',
        xaxis_title='Nota',
        yaxis_title='Número de Avaliações',
        legend_title='Marca',
        plot_bgcolor='rgba(0,0,0,0)', # Fundo interno
        paper_bgcolor='rgba(0,0,0,0)' # Fundo externo
    )
    
    # Grafico 3D
    fig2 = px.scatter_3d(filtro_df, x='Nota', y='Desconto', z='Preço', color='Marca')

    return fig1, fig2


def cria_app():
    app = Dash(__name__)

    app.layout = html.Div([
        html.H1('Dashboard Interativo'),
        dcc.Dropdown(
            id='dropdown',
            options=options,
            value=[lista_dados[0]],
            multi=True,
            placeholder='Selecione os dados'
        ),
        html.Br(),
        dcc.Graph(id='grafico_barras'),
        html.Br(),
        dcc.Graph(id='grafico_3d')
    ])

    return app

# Executa o aplicativo
if __name__ == '__main__':
    app = cria_app()
    
    @app.callback(
        [Output('grafico_barras', 'figure'),
         Output('grafico_3d', 'figure')],
         [Input('dropdown', 'value')]
    )
    def atualizar_graficos(selecao):
        if selecao is None or len(selecao) == 0:
            return {}, {}
        fig1, fig2 = cria_graficos(selecao)
        return fig1, fig2
    app.run(debug=True)
