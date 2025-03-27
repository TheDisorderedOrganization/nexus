from math import sin
import matplotlib.pyplot as plt

# construire les listes de valeurs
start = -5
end = 6
num = 200
dx = (end-start)/num

x = []
y = []
while start < end:
    this_x = start+dx
    this_y = sin(this_x)
    x.append(this_x)
    y.append(this_y)
    start += dx

# faire le graphe
plt.title('Mon premier graphe')
plt.xlabel('x')
plt.ylabel('y=sin(x)')

plt.plot(x,y,'+')
plt.show()