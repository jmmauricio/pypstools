import numpy as np
import matplotlib.pyplot as plt

x = np.arange(4)
y = x
t = [1.0,0.9,0.95,1.05]
s = np.array([1.0,0.9,0.95,1.05])*100
plt.scatter(x, y, c=t, s=s, alpha = 0.5)
plt.colorbar()
plt.show()
