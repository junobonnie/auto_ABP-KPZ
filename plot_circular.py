import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def func(x, a, b):
    return a * x**b

def log_func(x, a, b):
    return np.log(func(x, a, b))

# path = "snapshots/132x1320"

# path = "snapshots/60x600"
# path = "snapshots/120x1200"
# path = "snapshots/240x2400"
# path = "snapshots/480x4800"
# path = "snapshots/960x9600"
# path = "snapshots/480x1200"
# path = "snapshots/480x2400"
# path = "snapshots/480x9600"
# path = "snapshots/1920x4800"
path = "snapshots/2880x3200"

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

time = np.hstack([np.arange(500000, 1000000, 10000)])
time = time[:len(W)]

for is_error in [True, False]:
    plt.figure(dpi=300)
    if is_error:
        plt.errorbar(time, W, yerr=std_W, label="KPZ Simulation", color="green", marker=".", linestyle="None", label="circular", alpha=0.5)
        # plt.errorbar(time1, W_1, yerr=std_W_1, color="red", marker=".", linestyle="None")
    else:
        plt.plot(time, W, label="KPZ Simulation", color="green", marker=".", linestyle="None", label="circular")
        # plt.plot(time1, W_1, color="red", marker=".", linestyle="None")
    # plt.plot(time1, kpz1[(time_min1<=time) & (time<=time_max1)], label="%.2f, %.5f, %.5f"%(popt1[0], popt1[1], np.sqrt(np.diag(pcov1))[1]), color="red")
    # plt.plot(time, kpz1, color="red", alpha=0.2)
    plt.title("$W=a t^b$, a, b, std_b, %s"%(path.split("/")[1]))
    plt.legend()
    plt.xlabel("time")
    plt.ylabel("Standard Deviation of Heights")
    #plt.xscale("log")
    #plt.yscale("log")
    # plt.ylim(W.min(), W.max()*1.1)
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

time = list(range(500000, 700010, 10000))
#time = list(range(100, 510, 100))
#time = list(range(10000, 20010, 1000))
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

length = np.array([(np.pi/100)*(2**i) for i in range(1, 8)])

##popt, pcov = curve_fit(log_func, time[(time_min<=time) & (time<=time_max)], np.log(W[(time_min<>
#kpz = (0.2)*(width_**0.5) * ((time)/width_**1.5)**(1/3)
##kpz = func(time, *popt)
ave_LW = np.mean(LW, axis=0)
for is_error in [True, False]:
    plt.figure(dpi=300)
    for i, t in enumerate(time):
        if is_error:
            plt.errorbar(length, LW[i], yerr=std_LW[i], label="t=%ds"%(t), marker=".", linestyle=None, alpha=0.2)
            #plt.errorbar(time[(time_min<=time) & (time<=time_max)], W[(time_min<=time) & (time<=tim>
        else:
            plt.plot(length, LW[i], label="t=%ds"%(t), marker=".", linestyle="None", alpha=0.5)
            #plt.plot(time[(time_min<=time) & (time<=time_max)], W[(time_min<=time) & (time<=time_ma>
   #     plt.plot(time, kpz, label="Fitting curve", color="blue")
    #plt.title("$W=a t^b$, a = %.2f, b = %.5f, std_b = %.5f"%(popt[0], popt[1], np.sqrt(np.diag(>
    #plt.plot(length, length**(1/2), label="slope 1/2", color="red")
    plt.plot(length, ave_LW, label="Average", color="red", marker=".", linestyle="-")
    plt.xlabel("angle")
    plt.ylabel("Standard Deviation of Heights")
    plt.xscale("log")
    plt.yscale("log")
    # plt.legend()
    if is_error:
        plt.savefig('error_L_plot.png')
        plt.close()
    else:
        plt.savefig('L_plot.png')
        plt.close()

ave_LW = np.mean(LW, axis=0)
length_min1 = 0.1
length_max1 = 1.05
length1 = length[(length_min1<=length) & (length<=length_max1)]
ave_LW1 = ave_LW[(length_min1<=length) & (length<=length_max1)]
popt_, pcov_ = curve_fit(log_func, length1, np.log(ave_LW1))
#kpz = (0.2)*(width_**0.5) * ((time)/width_**1.5)**(1/3)
kpz_ = func(length, *popt_)

plt.figure(dpi=300)
plt.plot(length, ave_LW, label="Average", color="red", marker=".", linestyle="None")
plt.plot(length1, ave_LW1, color="blue", marker=".", linestyle="None")
plt.plot(length1, kpz_[(length_min1<=length) & (length<=length_max1)], label="a=%.2f, b=%.5f, std=%.5f"%(popt_[0], popt_[1], np.sqrt(np.diag(pcov_))[1]), color="blue")
plt.plot(length, kpz_, color="blue", alpha=0.2)
plt.title("Average of Standard Deviation of Heights")
plt.xlabel("angle")
plt.ylabel("Average of Standard Deviation of Heights")
plt.xscale("log")
plt.yscale("log")
interval = ave_LW.max()-ave_LW.min()
plt.ylim(ave_LW.min()-0.1*interval, ave_LW.max()+0.1*interval)
plt.legend()
plt.savefig('ave_L_plot.png')


import os
from TracyWidom import TracyWidom

os.system("rm delta_H.txt")
time = list(range(500000, 1000000, 10000))
#time = list(range(100, 510, 100))
#time = list(range(10000, 20010, 1000))
for t in time:
    if t > 700000:
        break

    for i in range(1, 11):
        os.system("cat %s/%03d/%d_H.txt"%(path, i, t) + " >> delta_H.txt")

with open("delta_H.txt", "r") as f:
    lines = f.readlines()
    delta_H = []
    for line in lines:
        delta_H.append(float(line.strip()))
delta_H = np.array(delta_H)

plt.figure(dpi=300)

# plt.hist(delta_H, bins=300, density=True, label='Simulation', histtype='step')
delta_H_pdf = np.histogram(delta_H, bins=300, density=True)

def std(hist):
    bins = hist[1]
    n = hist[0]
    s = 0
    for i in range(len(n)):
        s += n[i] * ((bins[i] + bins[i+1]) / 2) 
    mean = s / np.sum(n)

    t = 0
    for i in range(len(n)):
        t += n[i]*(bins[i] - mean)**2
    std = np.sqrt(t / np.sum(n))
    return std

std = std(delta_H_pdf)
delta_H_pdf = delta_H_pdf[0] * std, delta_H_pdf[1] / std  # normalize
plt.plot(delta_H_pdf[1][:-1], delta_H_pdf[0], label='Simulation', marker="D", linestyle="None", markersize=2)

x = np.linspace(-5, 5, 51)
tw1 = TracyWidom(beta=1) # GOE
tw2 = TracyWidom(beta=2) # GUE
def gaussian(x, mu, sig):
    return (
        1.0 / (np.sqrt(2.0 * np.pi) * sig) * np.exp(-np.power((x - mu) / sig, 2.0) / 2)
    )
std1 = np.sqrt(1.607781034581)
std2 = np.sqrt(0.8131947928329)
plt.plot(x / std1, tw1.pdf(x) * std1, label=r"TW(GOE)($Var=1$)", linestyle="--")
plt.plot(x / std2, tw2.pdf(x) * std2, label=r"TW(GUE)($Var=1$)", linestyle="-.")
plt.plot(x, gaussian(x, 0, 1), label="Gaussian(0, 1)", linestyle="-")

# plt.title("Histogram of delta Hs")
plt.xlabel(r"rescaled $\Delta H = \chi$")
plt.ylabel(r"$\rho(\chi)$")
plt.ylim(bottom = 1e-4, top = 1)
plt.yscale("log")
plt.legend()
plt.savefig('delta_H.png')
