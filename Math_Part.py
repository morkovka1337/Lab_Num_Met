# -*- coding: utf-8 -*-
import math
import pylab
from matplotlib import mlab
from matplotlib.figure import Figure
from label_for_graphic import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets, QtGui, QtCore
from main import MyWin
#######################################
class Math_Part(Ui_MainWindow):

    def bilding(self, n, L, I, h, x, R, w, E):
        eps = 0.00001
        print(L, R, I, h, x, n, E, w)
        self.tableWidget.setRowCount(n+1)
        for i in range(n+1):
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i)))
        def abs_solution(x, I):
            return (((E * R * math.sin(w * x))/((L**2)*(w**2) + (R**2))) - ((E * L * w * math.cos(w * x))/((L**2)*(w**2) + (R**2))) + (sol_const(I) * math.exp((-(R * x)) / L)))
        def sol_const(I):
            return I + E * L * w / ((L**2)*(w**2) + (R**2))
        def f(x, I):
            return (E * (math.sin(w * x)) - R * I) / L

        def loc_err(step_I, two_step_I):
            return ((two_step_I - step_I) * ((8.0) / 7.0))

        def step_func1(step, x, I):
            return step * f(x, I)

        def step_func2(step, x, I):
            return step * f(x + step / 2, I + step_func1(step, x, I) / 2)

        def step_func3(step, x, I):
            return step * f(x + step, I + 2 * step_func2(step, x, I) - step_func1(step, x, I))

        def next_point_x(step, x):
            return x + step

        def next_point_I(I, x, step):
            return I + (step_func1(step, x, I) + 4 * step_func2(step, x, I) + step_func3(step, x, I)) / 6

        ##################################################
        def new_point(step, x, I, number_r):
            nonlocal h
            new_I = next_point_I(I, x, step)
            new_x = next_point_x(step, x)

            add_I = next_point_I(I, x, step / 2)
            add_x = next_point_x(step / 2, x)

            add_I = next_point_I(add_I, add_x, step / 2)
            add_x = next_point_x(step / 2, add_x)

            S = loc_err(new_I, add_I)

            self.tableWidget.setItem(number_r, 1, QtWidgets.QTableWidgetItem(str(new_I)))
            self.tableWidget.setItem(number_r, 2, QtWidgets.QTableWidgetItem(str(new_x)))
            self.tableWidget.setItem(number_r, 3, QtWidgets.QTableWidgetItem(str(add_I)))
            self.tableWidget.setItem(number_r, 4, QtWidgets.QTableWidgetItem(str(add_x)))
            self.tableWidget.setItem(number_r, 5, QtWidgets.QTableWidgetItem(str(h)))
            self.tableWidget.setItem(number_r, 6, QtWidgets.QTableWidgetItem(str(S)))

            print("S####: ", S)
            print("exp###: ", eps / 16, eps)

            if abs(S) >= eps / 16 and abs(S) <= eps:
                print("save point")
                return new_x, new_I
            if abs(S) < eps / 16:
                print("save point, but change step")
                h *= 2
                return new_x, new_I
            if abs(S) > eps:
                print("Fail")
                h /= 2
                return new_point(h, x, I, number_r)

        ax = self.figure.add_subplot(111)
        ax.axis([-10, 20, -10, 20])
        abs_x, abs_I = x, abs_solution(x, I)
        for i in range(n):
            old_x, old_I = x, I
            x, I = new_point(h, x, I, i)
            self.tableWidget.setItem(i, 8, QtWidgets.QTableWidgetItem(str(x)))
            ax.plot([old_x, x], [old_I, I], '-b')
            old_abs_x, old_abs_I = abs_x, abs_I
            abs_x, abs_I = abs_x+h, abs_solution(x, abs_I)
            ax.plot([old_x, x], [old_abs_I, abs_I], '-r')
            self.tableWidget.setItem(i, 7, QtWidgets.QTableWidgetItem(str(abs_I)))

        ax.grid(True)
        self.canvas.draw()
