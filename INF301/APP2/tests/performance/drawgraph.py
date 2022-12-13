import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

def drawgraph(x, temps, memoire=None, mode=None):
    plt.clf()
    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('size')
    ax1.set_ylabel('time (s)', color=color)
    ax1.plot(x, temps, color=color)
    ax1.plot(x, temps, 'b+') # also plot the dots as crosshairs
    ax1.tick_params(axis='y', labelcolor=color)

    if memoire is not None:
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

        color = 'tab:green'
        ax2.set_ylabel('memoire (GB)', color=color)  # we already handled the x-label with ax1
        ax2.plot(x, memoire, color=color)
        ax2.plot(x, memoire, 'b+') # also plot the dots as crosshairs
        ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    plt.savefig(mode + ".png")


