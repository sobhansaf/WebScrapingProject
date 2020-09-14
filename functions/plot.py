import matplotlib.pyplot as plt
import datetime

def plot_date(xdates, yprices, x_label, y_label, rotation):
    plt.plot_date(xdates, yprices)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(rotation=rotation)
    plt.show()




