from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt


C = OrderedDict([(0.0, 1.6783367376655396), (0.1, 1.6963311939288026), (0.2, 1.7345752500757055), (0.3, 1.7967522977368948), (0.4, 1.705927617189841), (0.5, 1.3475075634956761), (0.6, 1.3847613008563597), (0.7, 1.309434242070453), (0.8, 1.1962294415210688), (0.9, 1.2206186819973137)])
D = OrderedDict([(0.0, 39), (0.1, 39), (0.2, 40), (0.3, 42), (0.4, 41), (0.5, 24), (0.6, 25), (0.7, 23), (0.8, 16), (0.9, 17)])
def display_successes_plot(D):
    N = 10
    ind = np.arange(N)  # the x locations for the groups
    width = 0.35       # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, D.values(), width, color='b')

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Successful trials out of 50')
    ax.set_xlabel('Gamma')
    ax.set_xticks(ind + width)
    ax.set_xticklabels((D.keys()))

    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1*height,
                    '%d' % int(height),
                    ha='center', va='bottom')

    autolabel(rects1)


    plt.show()

def display_avg_reward_plot(D):
    N = 10
    ind = np.arange(N)  # the x locations for the groups
    width = 0.35       # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, D.values(), width, color='b')

    # add some text for labels, title and axes ticks
    ax.set_xlabel('Gamma')
    ax.set_ylabel('Average reward per action')
    ax.set_xticks(ind + width)
    ax.set_xticklabels((D.keys()))

    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1*height,
                    '1.%d' % int((height-1)*100),
                    ha='center', va='bottom')

    autolabel(rects1)


    plt.show()
display_successes_plot(D)
display_avg_reward_plot(C)