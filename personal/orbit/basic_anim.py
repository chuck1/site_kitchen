import numpy as np
from matplotlib import pyplot as plt

fig = plt.figure()
ax = plt.axes( xlim=(0,2), ylim=(-2,2) )
line, = ax.plot([],[],lw=2)

def init():
	line.set_data([],[])
	return line,

def animate(i):
	x = np.linspace(0,2,1000)
	y = np.sin(2 * np.pi * (x - 0.01 * i))
	line.set_data(x,y)
	return line,

anim = animation.FuncAnimation(fig, animate, init_func=init, frame=200, interval=20, blit=True)

anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()



