import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
#from drawnow import *

# def makeFig():
#  gs = gridspec.GridSpec(3, 3) #gridspec 3x3
#  #Plot 1
#  plt.subplot(gs[0, :])#posicao do subplot
#  plt.ylim([-30,50])#valor min e max de y
#  plt.title('Temperatura em Graus C')#titulo
#  plt.grid(True)
#  plt.ylabel('Temp-1 c')#etiquetas do eixo y
#  plt.plot(tempF, 'ro-', label='temperatura em
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