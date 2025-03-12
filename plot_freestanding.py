import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def func(x, a, b):
    return a * x**b

def log_func(x, a, b):
    return np.log(func(x, a, b))

path = "snapshots/960x9600"

with open(path + "/W1.txt", "r") as f:
    lines = f.readlines()
    W1 = []
    for line in lines:
        W1.append(float(line.strip()))
W1 = np.array(W1)

with open(path + "/std_W1.txt", "r") as f:
    lines = f.readlines()
    std_W1 = []
    for line in lines:
        std_W1.append(float(line.strip()))
std_W1 = np.array(std_W1)

with open(path + "/W2.txt", "r") as f:
    lines = f.readlines()
    W2 = []
    for line in lines:
        W2.append(float(line.strip()))
W2 = np.array(W2)

with open(path + "/std_W2.txt", "r") as f:
    lines = f.readlines()
    std_W2 = []
    for line in lines:
        std_W2.append(float(line.strip()))
std_W2 = np.array(std_W2)

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
time = time[:len(W1)]

if path == "snapshots/960x9600":
    time_min1 = 0
    time_max1 = 100000
   

time1 = time[(time_min1<=time) & (time<=time_max1)]
W_1 = W1[(time_min1<=time) & (time<=time_max1)]
# std_W_1 = std_W1[(time_min1<=time) & (time<=time_max1)]
# popt1, pcov1 = curve_fit(log_func, time1, np.log(W_1), p0=[800, 0.0])
# kpz1 = func(time, *popt1)

for is_error in [True, False]:
    plt.figure(dpi=300)
    if is_error:
        plt.errorbar(time, W1, yerr=std_W1, label="KPZ Simulation", color="red", marker=".", linestyle="None", label="up", alpha=0.5)
        plt.errorbar(time, W2, yerr=std_W2, label="KPZ Simulation", color="blue", marker=".", linestyle="None", label="down", alpha=0.5)
        plt.errorbar(time, W, yerr=std_W, label="KPZ Simulation", color="green", marker=".", linestyle="None", label="up - down", alpha=0.5)
        # plt.errorbar(time1, W_1, yerr=std_W_1, color="red", marker=".", linestyle="None")
    else:
        plt.plot(time, W1, label="KPZ Simulation", color="red", marker=".", linestyle="None", label="up")
        plt.plot(time, W2, label="KPZ Simulation", color="blue", marker=".", linestyle="None", label="down")
        plt.plot(time, W, label="KPZ Simulation", color="green", marker=".", linestyle="None", label="up - down")
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

plt.figure(dpi=300)
plt.title("$Cov(H_{top}, H_{bottom})$ %s"%(path.split("/")[1]))
plt.plot(time, (W-(W1+W2))/2, label="Covariance", color="red", marker=".", linestyle="None", label="up")
plt.savefig('cov.png')
plt.close()

with open(path + "/H1.txt", "r") as f:
    lines = f.readlines()
    H1 = []
    for line in lines:
        H1.append(float(line.strip()))
H1 = np.array(H1)

with open(path + "/std_H1.txt", "r") as f:
    lines = f.readlines()
    std_H1 = []
    for line in lines:
        std_H1.append(float(line.strip()))
std_H1 = np.array(std_H1)

with open(path + "/H2.txt", "r") as f:
    lines = f.readlines()
    H2 = []
    for line in lines:
        H2.append(float(line.strip()))
H2 = np.array(H2)

with open(path + "/std_H2.txt", "r") as f:
    lines = f.readlines()
    std_H2 = []
    for line in lines:
        std_H2.append(float(line.strip()))
std_H2 = np.array(std_H2)

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
        plt.errorbar(time, H1, yerr=std_H1, label="KPZ Simulation", color="red", marker=".", linestyle="None", label="up")
        plt.errorbar(time, H2, yerr=std_H2, label="KPZ Simulation", color="blue", marker=".", linestyle="None", label="down")
        plt.errorbar(time, H, yerr=std_H, label="KPZ Simulation", color="green", marker=".", linestyle="None", label="up - down")
    else:
        plt.plot(time, H1, label="KPZ Simulation", color="red", marker=".", linestyle="None", label="up")
        plt.plot(time, H2, label="KPZ Simulation", color="blue", marker=".", linestyle="None", label="down")
        plt.plot(time, H, label="KPZ Simulation", color="green", marker=".", linestyle="None", label="up - down")
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
    if is_error:
        plt.savefig('error_plot.png')
        plt.close()
    else:
        plt.savefig('plot.png')
        plt.close()

time = list(range(0, 100010, 20000))
#time = list(range(100, 510, 100))
#time = list(range(10000, 20010, 1000))
for number in ["1", "2", ""]:
    LW = [[] for t in time]
    std_LW = [[] for t in time]
    for i, t in enumerate(time):
        with open(path + "/%d_LW%s.txt"%(t, number), "r") as f:
            lines = f.readlines()
            for line in lines:
                LW[i].append(float(line.strip()))

        with open(path + "/%d_std_LW%s.txt"%(t, number), "r") as f:
            lines = f.readlines()
            for line in lines:
                std_LW[i].append(float(line.strip()))

    LW = np.array(LW)
    std_LW = np.array(std_LW)

    #time = np.hstack([np.arange(0, 1000, 10), np.arange(1000, 10000, 100), np.arange(10000, 100000,>
    #time = time[:len(W)]
    #time_min = 50
    #time_max = 700

    length = np.array([15*2**i for i in range(0, 7)])

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
        plt.xlabel("length")
        plt.ylabel("Standard Deviation of Heights")
        plt.xscale("log")
        plt.yscale("log")
        plt.legend()
        if is_error:
            plt.savefig('error_L_plot'+number+'.png')
            plt.close()
        else:
            plt.savefig('L_plot'+number+'.png')
            plt.close()

    ave_LW = np.mean(LW, axis=0)
    length_min1 = 25
    length_max1 = 250
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
    plt.xlabel("length")
    plt.ylabel("Average of Standard Deviation of Heights")
    plt.xscale("log")
    plt.yscale("log")
    interval = ave_LW.max()-ave_LW.min()
    plt.ylim(ave_LW.min()-0.1*interval, ave_LW.max()+0.1*interval)
    plt.legend()
    plt.savefig('ave_L_plot'+number+'.png')
