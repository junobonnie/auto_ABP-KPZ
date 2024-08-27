import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def func(x, a, b):
    return a * x**b

def log_func(x, a, b):
    return np.log(func(x, a, b))

paths = ["60x600","120x1200","240x2400","480x4800","480x1200","480x2400"]
plt.figure(dpi=300)
for path in paths:
    with open("snapshots/" + path + "/H.txt", "r") as f:
        lines = f.readlines()
        H = []
        for line in lines:
            H.append(float(line.strip()))
    H = np.array(H)-int(path.split("x")[1])/10
    time = np.hstack([np.arange(0, 1000, 10), np.arange(1000, 10000, 100), np.arange(10000, 100000, 1000), np.arange(100000, 1000000, 10000)])
    time = time[:len(H)]
    plt.plot(time, H, label=path, marker="None")#, linestyle="None")
    #plt.plot(time[(time_min<=time) & (time<=time_max)], W[(time_min<=time) & (time<=time_max)], color="red", marker=".", linestyle="None")
    #plt.plot(time, kpz, label="Fitting curve", color="blue")
    #plt.title("$W=a t^b$, a = %.2f, b = %.5f, std_b = %.5f"%(popt[0], popt[1], np.sqrt(np.diag(pcov))[1]))
    #plt.legend()
    plt.title("Average of Heights")
    plt.xlabel("time")
    plt.ylabel("Average of Heights")
    plt.xscale("log")
    plt.yscale("log")
    plt.legend()
plt.savefig('all_plot.png')
plt.close()
