import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def func(x, a, b):
    return a * x**b

def log_func(x, a, b):
    return np.log(func(x, a, b))

path = "snapshots/60x600"
# path = "snapshots/120x1200"
# path = "snapshots/240x2400"
# path = "snapshots/480x4800"
# path = "snapshots/960x9600"
# path = "snapshots/480x1200"
# path = "snapshots/480x2400"
# path = "snapshots/480x9600"
# path = "snapshots/1920x4800"

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

if path == "snapshots/60x600":
    time_min1 = 100
    time_max1 = 500
    time_min2 = 600
    time_max2 = 1000
    time_min3 = 2000
    time_max3 = 100000

elif path == "snapshots/120x1200":
    time_min1 = 100
    time_max1 = 1000
    time_min2 = 1500
    time_max2 = 3000
    time_min3 = 4000
    time_max3 = 6000

elif path == "snapshots/240x2400":
    time_min1 = 100
    time_max1 = 1000
    time_min2 = 2000
    time_max2 = 5000
    time_min3 = 6000
    time_max3 = 15000

elif path == "snapshots/480x4800":
    time_min1 = 100
    time_max1 = 500
    time_min2 = 1000
    time_max2 = 4000
    time_min3 = 5000
    time_max3 = 30000

elif path == "snapshots/960x9600":
    time_min1 = 100
    time_max1 = 500
    time_min2 = 1000
    time_max2 = 4000
    time_min3 = 8000
    time_max3 = 20000
    
elif path == "snapshots/480x1200":
    time_min1 = 100
    time_max1 = 400
    time_min2 = 800
    time_max2 = 3000
    time_min3 = 5000
    time_max3 = 10000

elif path == "snapshots/480x2400":
    time_min1 = 100
    time_max1 = 500
    time_min2 = 1000
    time_max2 = 4000
    time_min3 = 8000
    time_max3 = 20000

elif path == "snapshots/480x9600":
    time_min1 = 100
    time_max1 = 500
    time_min2 = 1000
    time_max2 = 4000
    time_min3 = 5000
    time_max3 = 20000

elif path == "snapshots/1920x4800":
    time_min1 = 100
    time_max1 = 500
    time_min2 = 1000
    time_max2 = 4000
    time_min3 = 8000
    time_max3 = 20000

time1 = time[(time_min1<=time) & (time<=time_max1)]
W1 = W[(time_min1<=time) & (time<=time_max1)]
std_W1 = std_W[(time_min1<=time) & (time<=time_max1)]
popt1, pcov1 = curve_fit(log_func, time1, np.log(W1))
#kpz = (0.2)*(width_**0.5) * ((time)/width_**1.5)**(1/3)
kpz1 = func(time, *popt1)

time2 = time[(time_min2<=time) & (time<=time_max2)]
W2 = W[(time_min2<=time) & (time<=time_max2)]
std_W2 = std_W[(time_min2<=time) & (time<=time_max2)]
popt2, pcov2 = curve_fit(log_func, time2, np.log(W2))
#kpz = (0.2)*(width_**0.5) * ((time)/width_**1.5)**(1/3)
kpz2 = func(time, *popt2)

time3 = time[(time_min3<=time) & (time<=time_max3)]
W3 = W[(time_min3<=time) & (time<=time_max3)]
std_W3 = std_W[(time_min3<=time) & (time<=time_max3)]
popt3, pcov3 = curve_fit(log_func, time3, np.log(W3))
#kpz = (0.2)*(width_**0.5) * ((time)/width_**1.5)**(1/3)
kpz3 = func(time, *popt3)

for is_error in [True, False]:
    plt.figure(dpi=300)
    if is_error:
        plt.errorbar(time, W, yerr=std_W, label="KPZ Simulation", color="orange", marker=".", linestyle="None")
        plt.errorbar(time1, W1, yerr=std_W1, color="red", marker=".", linestyle="None")
        plt.errorbar(time2, W2, yerr=std_W2, color="green", marker=".", linestyle="None")
        plt.errorbar(time3, W3, yerr=std_W3, color="blue", marker=".", linestyle="None")
    else:
        plt.plot(time, W, label="KPZ Simulation", color="orange", marker=".", linestyle="None")
        plt.plot(time1, W1, color="red", marker=".", linestyle="None")
        plt.plot(time2, W2, color="green", marker=".", linestyle="None")
        plt.plot(time3, W3, color="blue", marker=".", linestyle="None")
    plt.plot(time1, kpz1[(time_min1<=time) & (time<=time_max1)], label="%.2f, %.5f, %.5f"%(popt1[0], popt1[1], np.sqrt(np.diag(pcov1))[1]), color="red")
    plt.plot(time2, kpz2[(time_min2<=time) & (time<=time_max2)], label="%.2f, %.5f, %.5f"%(popt2[0], popt2[1], np.sqrt(np.diag(pcov2))[1]), color="green")
    plt.plot(time3, kpz3[(time_min3<=time) & (time<=time_max3)], label="%.2f, %.5f, %.5f"%(popt3[0], popt3[1], np.sqrt(np.diag(pcov3))[1]), color="blue")
    plt.plot(time, kpz1, color="red", alpha=0.2)
    plt.plot(time, kpz2, color="green", alpha=0.2)
    plt.plot(time, kpz3, color="blue", alpha=0.2)
    plt.title("$W=a t^b$, a, b, std_b, %s"%(path.split("/")[1]))
    plt.legend()
    plt.xlabel("time")
    plt.ylabel("Standard Deviation of Heights")
    plt.xscale("log")
    plt.yscale("log")
    plt.ylim(W.min(), W.max())
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

V = []
time_  = []
for i in range(len(H)-1):
    V.append((H[i+1] - H[i])/(time[i+1]-time[i]))
    time_.append((time[i+1]+time[i])/2)

plt.figure(dpi=300)
plt.plot(time_, V, label="KPZ Simulation", color="red", marker=".", linestyle="None")
plt.title("Velocity of Average of Heights")
plt.xlabel("time")
plt.ylabel("Velocity of Average of Heights")
plt.xscale("log")
plt.yscale("log")
plt.savefig('v-plot.png')
plt.close()

time = list(range(100000, 1000010, 100000))
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

length = np.array(list(range(2, 96+1)))

##popt, pcov = curve_fit(log_func, time[(time_min<=time) & (time<=time_max)], np.log(W[(time_min<>
#kpz = (0.2)*(width_**0.5) * ((time)/width_**1.5)**(1/3)
##kpz = func(time, *popt)

for is_error in [True, False]:
    plt.figure(dpi=300)
    for i, t in enumerate(time):
        if is_error:
            plt.errorbar(length, LW[i], yerr=std_LW[i], label="t=%ds"%(t), marker=".", linestyle=None)
            #plt.errorbar(time[(time_min<=time) & (time<=time_max)], W[(time_min<=time) & (time<=tim>
        else:
            plt.plot(length, LW[i], label="t=%ds"%(t), marker=".", linestyle="None")
            #plt.plot(time[(time_min<=time) & (time<=time_max)], W[(time_min<=time) & (time<=time_ma>
   #     plt.plot(time, kpz, label="Fitting curve", color="blue")
    #plt.title("$W=a t^b$, a = %.2f, b = %.5f, std_b = %.5f"%(popt[0], popt[1], np.sqrt(np.diag(>
    #plt.plot(length, length**(1/2), label="slope 1/2", color="red")
    plt.xlabel("length")
    plt.ylabel("Standard Deviation of Heights")
    plt.xscale("log")
    plt.yscale("log")
    plt.legend()
    if is_error:
        plt.savefig('error_L_plot.png')
        plt.close()
    else:
        plt.savefig('L_plot.png')
        plt.close()
