import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def func(x, a, b):
    return a * x**b

def log_func(x, a, b):
    return np.log(func(x, a, b))

path = "snapshots/480x4800"



with open(path + "/W.txt", "r") as f:
    lines = f.readlines()
    W = []
    for line in lines:
        W.append(float(line.strip()))
W = np.array(W)

with open(path + "/std_W.txt", "r") as f:
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

for is_error in [True, False]:
    plt.figure(dpi=300)
    if is_error:
        plt.errorbar(time, W, yerr=std_W, label="KPZ Simulation", color="orange", marker=".", linestyle="None")
        plt.errorbar(time[(time_min<=time) & (time<=time_max)], W[(time_min<=time) & (time<=time_max)], yerr=std_W[(time_min<=time) & (time<=time_max)], color="red", marker=".", linestyle="None")
    else:
        plt.plot(time, W, label="KPZ Simulation", color="orange", marker=".", linestyle="None")
        plt.plot(time[(time_min<=time) & (time<=time_max)], W[(time_min<=time) & (time<=time_max)], color="red", marker=".", linestyle="None")
    plt.plot(time, kpz, label="Fitting curve", color="blue")
    plt.title("$W=a t^b$, a = %.2f, b = %.5f, std_b = %.5f"%(popt[0], popt[1], np.sqrt(np.diag(pcov))[1]))
    plt.legend()
    plt.xlabel("time")
    plt.ylabel("Standard Deviation of Heights")
    plt.xscale("log")
    plt.yscale("log")
    if is_error:
        plt.savefig('error_log_plot.png')
        plt.close()
    else:
        plt.savefig('log_plot.png')
        plt.close()


with open(path + "/H.txt", "r") as f:
    lines = f.readlines()
    H = []
    for line in lines:
        H.append(float(line.strip()))
H = np.array(H)

with open(path + "/std_H.txt", "r") as f:
    lines = f.readlines()
    std_H = []
    for line in lines:
        std_H.append(float(line.strip()))
std_H = np.array(std_H)

for is_error in [True, False]:
    plt.figure(dpi=300)
    if is_error:
        plt.errorbar(time, H, yerr=std_H, label="KPZ Simulation", color="orange", marker=".", linestyle="None")
        #plt.errorbar(time[(time_min<=time) & (time<=time_max)], W[(time_min<=time) & (time<=time_max)], yerr=std_W[(time_min<=time) & (time<=time_max)], color="red", marker=".", linestyle="None")
    else:
        plt.plot(time, H, label="KPZ Simulation", color="orange", marker=".", linestyle="None")
        #plt.plot(time[(time_min<=time) & (time<=time_max)], W[(time_min<=time) & (time<=time_max)], color="red", marker=".", linestyle="None")
    #plt.plot(time, kpz, label="Fitting curve", color="blue")
    #plt.title("$W=a t^b$, a = %.2f, b = %.5f, std_b = %.5f"%(popt[0], popt[1], np.sqrt(np.diag(pcov))[1]))
    #plt.legend()
    plt.title("Average of Heights")
    plt.xlabel("time")
    plt.ylabel("Average of Heights")
    plt.xscale("log")
    plt.yscale("log")
    if is_error:
        plt.savefig('error_plot.png')
        plt.close()
    else:
        plt.savefig('plot.png')
        plt.close()

time = time = list(range(1000, 10010, 1000))
LW = [[] for t in time]
std_LW = [[] for t in time]
for i, t in enumerate(time):
    with open(path + "/%d_LW.txt"%(t), "r") as f:
        lines = f.readlines()
        for line in lines:
            LW[i].append(float(line.strip()))

    with open(path + "/%d_std_LW.txt"%(t), "r") as f:
        lines = f.readlines()
        for line in lines:
            std_LW[i].append(float(line.strip()))

LW = np.array(LW)
std_LW = np.array(std_LW)

#time = np.hstack([np.arange(0, 1000, 10), np.arange(1000, 10000, 100), np.arange(10000, 100000,>
#time = time[:len(W)]
#time_min = 50
#time_max = 700

length = list(range(2, 96+1))

##popt, pcov = curve_fit(log_func, time[(time_min<=time) & (time<=time_max)], np.log(W[(time_min<>
#kpz = (0.2)*(width_**0.5) * ((time)/width_**1.5)**(1/3)
##kpz = func(time, *popt)

for is_error in [True, False]:
    plt.figure(dpi=300)
    for i, t in enumerate(reversed(time)):
        if is_error:
            plt.errorbar(length, LW[i], yerr=std_LW[i], label="t=%ds"%(t), marker=".", linestyle=None)
            #plt.errorbar(time[(time_min<=time) & (time<=time_max)], W[(time_min<=time) & (time<=tim>
        else:
            plt.plot(length, LW[i], label="t=%ds"%(t), marker=".", linestyle="None")
            #plt.plot(time[(time_min<=time) & (time<=time_max)], W[(time_min<=time) & (time<=time_ma>
   #     plt.plot(time, kpz, label="Fitting curve", color="blue")
    #plt.title("$W=a t^b$, a = %.2f, b = %.5f, std_b = %.5f"%(popt[0], popt[1], np.sqrt(np.diag(>
    plt.legend()
    plt.xlabel("length")
    plt.ylabel("Standard Deviation of Heights")
    plt.xscale("log")
    plt.yscale("log")
    if is_error:
        plt.savefig('error_L_plot.png')
        plt.close()
    else:
        plt.savefig('L_plot.png')
        plt.close()
