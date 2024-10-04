import matplotlib.pyplot as plt
import pandas as pd
import numpy as np 

#Função para plotar gráfico tipo bar
def plotar_grafico_bar(colors_string, heights, colors):
    df = pd.DataFrame([heights], index = [colors_string])
    fig, ax = plt.subplots(figsize=(5, 5))
    g = ax.bar(np.array(colors_string), np.array(heights), width=0.25, color=np.array(colors))
    ax.grid()
    ax.set_title('Bar\'s Height x Color', fontsize=20)
    ax.set_ylabel('Height (cm)', fontsize=14)
    ax.set_xlabel('Color (RGB)', fontsize=14)
    ax.set_frame_on(True)
    ax.tick_params(axis='both', which='both', length=0)
    ax.bar_label(g, fmt='{:,.1f}', padding = 3)
    plt.show()

#Função para plotar gráfico tipo stacked bar
def plotar_grafico_stacked(n_bars, heights, colors):
    fig, ax = plt.subplots(figsize=(5, 5))
    bottom = np.zeros(3)
    list_g = []
    for i in range(n_bars):
        list_g.append(ax.bar('Stack', heights[i], width=0.10, bottom=bottom, align='center', color=colors[i]))
        bottom += heights[i] 
    
    for i in range(n_bars):
        ax.bar_label(list_g[i], fmt='{:,.1f}', label_type='center', padding = 3)
    
    ax.grid()
    ax.set_title('Stacked Bar', fontsize=20)
    ax.set_ylabel('Height (cm)', fontsize=14)
    ax.set_xlabel('', fontsize=14)
    ax.set_frame_on(True)
    ax.tick_params(axis='both', which='both', length=0)
    
    plt.show()

#Função para plotar gráficos tipo bar e stacked bar
def plotar_graficos(n_bars, colors_string, heights, colors):
    df = pd.DataFrame([heights], index = [colors_string])
    fig, ax = plt.subplots(1, 2, figsize=(5, 5))
    g = ax[0].bar(np.array(colors_string), np.array(heights), width=0.25, color=np.array(colors))
    ax[0].grid()
    ax[0].set_title('Bar\'s Height x Color', fontsize=20)
    ax[0].set_ylabel('Height (cm)', fontsize=14)
    ax[0].set_xlabel('Color (RGB)', fontsize=14)
    ax[0].set_frame_on(True)
    ax[0].tick_params(axis='both', which='both', length=0)
    ax[0].bar_label(g, fmt='{:,.1f}', padding = 3)
    
    bottom = np.zeros(3)
    list_g = []
    for i in range(n_bars):
        list_g.append(ax[1].bar('Stack', heights[i], width=0.10, bottom=bottom, align='center', color=colors[i]))
        bottom += heights[i] 
    for i in range(n_bars):
        ax[1].bar_label(list_g[i], fmt='{:,.1f}', label_type='center', padding = 3)
    ax[1].grid()
    ax[1].set_title('Stacked Bar', fontsize=20)
    ax[1].set_ylabel('Height (cm)', fontsize=14)
    ax[1].set_xlabel('', fontsize=14)
    ax[1].set_frame_on(True)
    ax[1].tick_params(axis='both', which='both', length=0)

    plt.show()
    
# if(__name__ == "__main__"):
#     plotar_graficos()