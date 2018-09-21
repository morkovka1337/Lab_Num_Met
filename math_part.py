import math
import pylab
from matplotlib import mlab

#######################################
mincoord_x = -3
maxcoord_x = 8

float(mincoord_x)
float(maxcoord_x)  
n = int(input("Enter count repeat: "))
L = float(input ("begin L:"))
I0 = float(input ("begin I0:"))
h = float(input ("begin step:"))
x0 = float(input ("begin x:"))
R = float(input ("begin R:"))
w = float(input ("begin w:"))
E = float(input ("begin E:"))
eps = 0.00001
points = []
def abs_solution(x, I):
    return ((math.exp((-(R*x))/L)*((R**2)*I + R*E*((math.exp((R*x)/L)*math.sin(w*x)))-E*L*w*((math.exp((R*x)/L))*math.cos(w*x)+E*L*w+(L**2)*(w**2)*I)/((R**2)+(L**2)*(w**2)))))
def f(x, I):
    return (E*(math.sin(w * x)) - R * I)/L
def loc_err(step_I, two_step_I):
    return ((two_step_I - step_I) * ((8.0) / 7.0))
def step_func1(step, x, I):
    return step*f(x, I )
def step_func2(step, x, I):
    return step*f(x + step/2, I + step_func1(step, x, I)/2)
def step_func3(step, x, I):
    return step*f(x + step, I + 2*step_func2(step, x, I) - step_func1(step, x ,I))
def next_point_x(step, x):
    return x + step
def next_point_I(I, x, step):
    return I + (step_func1(step, x, I) + 4*step_func2(step, x, I) + step_func3(step, x, I))/6

##################################################
def new_point(step, x, I):

    global new_I
    new_I = I
    global new_x
    new_x = x
    new_I = next_point_I(new_I, new_x, step)
    new_x = next_point_x(step, new_x)

    global tmp_I
    tmp_I = new_I
    global tmp_x
    tmp_x = new_x
    global tmp_h
    tmp_h = step

    print ("func next I:", new_I)
    print ("func next x:", new_x)
    
    global add_I
    add_I = I
    global add_x
    add_x = x
    add_I = next_point_I(add_I, add_x, step/2)
    add_x = next_point_x(step/2, add_x)

    print ("func add I:", add_I)
    print ("func add x:", add_x)

    new_add_I = next_point_I(add_I, add_x, step/2)
    new_add_x = next_point_x(step/2, add_x)

    print ("func next I:", new_add_I)
    print ("func next x:", new_add_x)

    S = loc_err(new_I, new_add_I)

    print("S####: ", S)
    print("exp###: ", eps/16, eps)

    global new_h
    if abs(S) >= eps/16 and abs(S) <= eps:
        print("save point")
        new_h = tmp_h
        return {'coord_I':new_I, 'coord_x':new_x}
    if abs(S) < eps/16:
        print("save point, but change step")
        new_h = 2*tmp_h
        return {'coord_I':new_I, 'coord_x':new_x}
    if abs(S) > eps:
        print("Fail")
        tmp_h = tmp_h/2
        return new_point(tmp_h, tmp_x, tmp_I)

new_x = x0
new_I = I0
add_I = new_I
add_x = new_x
new_h = h
tmp_I = 0.0
tmp_x = 0.0
tmp_h = h
xlist = []
Ilist = []
for i in range(n):
    
    points.append(new_point(new_h, new_x, new_I))

for i in points:
    print(i, '\n')
for i in points:
    xlist.append(i['coord_x'])
    Ilist.append(i['coord_I'])

abs_x = xlist
abs_I = [abs_solution(x, I0) for x in abs_x]

pylab.plot(xlist, Ilist)
pylab.plot(abs_x, abs_I)
pylab.axis([-10, 60, -10, 60])
pylab.grid(True)
pylab.show()