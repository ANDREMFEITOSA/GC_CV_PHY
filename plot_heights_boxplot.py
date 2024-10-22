import numpy as np 
import matplotlib.pyplot as plt
import webcolors
import plot_graphs
import color_name

heights_list = [np.array([7.3, 7.3, 7.3, 7.3, 7.3, 7.6, 7.6, 7.5, 7.5, 7.5]),
                np.array([6.4, 6.3, 6.4, 6.4, 6.4, 6.6, 6.6, 6.6, 6.6, 6.6]),
                np.array([5.5, 5.4, 5.5, 5.5, 5.5, 5.7, 5.8, 5.8, 5.7, 5.7]),
                np.array([4.7, 4.6, 4.6, 4.6, 4.6, 4.8, 4.8, 4.8, 4.8, 4.8])]

color_name = ['red', 'limegreen', 'turquoise', 'sandybrown']

plot_graphs.plot_boxplot_graph(heights_list, color_name)

