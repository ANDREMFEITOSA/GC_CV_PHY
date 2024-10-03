import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import animation

l1 = [8.2, 9.7]
l2 = [(0.17113410101996532, 0.6809895833333334, 0.3185142013761733), (0.3567228582170274, 0.6158854166666666, 0.16760423448350692)]
l3 = ["("+", ".join(map(str, l2[0]))+")", "("+", ".join(map(str, l2[1]))+")"]

def plotar_grafico(a, b):
    df = pd.DataFrame(a, index = b)
    fig, ax = plt.subplots(figsize=(5, 5))
    g = ax.bar(a, b, width=0.25, color='green')
    ax.grid()
    ax.set_title('Bar Height x Color', fontsize=20)
    ax.set_ylabel('Height (cm)', fontsize=14)
    ax.set_xlabel('Color', fontsize=14)
    ax.set_frame_on(True)
    ax.tick_params(axis='both', which='both', length=0)
    ax.bar_label(g, fmt='{:,.1f}', padding = 3)
    plt.show()
    
plotar_grafico(l3, l1)

for i in range(len(l3)):
    print(l3[i])
