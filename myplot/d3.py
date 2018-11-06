# coding: utf-8

import sys
import doctest
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
from mpl_toolkits.mplot3d import Axes3D


class DonchianChannelOpt:
    """
    Donchian Channel 突破系统的优化
    对 DAY_IN, DAY_OUT 进行优化
    """

    def __init__(self, df):
        if df.shape[1] != 3:
            raise ValueError(u"df只能有3个 cols")
        self.df = df.copy()

    def draw(self):
        df = self.df
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        x_col, y_col, z_col = df.columns
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_zlabel(z_col)
        x = df[x_col]
        y = df[y_col]
        z = df[z_col]
        ax.set_title(z_col)
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
