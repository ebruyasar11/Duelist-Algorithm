from Duelist_Algorithm import Duelist_Algorithm
import math

def f(x1,x2):
	x = []
	x.append(x1)
	x.append(x2)
	obj = (math.sin(3*x[0]*math.pi))**2 + ((x[0] - 1)**2)*(1 + math.sin(3*x[1]*math.pi)**2) + ((x[1] - 1)**2)*(1 + math.sin(2*x[1]*math.pi)**2)
	return obj

#İstenilen test fonksiyonu, f isimli fonksiyonda obj olarak kullanılabilir.

#ackley    obj = -20*math.exp(-0.2*math.sqrt(0.5*(x1*x1*x2*x2)))-math.exp(0.5*(math.cos(2*math.pi*x1)+math.cos(2*math.pi*x2))) + math.e + 20
#beale     obj = (1.5 - x[0] + x[0]*x[1])**2 + (2.25 - x[0] + x[0]*x[1]**2)**2 + (2.625 - x[0] + x[0]*x[1]**3)**2
#goldstein obj = ((1 + (x[0] + x[1] + 1) ** 2 * (19 - 14 * x[0] + 3 * (x[0] ** 2) - 14 * x[1] + 6 * x[0] * x[1] + 3 * (x[1] ** 2))) * (30 + (2 * x[0] - 3 * x[1]) ** 2 * (18 - 32 * x[0] + 12 * (x[0] ** 2) + 48 * x[1] - 36 * x[0] * x[1] + 27 * (x[1] ** 2))))
#levi      obj = (math.sin(3*x[0]*math.pi))**2 + ((x[0] - 1)**2)*(1 + math.sin(3*x[1]*math.pi)**2) + ((x[1] - 1)**2)*(1 + math.sin(2*x[1]*math.pi)**2)

x=["x1","x2"]
xmin=[-10,-10]
xmax=[10,10]

DA = Duelist_Algorithm(f,x,xmin,xmax,iterasyon=100)
DA.baslangic()
