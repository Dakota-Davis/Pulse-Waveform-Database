import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import lfilter
import scipy.signal as signal
from statistics import mode, StatisticsError
import itertools
import operator

		#Average value of a list
def Average(arr):
	Ave = 0
	snum = 0
	for num in range(len(arr)):
		snum += float(arr[num])
	Ave = snum / len(arr)
	return Ave


		#Area under the curve
def Area_under_Curve(c, t):
	auc = np.trapz(y=(c), x=(t))  #Area under the curve
	AuC = np.absolute(auc)
	return AuC


		#Rise Time (Updated Version)
def Rise_Time(v, t):
	involtage = np.negative(v)		#Assists in using max() and ensures a positive returned value
	maxV = max(involtage)
	#print(maxV)
	maxVindex = np.argmax(involtage)
	#print(maxVindex)
	fiveper = 0.05 * maxV			#Finds 5% of max
	#print(fiveper)
	rise = involtage[:maxVindex]		#Makes rising array only until the peak
	for enty in range(len(rise)):	
		if rise[enty] > fiveper:	#Finds index of the first value above 5% max on the rising edge
			idx = enty
			break
	#print(idx)
	risetime = abs(t[maxVindex] - t[idx])	#Calculates time between 5% and max
	#print(time[maxVindex])
	#print(time[idx])
	#print(falltime)
	return risetime

		#Fall Time (Updated Version)
def Fall_Time(v, t):
	involtage = np.negative(v)		#Assists in using max() and ensures a positive returned value
	maxV = max(involtage)
	#print(maxV)
	maxVindex = np.argmax(involtage)
	#print(maxVindex)
	fiveper = 0.05 * maxV			#Finds 5% of max
	#print(fiveper)
	fall = involtage[maxVindex:]		#Makes falling array only after the peak
	for enty in range(len(fall)):
		if fall[enty] < fiveper:	#Finds index of the first value below 5% max on the falling edge
			idx = enty
			break
	#print(idx)
	falltime = abs(t[maxVindex] - t[idx])	#Calculates time between 5% and max
	#print(time[maxVindex])
	#print(time[idx])
	#print(falltime)
	return falltime

	
		#T90 (Shortened Version based on suggestion)
def T90(v, t):
	csum = np.cumsum(v)		#sums values in v
	for s in csum:
		csum = csum / csum[-1]		#normalize the total cumulative sum to 1
	index_array = np.arange(csum.size)

	mask_05 = csum < 0.05		
	t05 = t[mask_05][-1]
	
	mask_95 = csum < 0.95
	t95 = t[mask_95][-1]

	idx_05 = index_array[mask_05][-1]
	idx_95 = index_array[mask_95][-1]
	
	T90 = t95 - t05
	return T90, idx_05, idx_95


		#Exponential Fit
def Expo_Fit(v, t, s, c):
	absvoltage = np.absolute(v)	
	at = np.absolute(t)	
	maxVindex = absvoltage.argmax()
	#print(maxVindex)
	x = at[maxVindex:]		#fit exponential curve -- not working exactly the way I want but appears to be doing something
	y = absvoltage[maxVindex:]

	logy_data = np.log(y)
	curve_fit = np.polyfit(x, logy_data, 1)
	#print(curve_fit)
	yy = np.exp(curve_fit[1]) * np.exp(curve_fit[0]*x)
	#print(yy)
	plt.plot(x, yy, label='Scint {}'.format(s), color='{}'.format(c))
	return



		###SAMPLE T90 CODE FOR CHECKING###
def t90(v, t):							
	vol = np.negative(v)
	c = vol / 50

	i_total = c.sum()

	i_sum = 0.
	t_05 = -1.
	t_95 = -1.
	for j in range(c.size):
		i_sum += c[j]
		frac = i_sum / i_total

		if t_05 < 0. and frac > 0.05:
			t_05 = t[j]
		if t_95 < 0. and frac > 0.95:
			t_95 = t[j]
	t90 = t_95 - t_05
	return t90

		#T90 (Original Version)
def t_90(v, t):
	involtage = np.negative(v)		
	area = 0
	current = involtage / 50		#Gets current from voltage to integrate into charge
	runsum = 0
	runarr = [0] * len(current)
	m = 0

	for m in range(len(current)):			#for loop that approximates area under curve for set
		if m < len(current)-1:
			area = (current[m]) *  abs((t[m+1] - t[m]))
			runsum = runsum + area
			#print(runsum)
			runarr[m] += runsum
			#print(runarr)
			#print(m)
		elif m >= len(current)-1:
			area = (current[m]) * abs(t[m]-t[m-1])
			#print(area)
			runsum = runsum + area
			#print(runsum)
			runarr[m] += runsum
			#print(runarr)
			#print(m)
	#print(runarr)
	#print("The running sum (approx. AuC): " ,runsum, "Coulombs")
	fivesum = 0.05 * runsum
	#print("5% = ",fivesum)
	nifisum = 0.95 * runsum
	#print("95% = ",nifisum)
	w = 0
	fiperer = 0
	fipererarr = [0] * len(runarr)
	nifiperer = 0
	nifipererarr = [0] * len(runarr)

	for w in range(len(runarr)):			#checks percent error between runsum values and 5% (and 95%) of total integral 
		fiperer = abs((runarr[w] - fivesum)/fivesum)
		#print(fiperer)
		nifiperer = abs((runarr[w] - nifisum)/nifisum)
		#print(nifiperer)
		fipererarr[w] += fiperer
		nifipererarr[w] += nifiperer
	fiindex = np.argmin(fipererarr)				#index at which 5% of total runsum is met
	nifiindex = np.argmin(nifipererarr)			#index at which 95% of total runsum is met
	#print("5% index: ",fiindex)
	#print("95% index: ",nifiindex)	
	t90sum = runarr[nifiindex] - runarr[fiindex]		#the '95% - 5% = 90%' of runsum
	ninetypercent = 0.9 * runsum				#expected 90% of runsum (approxed AuC)
	#print("t90sum = ",t90sum)
	#print("ninety percent = ",ninetypercent) 
	T90 = t[nifiindex] - t[fiindex]			#not entirely sure if this is correct but I think the method works well enough

	#print("Checking: " ,auc * .90)				#just to compare the two integration methods for the T90
	
	return T90, fiindex, nifiindex
