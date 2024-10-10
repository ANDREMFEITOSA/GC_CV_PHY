import matplotlib.pyplot as plt
import pandas as pd
import numpy as np 

#Function to plot bar graph
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

#Function to plot stacked bar graph
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

#Function to plot bar and stacked bar graphs
#def plotar_graficos(n_bars, colors_name, heights):
def plotar_graficos(n_bars, rgb_string, heights, average_rgb):
    #df = pd.DataFrame([heights], index = np.array(average_rgb))
    fig, ax = plt.subplots(1, 2, figsize=(5, 5))
    g = ax[0].bar(np.array(rgb_string), np.array(heights), width=0.25, color=np.array(average_rgb))
    ax[0].grid()
    ax[0].set_title('Bar\'s Height x Color', fontsize=20)
    ax[0].set_ylabel('Height (cm)', fontsize=14)
    ax[0].set_xlabel('Color', fontsize=14)
    ax[0].set_frame_on(True)
    ax[0].tick_params(axis='both', which='both', length=0)
    ax[0].bar_label(g, fmt='{:,.1f}', padding = 3)
    
    bottom = np.zeros(3)
    list_g = []
    for i in range(n_bars):
        list_g.append(ax[1].bar('Stack', heights[i], width=0.10, bottom=bottom, align='center', color=average_rgb[i]))
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
    
    
def plotar_graficos_(n_bars, color_name, heights):
    fig, ax = plt.subplots(1, 2, figsize=(5, 5))
    g = ax[0].bar(np.array(color_name), np.array(heights), width=0.25, color=np.array(color_name))
    ax[0].grid()
    ax[0].set_title('Bar\'s Height x Color', fontsize=20)
    ax[0].set_ylabel('Height (cm)', fontsize=14)
    ax[0].set_xlabel('Color', fontsize=14)
    ax[0].set_frame_on(True)
    ax[0].tick_params(axis='both', which='both', length=0)
    ax[0].bar_label(g, fmt='{:,.1f}', padding = 3)
    
    bottom = np.zeros(3)
    list_g = []
    for i in range(n_bars):
        list_g.append(ax[1].bar('Stack', heights[i], width=0.10, bottom=bottom, align='center', color=color_name[i]))
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
