import matplotlib.pyplot as plt
import math
import numpy
vmax = 117.6
c = 4.418	#in mF
resistor = [100, 120, 150, 180, 220, 270, 330, 390]
peak_power = []
time = []
time_ov = []
ovload_x = []
ovload_ovhead = []
ovload_max = []
rms = []

R_data =[]

R_ovload_model = [[25, 25, 12.5, 10, 7.5, 6.5, 5, 2.5], [0.1, 1, 2, 2.75, 3.5, 4, 5, 10]]  # [multiplier], [time in s]

def find_resistor(vmax, C, R_power, percent=96):
	C = C/1000
	percent /= 100
	# to account for diode, worst case
	percent = (percent * vmax)/(vmax - 1)
	for i in range(len(resistor)):
		R = resistor[i]
		t = -R*C*math.log(1-percent)
		power = round(vmax**2/resistor[i], 2)
		peak_power.append(power)
		time.append(t)
		no_ov_v = vmax-(R*R_power)**0.5
		t_no_ov = round(-R*C*math.log(1-no_ov_v/vmax),2)
		time_ov.append(t_no_ov)
		safety_timer  = round(5*R*C,2) # for safety shutdown timer
		ov = round(power/R_power,2)
		ovload_x.append(ov)
		R_data.append([R, power, round(t,2), t_no_ov, safety_timer, ov])
		vt2 = []
		
		for tt in numpy.linspace(0,t,2000):
			vt2.append((vmax*(pow(math.e,-tt/(R*C))))**2)
		rms.append(round((math.sqrt(numpy.mean(vt2))**2)/R,2))
			
		for j in range(len(R_ovload_model[1])-1):
			if time[i] > R_ovload_model[1][j] and time[i] < R_ovload_model[1][j+1]:
				x1, x2 = R_ovload_model[1][j], R_ovload_model[1][j+1]
				y1, y2 = R_ovload_model[0][j], R_ovload_model[0][j+1]
				y = (time[i]-x1)*(y1-y2)/(x1-x2)+y1
				ovhead = y-ovload_x[i]
				ovload_max.append(y)
				ovload_ovhead.append(ovhead)
				R_data[i].append(ovhead)
	
		print(R, "  P_peak (W):", round(power,2), "\tT (s):",round(t,2), "\t\tOvLoad (s):", t_no_ov)
		print("      Ovload_x:", ov, "\t\tOvload_max_x:", round(ovload_max[i], 2), "\tOvHead (W):", round(ovhead*R_power,2))
		print("      P_RMS (W):", rms[i], "\t\tSafety_Timer (s):",round(safety_timer, 2))
		print()
		
find_resistor(vmax, c, 12.5)
	
#plt.plot(resistor, peak_power)
#plt.xticks(resistor)
#plt.yticks(peak_power)
#plt.title("Peak Power")
#plt.show()
#plt.title("Overload End Time vs Resistor")
#plt.plot(resistor, time_ov)
#plt.xticks(resistor)
#plt.yticks(time_ov)
#plt.show()
