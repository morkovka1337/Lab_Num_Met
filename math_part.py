import math

#######################################

n = int(input("Enter count repeat: "))
L = float(input ("begin L:"))
I0 = float(input ("begin I0:"))
h = float(input ("begin step:"))
x0 = float(input ("begin x:"))
R = float(input ("begin R:"))
w = float(input ("begin w:"))
E = float(input ("begin E:"))
exp = 0.00001
points = []
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
    print("exp###: ", exp/16, exp)

    global new_h
    if abs(S) >= exp/16 and abs(S) <= exp:
        print("save point")
        new_h = h
        return (new_I, new_x)
    if abs(S) < exp/16:
        print("save point, but change step")
        new_h = 2*h
        return (new_I, new_x)
    if abs(S) > exp:
        print("Fail")
        curr_h = tmp_h/2
        return new_point(curr_h, tmp_x, tmp_I)

new_x = x0
new_I = I0
add_I = new_I
add_x = new_x
new_h = h
tmp_I = 0.0
tmp_x = 0.0
tmp_h = h
for i in range(n):
    
    points.append(new_point(new_h, new_x, new_I))

for i in points:

    print(i, '\n')
