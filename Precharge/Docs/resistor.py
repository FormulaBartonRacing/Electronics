import matplotlib.pyplot as plt
import math
import numpy
vmax = 117.6
c = 4.418	#in mF
resistor = [100, 120, 150, 180, 210, 270, 330, 390]
peak_power = []
time = []
time_ov = []

R_ovload_model = [[25, 12.5, 10, 7.5, 5], [1, 2, 2.75, 3.5, 4.7]]  
				 # [multiplier], [time in s]

def find_resistor(vmax, C, R_power, percent=97.4):
	C = C/1000
	for i in range(len(resistor)):
		R = resistor[i]
		t = -R*C*math.log(1-percent/100)
		power = round(vmax**2/resistor[i], 2)
		peak_power.append(power)
		time.append(t)
		no_ov_v = vmax-(R*R_power)**0.5
		t_no_ov = round(-R*C*math.log(1-no_ov_v/vmax),2)
		time_ov.append(t_no_ov)
		safety_timer  = round(5*R*C,2) # for safety shutdown timer
		print(R, "  P_peak:", power, "  T:",round(t,2), "  OvLoad:", t_no_ov, "  Safety_Timer:", safety_timer)
		print("      Overload_x:", power/R_power)
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
