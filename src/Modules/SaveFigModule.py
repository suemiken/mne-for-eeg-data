# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

def ERSPMultiFig(ERSPs, Time = [None, None], Frq = [None, None], aspect=0.01, vNum = None, hNum = None,
                wspace=0.4, hspace=0.6):
    fig, axes = plt.subplots(nrows=vNum, ncols=hNum, figsize=(16, 30), sharex=False, sharey=False)
    fig.subplots_adjust(wspace=wspace, hspace=hspace)

    nNum = ERSPs.shape[0]

    cnt = -1
    for i in range(0, vNum):
        for j in range(0, hNum):
            axes[i,j].axis('tight')
            cnt = cnt + 1
            axes[i,j].imshow(ERSPs[cnt, :, :], origin='lower', cmap='jet',
                    extent=(Time[0], Time[-1], Frq[0], Frq[-1]), aspect=aspect)
            #axes[i,j].plot(time, Amp[:, cnt], linewidth=2)
            Numstr = 'Channel' + str(cnt+1)
            axes[i,j].set_title(Numstr)
            axes[i,j].set_xlabel('Time [s]')
            axes[i,j].set_ylabel('Freaquency [Hz]')
            axes[i,j].set_xlim(Time[0], Time[-1])
            axes[i,j].set_ylim(Frq[0], Frq[-1])

            if cnt == nNum-1:
                plt.show()
                print('OK!')
                return (fig, axes)

def PlotMultiFig(time, Amp, xlim = [None, None], vNum = None, hNum = None,
                title = 'Fig', xlabel = 'x', ylabel = 'y', figsize = (48,32), wspace=0.4, hspace=0.6):

    fig, axes = plt.subplots(nrows=vNum, ncols=hNum, figsize=figsize, sharex=False, sharey=False)
    fig.subplots_adjust(wspace=wspace, hspace=hspace)

    nNum = Amp.shape[0]

    cnt = -1
    for i in range(0, vNum):
        for j in range(0, hNum):
            cnt = cnt + 1
            axes[i,j].plot(time, Amp[cnt, :], linewidth=0.5)
            Numstr = title + str(cnt+1)
            axes[i,j].set_title(Numstr)
            axes[i,j].set_xlabel(xlabel)
            axes[i,j].set_ylabel(ylabel)
            axes[i,j].grid(True)
            axes[i,j].set_xlim(xlim[0], xlim[1])

            if cnt == nNum-1:
                plt.show()
                print('OK!')
                return (fig, axes)
