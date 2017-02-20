# http://kashanu.ac.ir/Files/Content/Heat%20transfer-incropra.pdf
from gpkit import Model, Variable
import gpkit
import numpy as np
import matplotlib.pyplot as plt
import math


# MKS unit system
# Assumptions:
# equilateral geometry
# chi stays around 1.1 because of the operating range of reynolds (only varies between 1 and 1.05)
# Friction factor was taken along the P_T/D = 1.25 line, whereas it is actually closer to the 1.09 (this may lead to a decent underestimation of pressure drop)
# 0-1000 Pa difference operating range


mdot = Variable("mdot",np.linspace(1e-3,1e-2,100),"kg/s","flow rate in")
S_inlet = Variable("S_inlet",0.2523*0.401550,"m^2","Cross sectional area of inlet")

S_T = Variable("S_T",0.0202,"m")
S_L = Variable("S_L",0.0202,"m")
S_D = Variable("S_D",0.0202,"m")
D = Variable("D",0.0184,"m")
delta_p = Variable("delta_p","Pa","total pressure difference across pack")
N_L = Variable("N_L",12,"-","number of rows")
Re_Dmax = Variable("Re_Dmax","-")
V = Variable("V","m/s","inlet flow velocity")
chi = Variable("chi",1.1,"-","correction factor?")
rho = Variable("rho",1.225,"kg/m^3","air density at sea level")
V_max = Variable("V_max","m/s")
f = Variable("f","-","friction factor")
A = Variable("A","m","gap between cells (wall to wall)")
mu = Variable("mu",1.983e-5,"Pa*s")

with gpkit.SignomialsEnabled():
	constraints = [f >=1542.963*Re_Dmax**(-0.1678948),
				   Re_Dmax == V_max*rho*D/mu,
				   V == mdot/(S_inlet*rho),
				   A <= S_T - D,
				   V_max >= S_T*V/(A),
				   delta_p >= N_L*chi*((rho*V_max**2)/2)*f]

objective = delta_p
m = Model(objective,constraints)
sol = m.solve(verbosity=0)
print sol(delta_p)
print sol.table()

if sol(Re_Dmax).any() >= 1e6:
	print "REYNOLDS TOO HIGH, INVALID ASSUMPTION ON CHI"

plt.scatter(sol(mdot), sol(delta_p))
plt.xlabel("mdot (kg/s)")
plt.ylabel("delta_p or backpressure (Pa)")
plt.show()

# def drawPack(S_T,S_L,S_D,D):
# 	# Drawing clockwise from lower left corner
# 	# x = [0,0,S_L,S_L]
# 	# y = [0,S_T,S_T+math.sqrt(S_D**2-S_L**2),math.sqrt(S_D**2-S_L**2)]
# 	# colors = [150,150,150,150]
# 	# area = np.pi * (D/2)**2  # 0 to 15 point radii

# 	# plt.scatter(x, y, s=area, c=colors, alpha=0.5)
# 	# plt.show()

# 	circle1 = plt.Circle((0, 0), D, color='r')
# 	circle2 = plt.Circle((0, S_T), D, color='g')
# 	circle3 = plt.Circle((S_L, S_T+math.sqrt(S_D**2-S_L**2)), D, color='blue')
# 	circle4 = plt.Circle((S_L,math.sqrt(S_D**2-S_L**2)), D, color='black')
# 	fig, ax = plt.subplots() # note we must use plt.subplots, not plt.subplot
# 	# (or if you have an existing figure)
# 	# fig = plt.gcf()
# 	# ax = fig.gca()

# 	ax.add_artist(circle1)
# 	ax.add_artist(circle2)
# 	ax.add_artist(circle3)
# 	ax.add_artist(circle4)
# 	plt.show()

# # drawPack(0.0202,0.0202,0.0202,0.0184)

# # Task 2
# # http://www.thermopedia.com/content/1211/