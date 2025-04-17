import yt
import numpy as np
import matplotlib.pyplot as plt
import sys

colors = ["#D74214", "#E8C00C","#0E920E","#8D3FBE","#2D2DC8","#79838B"]

file_name = '/scratch/gpfs/MUELLER/ltt/Hydrogen/2D/plt/no_amr/plt_h01850' 
f_1 = yt.load(file_name)

file_name_1 = '/scratch/gpfs/MUELLER/ltt/Hydrogen/2D/plt/amr1/plt_h02000'
file_name_2 = '/scratch/gpfs/MUELLER/ltt/Hydrogen/2D/plt/amr2/plt_h01650'
file_name_3 = '/scratch/gpfs/MUELLER/ltt/Hydrogen/2D/plt/amr3/plt_h01600'

f_amr1 = yt.load(file_name_1)
f_amr2 = yt.load(file_name_2)
f_amr3 = yt.load(file_name_3)

# Get the information needed for the grid
max_level = f_1.index.max_level 
max_level_1 = f_amr1.index.max_level 
max_level_2 = f_amr2.index.max_level 
max_level_3 = f_amr3.index.max_level 

lo =  np.array([0.0, 0.0,0.])
hi = np.array([15.0, 5.0,0.025])
lo1 =  np.array([0.0, 0.0,0.])
hi1 = np.array([15.0, 5.0,0.0125])
lo2 =  np.array([0.0, 0.0,0.])
hi2 = np.array([15.0, 5.0,0.00625])
lo3 =  np.array([0.0, 0.0,0.])
hi3 = np.array([15.0, 5.0,0.003125])

dxmin = f_1.index.get_smallest_dx()
dxmin1 = f_amr1.index.get_smallest_dx()
dxmin2 = f_amr2.index.get_smallest_dx()
dxmin3 = f_amr3.index.get_smallest_dx()
dxmax3 = dxmin*2.0*2.0*2.0 # if amr level 3
dxmax2 = dxmin*2.0*2.0 # if amr level 2
dxmax1 = dxmin*2.0 # if amr level 1
npts=np.floor((hi-lo)/dxmin)
npts_np = np.array(npts)
npts1=np.floor((hi-lo)/dxmin1)
npts_np1 = np.array(npts1)
npts2=np.floor((hi-lo)/dxmin2)
npts_np2 = np.array(npts2)
npts3=np.floor((hi-lo)/dxmin3)
npts_np3 = np.array(npts3)
fields_load=["density","pressure", "Temp", "x_velocity", "y_velocity", "z_velocity","Y(H2O)"]

# Get the values on the grid at level 0 (finest level)
first = f_1.covering_grid(level=max_level, left_edge=lo, dims=npts, fields=fields_load)
second = f_2.covering_grid(level=max_level, left_edge=lo, dims=npts, fields=fields_load)

amr1 = f_amr1.covering_grid(level=max_level_1, left_edge=lo1, dims=npts1, fields=fields_load)
amr2 = f_amr2.covering_grid(level=max_level_2, left_edge=lo2, dims=npts2, fields=fields_load)
amr3 = f_amr3.covering_grid(level=max_level_3, left_edge=lo3, dims=npts3, fields=fields_load)

pres_1    = np.array(first["pressure"])
pres_2    = np.array(second["pressure"])

pres_amr1    = np.array(amr1["pressure"])
pres_amr2    = np.array(amr2["pressure"])
pres_amr3    = np.array(amr3["pressure"])


x_arr = np.linspace(lo[0], hi[0], int(npts_np[0]))
y_arr = np.linspace(lo[1], hi[1], int(npts_np[1]))
x_arr1 = np.linspace(lo[0], hi[0], int(npts_np1[0]))
y_arr1 = np.linspace(lo[1], hi[1], int(npts_np1[1]))
x_arr2 = np.linspace(lo[0], hi[0], int(npts_np2[0]))
y_arr2 = np.linspace(lo[1], hi[1], int(npts_np2[1]))
x_arr3 = np.linspace(lo[0], hi[0], int(npts_np3[0]))
y_arr3 = np.linspace(lo[1], hi[1], int(npts_np3[1]))


ax = plt.figure()
plt.plot(x_arr,pres_1[:,2]**10^(-1), label="No AMR", color=colors[0])
plt.plot(x_arr1,pres_amr1[:,4]**10^(-1), label="AMR 1", color=colors[1])
plt.plot(x_arr2,pres_amr2[:,6]**10^(-1), label="AMR 2", color=colors[2])
plt.plot(x_arr3,pres_amr3[:,8]**10^(-1), label="AMR 3", color=colors[3])
ax.grid()
plt.legend()
plt.xlabel("X (cm)")
plt.ylabel("Pressure (Pa)")
plt.savefig(f"pres_amr.png")
plt.close()