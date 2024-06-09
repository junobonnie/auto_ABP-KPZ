import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def func(x, a, b):
    return a * x**b

def log_func(x, a, b):
    return np.log(func(x, a, b))

with open("snapshots/480x4800/W.txt", "r") as f:
    lines = f.readlines()
    W = []
    for line in lines:
        W.append(float(line.strip()))
W = np.array(W)

with open("snapshots/480x4800/std_W.txt", "r") as f:
    lines = f.readlines()
    std_W = []
    for line in lines:
        std_W.append(float(line.strip()))
std_W = np.array(std_W)

time = np.hstack([np.arange(0, 1000, 10), np.arange(1000, 10000, 100), np.arange(10000, 100000, 1000), np.arange(100000, 1000000, 10000)])
time = time[:len(W)]
time_min = 50
time_max = 700

popt, pcov = curve_fit(log_func, time[(time_min<=time) & (time<=time_max)], np.log(W[(time_min<=time) & (time<=time_max)]))
#kpz = (0.2)*(width_**0.5) * ((time)/width_**1.5)**(1/3)
kpz = func(time, *popt)
plt.figure(dpi=300)
plt.errorbar(time, W, yerr=std_W, label="KPZ Simulation", color="orange", marker=".", linestyle="None")
plt.errorbar(time[(time_min<=time) & (time<=time_max)], W[(time_min<=time) & (time<=time_max)], yerr=std_W[(time_min<=time) & (time<=time_max)], color="red", marker=".", linestyle="None")
#plt.plot(time, W, label="KPZ Simulation", color="orange", marker=".", linestyle="None")
#plt.plot(time[(time_min<=time) & (time<=time_max)], W[(time_min<=time) & (time<=time_max)], color="red", marker=".", linestyle="None")
plt.plot(time, kpz, label="Fitting curve", color="blue")
plt.title("$W=a t^b$, a = %.2f, b = %.5f, std_b = %.5f"%(popt[0], popt[1], np.sqrt(np.diag(pcov))[1]))
plt.legend()
plt.xlabel("time")
plt.ylabel("Standard Deviation of Heights")
plt.xscale("log")
plt.yscale("log")
plt.savefig('log_plot.png')
