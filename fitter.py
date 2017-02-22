from gpfit.fit import fit
from numpy import logspace, log, log10, random
import numpy as np
import matplotlib.pyplot as plt
# fixed initial guess for fitting
# random.seed(33404)

mdot = np.array([0.001411400768,0.04734265813,
0.1014552215])
delta_p_inv = np.array([1121.643023,908.6306982,
29.95485818])
K = 1

x = log(mdot)
y = log(delta_p_inv)

# plt.plot(mdot,delta_p)
# plt.show()
cMA, errorMA = fit(x,y, K, "MA")
cSMA, errorSMA = fit(x, y, K, "SMA")
# cISMA, errorISMA = fit(x, y, K, "ISMA")

print "MA RMS Error: %.5g" % errorMA
print "SMA RMS Error: %.5g" % errorSMA
# print "ISMA RMS Error: %.5g" % errorISMA