import matplotlib.pyplot as plt 
import numpy as np 

x = np.arange(0, 5*np.pi, 0.1*np.pi)
y = np.asin(x)
plt.plot(x, y, color= 'black')
plt.xlabel("x")
plt.ylabel("y")
plt.show()