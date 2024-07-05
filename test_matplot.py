import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns

import pandas as pd

df = pd.read_csv('C:/Users/User/Projetos/alura-vizualizacao-de-dados-python/imigrantes_canada.csv')

#df.info()

df.set_index('País', inplace=True)

anos = list(map(str, range(1980, 2014)))

#print(anos)

brasil = df.loc['Brasil', anos]
argentina = df.loc['Argentina', anos]
peru = df.loc['Peru', anos]
colombia = df.loc['Colômbia', anos]

#print(brasil)

brasil_dict = {'ano': brasil.index.tolist(), 'imigrantes': brasil.values.tolist()}
dados_brasil = pd.DataFrame(brasil_dict)

argentina_dict = {'ano': argentina.index.tolist(), 'imigrantes': argentina.values.tolist()}
dados_argentina = pd.DataFrame(argentina_dict)

peru_dict = {'ano': peru.index.tolist(), 'imigrantes': peru.values.tolist()}
dados_peru = pd.DataFrame(peru_dict)

colombia_dict = {'ano': colombia.index.tolist(), 'imigrantes': colombia.values.tolist()}
dados_colombia = pd.DataFrame(colombia_dict)
### Matplotlib

#print(dados_brasil)

# plt.figure(figsize=(8, 4))

# plt.plot(dados_brasil['ano'], dados_brasil['imigrantes'])
# plt.plot(dados_argentina['ano'], dados_argentina['imigrantes'])
# plt.title('Imigração do Brasil para o Canada')
# plt.xlabel('Ano')
# plt.ylabel('Número de imigrantes')
# plt.legend()

# fig, ax = plt.subplots(figsize=(8, 4))
# ax.plot(dados_brasil['ano'], dados_brasil['imigrantes'])
# ax.set_title('Imigração do Brasil para o Canada\n1980 a 2013')
# ax.set_xlabel('Ano')
# ax.set_ylabel('Número de imigrantes')
# ax.xaxis.set_major_locator(plt.MultipleLocator(5))

###

# fig, axs = plt.subplots(1, 2, figsize=(15, 5))
# axs[0].plot(dados_brasil['ano'], dados_brasil['imigrantes'])
# axs[0].set_title('Imigração do Brasil para o Canada\n1980 a 2013')
# axs[0].set_xlabel('Ano')
# axs[0].set_ylabel('Número de imigrantes')
# axs[0].xaxis.set_major_locator(plt.MultipleLocator(5))
# axs[0].grid()

# axs[1].boxplot(dados_brasil['imigrantes'])
# axs[1].set_title('Boxplot da Imigração do Brasil para o Canada\n1980 a 2013')
# axs[1].set_xlabel('Brasil')
# axs[1].set_ylabel('Número de imigrantes')
# axs[1].grid()

###

# #plt.style.use('fivethirtyeight')
# plt.style.use('Solarize_Light2')

# fig, axs = plt.subplots(2, 2, figsize=(10, 6))

# fig.subplots_adjust(hspace=0.5, wspace=0.3)
# fig.suptitle('Imigração dos quatro maiores países da América do Sul para o Canadá de 1998 a 2013', fontsize=18)

# axs[0, 0].plot(df.loc['Brasil', anos], lw=3, marker='o', color='g')
# axs[0, 0].set_title('Brasil', loc='left')
# # axs[0, 0].set_xlabel('Ano')
# # axs[0, 0].set_ylabel('Número de imigrantes')
# # axs[0, 0].xaxis.set_major_locator(plt.MultipleLocator(5))
# # axs[0, 0].grid()

# axs[0, 1].plot(df.loc['Colômbia', anos], lw=3, marker='o')
# axs[0, 1].set_title('Colômbia', loc='left')
# # axs[0, 1].set_xlabel('Ano')
# # axs[0, 1].set_ylabel('Número de imigrantes')
# # axs[0, 1].xaxis.set_major_locator(plt.MultipleLocator(5))
# # axs[0, 1].grid()

# axs[1, 0].plot(df.loc['Argentina', anos], lw=3, marker='o')
# axs[1, 0].set_title('Argentina', loc='left')
# # axs[1, 0].set_xlabel('Ano')
# # axs[1, 0].set_ylabel('Número de imigrantes')
# # axs[1, 0].xaxis.set_major_locator(plt.MultipleLocator(5))
# # axs[1, 0].grid()

# axs[1, 1].plot(df.loc['Peru', anos])
# axs[1, 1].set_title('Peru', loc='left')
# # axs[1, 1].set_xlabel('Ano')
# # axs[1, 1].set_ylabel('Número de imigrantes')
# # axs[1, 1].xaxis.set_major_locator(plt.MultipleLocator(5))
# # axs[1, 1].grid()

# for ax in axs.flat:
#     ax.xaxis.set_major_locator(plt.MultipleLocator(5))

# for ax in axs.flat:
#     ax.set_xlabel('Ano', fontsize=14)
#     ax.set_ylabel('Número de imigrantes', fontsize=14)
#     ax.xaxis.set_tick_params(labelsize=12)
#     ax.yaxis.set_tick_params(labelsize=12)
    
# ymin = 0
# ymax = 7000

# for ax in axs.ravel():
#     ax.set_ylim(ymin, ymax)

# #plt.grid(linestyle='--')

###

# america_sul = df.query('Região =="América do Sul"')
# america_sul_sorted = america_sul.sort_values('Total', ascending=True)

# #print(america_sul)

# #cores = ['royalblue', 'orange', 'forestgreen', 'orchid', 'purple', 'brown', 'slateblue', 'gray', 'olive', 'navy', 'teal', 'tomato']

# #adicionar cor de barra para um dado específico
# cores = []

# for pais in america_sul_sorted.index:
#     if pais == 'Brasil':
#         cores.append('green')
#     else:
#         cores.append('silver')
    

# fig, ax = plt.subplots(figsize=(12, 5))
# ax.barh(america_sul_sorted.index, america_sul_sorted['Total'], color=cores)
# ax.set_title('América do Sul: Brasil foi o quarto País com mais imigrantes\npara o Canada no período de 1980 a 2013', loc='left', fontsize=14)
# ax.set_xlabel('Número de imigrantes', fontsize=14)
# ax.set_ylabel('')
# ax.xaxis.set_tick_params(labelsize=12)
# ax.yaxis.set_tick_params(labelsize=12)

# #adicionar os valores nas barras do gráfico
# for i, v in enumerate(america_sul_sorted['Total']):
#     ax.text(v + 20, i, str(v), color='black', fontsize=10, ha='left', va='center')

# #retira a borda externa do gráfico
# ax.set_frame_on(False)

# #retira o eixo x
# ax.get_xaxis().set_visible(False)

# #retira os ticks dos eixos
# ax.tick_params(axis='both', which='both', length=0)

# #imprimir tipos de formatos dos gráficos
# #print(fig.canvas.get_supported_filetypes())

# #salvar imagem do gráfico
# #fig.savefig('imigracao_brasil_canada.png', transparent=False, dpi=300, bbox_inches='tight')

# plt.show()

### Seaborn

#sns.set_style()
#sns.set_theme()
#sns.set_theme(style='dark')
#sns.set_theme(style='whitegrid')

sns.set_theme(style='ticks')

sns.set_palette('tab10')

top_10 = df.sort_values('Total', ascending=False).head(10)

#print(top_10)

#gráfico na vertical
# sns.barplot(data=top_10, x=top_10.index, y='Total')

#gráfico na horizontal
def gerar_grafico_paleta(palette): #argumento para indicar a paleta utilizada
    fig, ax = plt.subplots(figsize=(8, 4))
    ax = sns.barplot(data=top_10, y=top_10.index, x='Total', orient='h', palette=palette)
    ax.set(title='Países com maior imigação para o Canadá\n1980 a 2013', xlabel='Número de imigrantes', ylabel='')
    ax.set_xlabel('Número de imigrantes', fontsize=14)
    ax.set_ylabel('')
    sns.despine() #retira as bordas do gráfico
    plt.show()

#gerar_grafico_paleta('Blues_r')
#gerar_grafico_paleta('rocket')
#gerar_grafico_paleta('coolwarm')
#gerar_grafico_paleta('tab10') #paleta categórica

###

### Desafio

def gerar_grafico_paleta_4():
    
    fig, axs = plt.subplots(2, 2, figsize=(20, 10))

    fig.subplots_adjust(hspace=0.5, wspace=0.3)
    fig.suptitle('Imigração dos quatro maiores países da América do Sul para o Canadá de 1998 a 2013', fontsize=18)

    axs[0, 0] = sns.barplot(data=dados_brasil, y=dados_brasil.index, x='imigrantes', orient='h')
    axs[0, 0].set_title('Brasil', loc='left')
    # axs[0, 0].set_xlabel('Ano')
    # axs[0, 0].set_ylabel('Número de imigrantes')
    # axs[0, 0].xaxis.set_major_locator(plt.MultipleLocator(5))
    # axs[0, 0].grid()

    axs[0, 1] = sns.barplot(data=dados_colombia, y=dados_colombia.index, x='imigrantes', orient='h')
    axs[0, 1].set_title('Colômbia', loc='left')
    # axs[0, 1].set_xlabel('Ano')
    # axs[0, 1].set_ylabel('Número de imigrantes')
    # axs[0, 1].xaxis.set_major_locator(plt.MultipleLocator(5))
    # axs[0, 1].grid()

    axs[1, 0] = sns.barplot(data=dados_argentina, y=dados_argentina.index, x='imigrantes', orient='h')
    axs[1, 0].set_title('Argentina', loc='left')
    # axs[1, 0].set_xlabel('Ano')
    # axs[1, 0].set_ylabel('Número de imigrantes')
    # axs[1, 0].xaxis.set_major_locator(plt.MultipleLocator(5))
    # axs[1, 0].grid()

    axs[1, 1] = sns.barplot(data=dados_peru, y=dados_peru.index, x='imigrantes', orient='h')
    axs[1, 1].set_title('Peru', loc='left')
    # axs[1, 1].set_xlabel('Ano')
    # axs[1, 1].set_ylabel('Número de imigrantes')
    # axs[1, 1].xaxis.set_major_locator(plt.MultipleLocator(5))
    # axs[1, 1].grid()
    
    sns.despine()
    plt.show()

gerar_grafico_paleta_4()

#from drawnow import *
# def makeFig():
#  gs = gridspec.GridSpec(3, 3) #gridspec 3x3
#  #Plot 1
#  plt.subplot(gs[0, :])#posicao do subplot
#  plt.ylim([-30,50])#valor min e max de y
#  plt.title('Temperatura em Graus C')#titulo
#  plt.grid(True)
#  plt.ylabel('Temp-1 c')#etiquetas do eixo y
#  plt
# .plot(tempF, 'ro-', label='temperatura em
#  graus') #plot de temperature
#  plt.legend(loc='upper left')#plot da legenda
#  plt2=plt.twinx()#cria um Segundo eixo y
#  plt.ylim(-30,50)#define os limites do Segundo eixo y
#  plt2.plot(tempF2, 'b^-', label='Temp-2 c')
#  # desenha os val. De tempF2
#  plt2.set_ylabel('Temp-2 c') #Etiqueta do
#  # Segundo eixo
#  plt2.ticklabel_format(useOffset=False)# impede
#  # a escala do eixo X
#  plt2.legend(loc='upper right')
#  #Plot 2
#  plt.subplot(gs[1, :])
#  plt.ylim([0,100])
#  plt.title('Humidade do Ar em Percentagem')
#  plt.grid(True)
#  plt.ylabel('Humidade -1 %')
#  plt.plot(humF1, 'ro-', label='Humidade')
#  plt.legend(loc='upper left')
#  plt2=plt.twinx()
#  plt.ylim(0,100)
#  plt2.plot(humF2, 'b^-', label='Humidade-2 %')
#  plt2.set_ylabel('Humidade-2 %')
#  plt2.ticklabel_format(useOffset=False)
#  plt2.legend(loc='upper right')
#  #Plot 3
#  plt.subplot(gs[-1,0])
#  plt.ylim([0,100])
#  plt.title('Humidade do solo')
#  plt.grid(True)
#  plt.ylabel('Humidade %')
#  plt.plot(moist, 'ro-', label='Humidade')
#  plt.legend(loc='upper left')
#  #Plot 4
#  plt.subplot(gs[-1,-1])
#  plt.ylim([0,2000])
#  plt.title('Luminosidade')
#  plt.grid(True)
#  plt.ylabel('Luminosidade (lux)')
#  plt.plot(lum, 'ro-', label='Luminosidade')
#  plt.legend(loc='upper left')

# #instanciação dos objectos
# tempF = array('f')
# tempF2 = array('f')
# humF1 = array('f')
# humF2 = array('f')
# lum = array('f')
# moist = array('f')
# #comunicacao
# arduinoData = serial.Serial('com3', 115200) #Cria
# # um objecto do tipo serial chamado
# # arduinoData
# plt.ion()
# cnt=0

# while True:
#   while (arduinoData.inWaiting()==0):
#     pass
#   arduinoString = arduinoData.readline()
#   #"A tarefa mais urgente da vida, é: O que
#   # estás a fazer pelos outros?" (Martin
#   # Luther King Jr.)
#   splitedArray = [float(s) for s in
#   arduinoString.split(',')]
#   temp = splitedArray[0]
#   hum1 = splitedArray[1]
#   temp2 = splitedArray[2]
#   hum2 = splitedArray[3]
#   moisture = splitedArray[4]
#   lumen = splitedArray[5]
#   tempF.append(temp)
#   tempF2.append(temp2)
#   humF1.append(hum1)
#   humF2.append(hum2)
#   moist.append(moisture)
#   lum.append(lumen)
#   drawnow(makeFig)
#   plt.pause(.000005)
#   cnt=cnt+1
#   if(cnt>50):
#     tempF.pop(0)
#     tempF2.pop(0)
#     humF1.pop(0)
#     humF2.pop(0)
#     moist.pop(0)
#     lum.pop(0)