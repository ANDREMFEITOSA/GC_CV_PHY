import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def func(pct, heights):
    #absolute = int(np.round(pct/100.*np.sum(heights), 2))
    absolute = np.round(pct/100.*np.sum(heights), 2)
    return f"{pct:.1f}%\n({absolute:.1f} cm)"

#Function to plot bar and pie graphs  
def plot_bar_pie_graphs(heights, color_name):
    fig, ax = plt.subplots(1, 2, figsize=(5, 5))
    g = ax[0].bar(np.array(color_name), np.array(heights), width=0.25, color=np.array(color_name))
    ax[0].grid()
    ax[0].set_ylabel('Height (cm)', fontsize=14)
    ax[0].set_xlabel('Color', fontsize=14)
    ax[0].set_frame_on(True)
    ax[0].tick_params(axis='both', which='both', length=0)
    ax[0].bar_label(g, fmt='{:,.1f}', padding = 3)
    
    ax[1].pie(np.array(heights), labels=np.array(color_name), colors=np.array(color_name), autopct=lambda pct: func(pct, np.array(heights)))

    plt.show()

#Function to plot a boxplot graph
def plot_boxplot_graph(heights, color_name):
    fig, ax = plt.subplots()
    g = ax.boxplot(heights, patch_artist=True, labels=np.array(color_name))
    ax.grid()
    #ax.set_title('Bar\'s Heights, fontsize=20)
    ax.set_ylabel('Bar Heights (cm)', fontsize=14)
    ax.set_frame_on(True)
    
    for patch, color in zip(g['boxes'], color_name):
        patch.set_facecolor(color)
    
    plt.show()

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
