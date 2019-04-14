import math
import matplotlib.pyplot as plt
from matplotlib import animation 

# rumus solusi numerik
def calculateX(xBefore, vX, deltaT):
    return xBefore + (vX * deltaT)

def calculateY(yBefore, vY, deltaT):
    return yBefore + (vY * deltaT)

def speedY(speedBefore, deltaT):
    return speedBefore + (-9.8 * deltaT)

# rumus solusi analitik
def analitikX(t, v0, degree):
    return v0 * math.cos(degree) * t

def analitikY(t, v0, degree):
    return ((1/2) * (-9.8) * t ** 2) + (v0 * math.sin(degree) * t)  

# parameter perhitungan
initialSpeed = 15
degree = 15
deltaT = 0.001

# data training free kick dalam meter
highBar = 1.8   
distanceGoal = 18                                 
distanceBar = 9.1
highGoal = 2.4

# mengubah derajat kemiringan ke dalam radion
degree = math.radians(degree)                    

# menghitung nilai solusi numerik
t = [0]
x = [0]
y = [0]

vX = initialSpeed * math.cos(degree)            # menghitung nilai kecepatan terhadap sumbu x
initial_Vy = initialSpeed * math.sin(degree)    # menghitung nilai kecepatan awal terhadap sumbu y

vY = [initial_Vy]

i = 0
highBall_at_bar = 0                             # ketinggian bola saat mencapai bar
highBall_at_goal = 0                            # ketinggian bola saat mencapai gawang

while (math.degrees(degree) <= 70):
    initialSpeed = 15

    while (initialSpeed <= 60):
        
        t = [0]
        x = [0]
        y = [0]

        vX = initialSpeed * math.cos(degree)            # menghitung nilai kecepatan terhadap sumbu x
        initial_Vy = initialSpeed * math.sin(degree)    # menghitung nilai kecepatan awal terhadap sumbu y

        vY = [initial_Vy]
        i = 0

        highBall_at_bar = 0
        highBall_at_goal = 0

        while True:
            i += 1
            t.append(t[i-1] + deltaT)
            x.append( calculateX(x[i-1], vX, deltaT) )
            vY.append( speedY(vY[i-1], deltaT) )
            y.append( calculateY(y[i-1], vY[i], deltaT) )

            # mendapatkan ketinggian bola saat mencapai bar
            if (x[i] - distanceBar <= 0.1):
                highBall_at_bar = y[i]

            # mendapatkan ketinggian bola saat mencapai gawang
            if (x[i] - distanceGoal <= 0.1):
                highBall_at_goal = y[i]

            # ketika ketinggan sudah kurang dari 0
            if (y[i] <= 0):
                y.pop(i)
                x.pop(i)
                t.pop(i)
                vY.pop(i)
                break

        if (max(x) > distanceGoal and highBall_at_bar > highBar and highBall_at_goal < highGoal):
            print('Goal with max x = {} and high ball at bar position = {} and high ball at goal position = {}'.format( max(x), highBall_at_bar, highBall_at_goal ))
            break
        else:
            print('Failed, Calculating Again, current initialSpeed = {} and degree = {}'.format( initialSpeed, math.degrees(degree) ))
            initialSpeed += 0.1

    if (max(x) > distanceGoal and highBall_at_bar > highBar and highBall_at_goal < highGoal):
        break
    else:
        degree += math.radians(0.1)
        

# menghitung nilai solusi numerik
t_analitik = [0]
x_analitik = [0]
y_analitik = [0]

i = 0

max_x = 0
max_y = 0


while True:
    i += 1
    t_analitik.append(t_analitik[i-1] + deltaT)
    x_analitik.append( analitikX(t_analitik[i], initialSpeed, degree) )
    y_analitik.append( analitikY(t_analitik[i], initialSpeed, degree) )
    if (y_analitik[i] <= 0):
        x_analitik.pop(i)
        y_analitik.pop(i)
        i -= 1
        x_analitik.pop(i)
        y_analitik.pop(i)
        break


# membuat animasi
fig = plt.figure()
ax = plt.axes(xlim=(0, round(max(x))), ylim=(0, 8))
# ax = plt.axvline(x=9.1)
line, = ax.plot([9.1 , 9.1] , [0 , 1.7])
line2, = ax.plot([18, 18],[0,2.5])
dot, = ax.plot([], [], 'ro', color='red')
dot2, = ax.plot([], [], 'ro', color='blue')


def init():
    dot.set_data([], [])
    return dot,

def init2():
    dot2.set_data([], [])
    return dot2,

def animate(i):
    dot.set_data(x[i], y[i])
    return dot,

def animate2(i):
    dot2.set_data(x_analitik[i], y_analitik[i])
    return dot2,

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(x), interval=1)
anim2 = animation.FuncAnimation(fig, animate2, init_func=init2, frames=len(x_analitik), interval=1)

plt.show()


