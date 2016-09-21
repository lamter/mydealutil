# coding: utf-8

import doctest
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class DonchianChannelOpt:
    """
    Donchian Channel 突破系统的优化
    对 DAY_IN, DAY_OUT 进行优化
    """

    def __init__(self, df):
        self.df = df.copy()

    def draw(self):
        df = self.df
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.set_xlabel("DAY_IN")
        ax.set_ylabel("DAY_OUT")
        ax.set_zlabel("capital")
        x = df["DAY_IN"]
        y = df["DAY_OUT"]
        z = df["capital"]
        ax.plot_trisurf(x, y, z, cmap=cm.jet, linewidth=0.01)



class Example:
    def draw(self):
        """
        >>> e = Example()
        >>> e.draw()

        :return:
        """
        delta = 1
        x = np.arange(-3, 3, delta)
        y = np.arange(-2, 4, delta)
        X, Y = np.meshgrid(x, y)
        Z = X ** 2 + Y ** 2

        x = X.flatten()
        y = Y.flatten()
        z = Z.flatten()



        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot_trisurf(x, y, z, cmap=cm.jet, linewidth=0.01)


if __name__ == "__main__":
    doctest.testmod()
