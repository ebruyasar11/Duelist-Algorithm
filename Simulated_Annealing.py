import numpy as np
import matplotlib.pyplot as plt
import random
import math

# define objective function

def f(x):
    x1 = x[0]
    x2 = x[1]
    obj = -20*math.exp(-0.2*math.sqrt(0.5*(x1*x1*x2*x2)))-math.exp(0.5*(math.cos(2*math.pi*x1)+math.cos(2*math.pi*x2))) + math.e + 20
    return obj

#İstenilen test fonksiyonu, f isimli fonksiyonda obj olarak kullanılabilir.

#ackley    obj = -20*math.exp(-0.2*math.sqrt(0.5*(x1*x1*x2*x2)))-math.exp(0.5*(math.cos(2*math.pi*x1)+math.cos(2*math.pi*x2))) + math.e + 20
#beale     obj = (1.5 - x[0] + x[0]*x[1])**2 + (2.25 - x[0] + x[0]*x[1]**2)**2 + (2.625 - x[0] + x[0]*x[1]**3)**2
#goldstein obj = ((1 + (x[0] + x[1] + 1) ** 2 * (19 - 14 * x[0] + 3 * (x[0] ** 2) - 14 * x[1] + 6 * x[0] * x[1] + 3 * (x[1] ** 2))) * (30 + (2 * x[0] - 3 * x[1]) ** 2 * (18 - 32 * x[0] + 12 * (x[0] ** 2) + 48 * x[1] - 36 * x[0] * x[1] + 27 * (x[1] ** 2))))
#levi      obj = (math.sin(3*x[0]*math.pi))**2 + ((x[0] - 1)**2)*(1 + math.sin(3*x[1]*math.pi)**2) + ((x[1] - 1)**2)*(1 + math.sin(2*x[1]*math.pi)**2)


# Start location
x_start = [0.8, -0.5]

##################################################
# Simulated Annealing
##################################################
# Number of cycles
n = 100
# Number of trials per cycle
m = 100
# Number of accepted solutions
na = 0.0
# Probability of accepting worse solution at the start
p1 = 0.7
# Probability of accepting worse solution at the end
p50 = 0.001
# Initial temperature
t1 = -1.0/math.log(p1)
# Final temperature
t50 = -1.0/math.log(p50)
# Fractional reduction every cycle
frac = (t50/t1)**(1.0/(n-1.0))
# Initialize x
x = np.zeros((n+1,2))
x[0] = x_start
xi = np.zeros(2)
xi = x_start
na = na + 1.0
# Current best results so far
xc = np.zeros(2)
xc = x[0]
fc = f(xi)
fs = np.zeros(n+1)
fs[0] = fc
# Current temperature
t = t1
# DeltaE Average
DeltaE_avg = 0.0
for i in range(n):
    print('Cycle: ' + str(i) + ' with Temperature: ' + str(t))
    for j in range(m):
        # Generate new trial points
        xi[0] = xc[0] + random.random() - 0.5
        xi[1] = xc[1] + random.random() - 0.5
        # Clip to upper and lower bounds
        xi[0] = max(min(xi[0],1.0),-1.0)
        xi[1] = max(min(xi[1],1.0),-1.0)
        DeltaE = abs(f(xi)-fc)
        if (f(xi)>fc):
            # Initialize DeltaE_avg if a worse solution was found
            #   on the first iteration
            if (i==0 and j==0): DeltaE_avg = DeltaE
            # objective function is worse
            # generate probability of acceptance
            p = math.exp(-DeltaE/(DeltaE_avg * t))
            # determine whether to accept worse point
            if (random.random()<p):
                # accept the worse solution
                accept = True
            else:
                # don't accept the worse solution
                accept = False
        else:
            # objective function is lower, automatically accept
            accept = True
        if (accept==True):
            # update currently accepted solution
            xc[0] = xi[0]
            xc[1] = xi[1]
            fc = f(xc)
            # increment number of accepted solutions
            na = na + 1.0
            # update DeltaE_avg
            DeltaE_avg = (DeltaE_avg * (na-1.0) +  DeltaE) / na
    # Record the best x values at the end of every cycle
    x[i+1][0] = xc[0]
    x[i+1][1] = xc[1]
    fs[i+1] = fc
    # Lower the temperature for next cycle
    t = frac * t

# print solution
print('Best solution: ' + str(xc))
print('Best objective: ' + str(fc))

plt.plot(x[:,0],x[:,1],'y-o')
plt.savefig('contour.png')

fig = plt.figure()
ax1 = fig.add_subplot(211)
ax1.plot(fs,'r.-')
ax1.legend(['Objective'])
ax2 = fig.add_subplot(212)
ax2.plot(x[:,0],'b.-')
ax2.plot(x[:,1],'g--')
ax2.legend(['x1','x2'])

# Save the figure as a PNG
plt.savefig('iterations.png')

plt.show()
