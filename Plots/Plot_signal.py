import numpy as np
import matplotlib.pyplot as plt


def plotsignals(signals):
    for x, y in enumerate(signals):
        l, = plt.plot(x, y)
    plt.legend(loc='lower right')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()



            