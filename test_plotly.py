import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go #Módulo da biblioteca para criar visualizações de dados interativas e personalizadas

df = pd.read_csv('C:/Users/User/Projetos/alura-vizualizacao-de-dados-python/imigrantes_canada.csv')

df.set_index('País', inplace=True)

###

anos = list(map(str, range(1980, 2014)))

brasil = df.loc['Brasil', anos]
argentina = df.loc['Argentina', anos]

brasil_dict = {'ano': brasil.index.tolist(), 'imigrantes': brasil.values.tolist()}
dados_brasil = pd.DataFrame(brasil_dict)

argentina_dict = {'ano': argentina.index.tolist(), 'imigrantes': argentina.values.tolist()}
dados_argentina = pd.DataFrame(argentina_dict)


###

america_sul = df.query('Região =="América do Sul"')

df_america_sul_clean = america_sul.drop(['Continente', 'Região', 'Total'], axis=1) #remove colunas (axis=1) do dataframe america_sul

america_sul_final = df_america_sul_clean.T #transposiçãao linha x coluna da tabela

#print(america_sul_final.head())
###

# fig = px.line(dados_brasil, x='ano', y='imigrantes',
#               title='Imigração do Brasil para o Canadá no período de 1980 a 2013')

# fig = px.line(america_sul_final, x=america_sul_final.index, y=america_sul_final.columns, color='País',
#               title='Imigração dos Países da Américado Sul para o Canadá no período de 1980 a 2013', markers=True)

#fig.update_traces(line_color='green', line_width=4)

# fig.update_layout(width=1000, height=500,
#                   xaxis={'tickangle':-45},
#                 #   font_family='Arial',
#                 #   font_size=14,
#                 #   font_color='grey',
#                 #   title_font_color='black',
#                 #   title_font_size=22,
#                   xaxis_title='Ano',
#                   yaxis_title='Número de imigrantes')

#fig.write_html('imigracao_america_sul.html') #salvar gráfico em html

### Criação de gráfico com animação

# Mudar o tipo de dados da coluna que contém os anos para int ao invés de manter como strings

dados_brasil['ano'] = dados_brasil['ano'].astype(int)
dados_argentina['ano'] = dados_argentina['ano'].astype(int)

#Criação de uma figura vazia

fig = go.Figure()

# Uma linha é adicionada ao gráfico
# Objeto Scatter recebe como argumentos os dados para os eixos X e Y do gráfico

fig.add_trace(
    go.Scatter(x=[dados_brasil['ano'].iloc[0]], y=[dados_brasil['imigrantes'].iloc[0]], mode='lines', name='Imigrantes', line=dict(width=4))
)

fig.add_trace(
    go.Scatter(x=[dados_argentina['ano'].iloc[0]], y=[dados_argentina['imigrantes'].iloc[0]], mode='lines', name='Imigrantes', line=dict(width=4))
)

fig.update_layout(
    title=dict(
        text='<b>Imigração do Brasil e da Argentina para o Canadá no período de 1980 a 2013</b>',
        x=0.1,
        #xanchor='left',
        font=dict(size=18)
    ),
    xaxis=dict(range=[1980, 2013], autorange=False, title='<b>Ano</b>'),
    yaxis=dict(range=[0, 3000], autorange=False, title='<b>Número de imigrantes</b>'),
    updatemenus=[dict( # Adição de um botão "Play" para a animação
        type='buttons',
        showactive=False,
        buttons=[dict(
            label='Play',
            method='animate',
            args=[None, {'frame': {'duration': 100, 'redraw': True}, 'fromcurrent': True}]
        )]
    )],
    width=1200,
    height=600 )

# Definir as configurações de animação

frames = []

# frames = [go.Frame(data=[go.Scatter(x=dados_brasil['ano'].iloc[:i+1], y=dados_brasil['imigrantes'].iloc[:i+1])]) for i in range(len(dados_brasil))]
# fig.frames = frames

for i in range(len(dados_brasil)):
    frame_data = [
        go.Scatter(x=dados_brasil['ano'].iloc[:i+1], y=dados_brasil['imigrantes'].iloc[:i+1]),
        go.Scatter(x=dados_argentina['ano'].iloc[:i+1], y=dados_argentina['imigrantes'].iloc[:i+1])
    ]

    frame = go.Frame(data=frame_data)

    frames.append(frame)
    
fig.frames = frames

fig.show()

