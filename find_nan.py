import yt
import numpy as np
import matplotlib.pyplot as plt
import sys

#fil = yt.load('/scratch/gpfs/MUELLER/ltt/Methane/2D/plt/plt_2D05554')
fil = yt.load('/scratch/gpfs/MUELLER/ltt/Hydrogen/2D/plt/amr_1act/plt_h17450')

lo =  np.array([0.0, 0.0,0.])
hi = np.array([15.0, 5.0,0.025])
max_level = fil.index.max_level 
dxmin = fil.index.get_smallest_dx()
dxmax = dxmin*2.0*2.0 # if amr level 2
npts=np.floor((hi-lo)/dxmin)
npts_np = np.array(npts)
fields_load=["density","pressure", "Temp", "x_velocity", "y_velocity", "z_velocity","Y(H2O)"]

# Get the values on the grid at level 0 (finest level)
first = fil.covering_grid(level=max_level, left_edge=lo, dims=npts, fields=fields_load)
pres_1    = np.array(first["pressure"])
temp_1    = np.array(first["temperature"])
x_vel     = np.array(first["x_velocity"])
y_vel     = np.array(first["y_velocity"])
z_vel     = np.array(first["z_velocity"])
ch4     = np.array(first["Y(H2)"])

print("Pressure: ",pres_1[1569:1581,0,0])
print("Temperature: ",temp_1[1569:1581,0,0])
print("X Velocity: ",x_vel[1569:1581,0,0])
print("Y Velocity: ",y_vel[1569:1581,0,0])
print("Z Velocity: ",z_vel[1569:1581,0,0])
print("Y(H2): ",ch4[1569:1581,0,0])
#print("Temperature: ",np.where(np.isnan(temp_1)))