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
        points = []
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

            nonlocal new_I
            new_I = I
            nonlocal new_x
            new_x = x
            new_I = next_point_I(new_I, new_x, step)
            new_x = next_point_x(step, new_x)

            nonlocal tmp_I
            tmp_I = new_I
            nonlocal tmp_x
            tmp_x = new_x
            nonlocal tmp_h
            tmp_h = step

            print("func next I:", new_I)
            print("func next x:", new_x)

            nonlocal add_I
            add_I = I
            nonlocal add_x
            add_x = x
            add_I = next_point_I(add_I, add_x, step / 2)
            add_x = next_point_x(step / 2, add_x)

            print("func add I:", add_I)
            print("func add x:", add_x)

            new_add_I = next_point_I(add_I, add_x, step / 2)
            new_add_x = next_point_x(step / 2, add_x)

            print("func next I:", new_add_I)
            print("func next x:", new_add_x)

            S = loc_err(new_I, new_add_I)

            self.tableWidget.setItem(number_r, 1, QtWidgets.QTableWidgetItem(str(new_I)))
            self.tableWidget.setItem(number_r, 2, QtWidgets.QTableWidgetItem(str(new_x)))
            self.tableWidget.setItem(number_r, 3, QtWidgets.QTableWidgetItem(str(new_add_I)))
            self.tableWidget.setItem(number_r, 4, QtWidgets.QTableWidgetItem(str(new_add_x)))
            self.tableWidget.setItem(number_r, 5, QtWidgets.QTableWidgetItem(str(tmp_h)))
            self.tableWidget.setItem(number_r, 6, QtWidgets.QTableWidgetItem(str(S)))
            print("S####: ", S)
            print("exp###: ", eps / 16, eps)

            nonlocal new_h
            if abs(S) >= eps / 16 and abs(S) <= eps:
                print("save point")
                new_h = tmp_h
                # return {'coord_x': new_x, 'coord_I': new_I}
                return new_x, new_I
            if abs(S) < eps / 16:
                print("save point, but change step")
                new_h = 2 * tmp_h
                # return {'coord_x': new_x, 'coord_I': new_I}
                return new_x, new_I
            if abs(S) > eps:
                print("Fail")
                tmp_h = tmp_h / 2
                return new_point(tmp_h, tmp_x, tmp_I, number_r)

        new_x = x
        new_I = I
        add_I = new_I
        add_x = new_x
        new_h = h
        tmp_I = 0.0
        tmp_x = 0.0
        tmp_h = h
        xlist = []
        Ilist = []
        for i in range(n):
            a, b = new_point(new_h, new_x, new_I, i)
            # print(points)
            self.tableWidget.setItem(i, 8, QtWidgets.QTableWidgetItem(str(a)))
            xlist.append(a)
            Ilist.append(b)
        # for i in points:
        #    print(i, '\n')
        # for i in points:
        #    xlist.append(i['coord_x'])
        #    Ilist.append(i['coord_I'])
        abs_x = xlist
        abs_I = [abs_solution(x, I) for x in abs_x]
        for i in range(len(abs_I)):
            self.tableWidget.setItem(i, 7, QtWidgets.QTableWidgetItem(str(abs_I[i])))
        ax = self.figure.add_subplot(111)
        #ax.clear()
        print(xlist)
        ax.plot(xlist, Ilist, '-b')
        ax.plot(abs_x, abs_I, '-r')
        ax.axis([-10, 20, -10, 20])
        ax.grid(True)
        self.canvas.draw()
