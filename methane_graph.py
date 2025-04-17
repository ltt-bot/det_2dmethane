import yt
import numpy as np
import matplotlib.pyplot as plt
import sys

colors = ["#D74214","#E8C00C","#0F9C0F","#8D3FBE","#2D2DC8","#79838B"]
grid_x = 450
grid_y = 150
dx = 15/450
diff = 1000
start_timestep = 1000
end_timestep = 57000
start = 1000
stab = 0
plot_single = 55000
#end_timestep  = 22000
vel = np.zeros((int((end_timestep - start_timestep) / diff),2))
mdots = np.zeros((int((end_timestep - start_timestep) / diff),2))
thrusts = np.zeros((int((end_timestep - start_timestep) / diff),2))
isps = np.zeros((int((end_timestep - start_timestep) / diff),2))
while (start_timestep < end_timestep):
    file_name = '/scratch/gpfs/MUELLER/ltt/Methane/2D/120_inlet/plt_2D' 
    f_1 = yt.load(file_name +"{:05d}".format(start_timestep))
    f_2= yt.load(file_name + "{:05d}".format(start_timestep+diff))


    # Get the information needed for the grid
    max_level = f_1.index.max_level 

    lo =  np.array([0.0, 0.0,0.])
    hi = np.array([15.0, 5.0,dx])

    dxmin = f_1.index.get_smallest_dx()
    dxmax = dxmin*2.0*2.0 # if amr level 2
    npts=np.floor((hi-lo)/dxmin)
    npts_np = np.array(npts)
    fields_load=["density","pressure", "Temp", "x_velocity", "y_velocity", "z_velocity","Y(H2O)"]

    # Get the values on the grid at level 0 (finest level)
    first = f_1.covering_grid(level=max_level, left_edge=lo, dims=npts, fields=fields_load)
    second = f_2.covering_grid(level=max_level, left_edge=lo, dims=npts, fields=fields_load)
    pres_1    = np.array(first["pressure"])
    pres_2    = np.array(second["pressure"])
    temp_1    = np.array(first["temperature"])
    dens = np.array(first["density"])
    y_vel = np.array(first["y_velocity"])
    h20 = np.array(first["Y(H2O)"])
    h2 = np.array(first["Y(H2)"])

    mdot = np.trapezoid((dens[:,grid_y-1,0] * y_vel[:,grid_y-1,0]), dx=dx) * 10**(-1)
    thrust = np.trapezoid(dens[:,grid_y-1,0] * (y_vel[:,grid_y-1,0]**2) + pres_1[:,grid_y-1,0] - 1013250, dx=dx)
    mdot_h2 = np.trapezoid((dens[:,0,0] * h2[:,0,0] * y_vel[:,0,0]), dx=dx)
    isp = thrust/(mdot_h2 * 980.665)
    x_arr = np.linspace(lo[0], hi[0], int(npts_np[0]))
    y_arr = np.linspace(lo[1], hi[1], int(npts_np[1]))

    if start_timestep == 32000:
        grad_pres = np.gradient(pres_1[:,:,0],dx*10**(-2),dx*10**(-2))
        dp_dx = grad_pres[1]
        dp_dy = grad_pres[0]
        mag_pres =  np.sqrt(dp_dx**2 + dp_dy**2)
        beta = 1
        k = 60
        grad_1 = beta * np.exp((-k*mag_pres)/np.max(mag_pres))
        ax = plt.figure(figsize=(8,3))
        im1 =  plt.imshow(np.fliplr(np.rot90(grad_1,2).T),cmap="binary",extent=[0, 15, 0, 5])
        plt.colorbar(im1, label='Pressure Gradient',shrink=0.6, aspect=20*0.6)
        plt.xlabel("X (cm)")
        plt.ylabel("Y (cm)")
        plt.savefig(f"pres_grad.png", dpi=1200)
        plt.close()

        ax2 = plt.figure(figsize=(8,4))
        im = plt.imshow(np.fliplr(np.rot90(temp_1[:,:,0],2).T), cmap="jet",extent=[0, 15, 0, 5])
        #contour = plt.contourf(x_arr,y_arr, temp_1[:,:,0].transpose(), levels = 1000, cmap="jet")
        plt.xlabel("X (cm)")
        plt.ylabel("Y (cm)")
        plt.colorbar(im, label='Temperature (K)',shrink=0.6, aspect=20*0.6)
        plt.savefig(f"temp.png", dpi=1200)
        plt.close()

        equil = 0.22190
        ax3 = plt.figure(figsize=(8,4))
        plt.plot( pres_1[:,20,0] * 10**(-1),h20[:,20,0]/equil)
        plt.xlabel("Pressure (Pa)")
        plt.ylabel("Y(H2O)")
        plt.savefig(f"h20_pres.png", dpi=1200)
        plt.close()



    dt = f_2.current_time - f_1.current_time

    if f_1.current_time > 0.35 * 10**(-3) and stab == 0:
        stab = int((end_timestep - start_timestep) / diff) - 1


    check = pres_1[:,0,0]
    check2 = pres_2[:,0,0]
    max_index1 = np.unravel_index(np.argmax(check), check.shape)[0]
    max_index2 = np.unravel_index(np.argmax(check2), check2.shape)[0]
    if max_index2 < max_index1:
        max_index2 = grid_x + max_index2
    speed = (((max_index2 - max_index1) * dxmin) / (dt)) *(10**-2)
    vel[int((start_timestep - start) / diff),:] = [f_1.current_time, speed]
    mdots[int((start_timestep - start) / diff),:] = [f_1.current_time, mdot]
    thrusts[int((start_timestep - start) / diff),:] = [f_1.current_time, thrust]
    isps[int((start_timestep - start) / diff),:] = [f_1.current_time, isp]
    start_timestep = start_timestep + diff

f, (ax,axs) = plt.subplots(1,2, figsize=(7,4), width_ratios=[1,0.75])
ax.plot(vel[:,0] * 10**3,vel[:,1],  color="#ea5545")
ax.grid()
ax.set_xlabel("Time (ms)")
ax.set_ylabel("Velocity (m/s)")
# plt.savefig(f"Velocity_sing.png", dpi=1200)
# plt.close()

# axs = plt.figure()
colors = ["#ea5545"]
bplot = axs.boxplot(x=[vel[stab:,1]], 
                 patch_artist=True)
axs.grid(True, axis='y')
# fill with colors
for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)
for median in bplot['medians']:
    median.set_color('black')
axs.set_xticks([y + 1 for y in range(1)],labels=[""])
plt.savefig(f"Velocity_sing.png", dpi=1200)
plt.close()

# ax_m = plt.figure()
# plt.plot(mdots[stab:,0]  * 10**3 ,mdots[stab:,1],  color="#ea5545")
# plt.grid()
# plt.xlabel("Time (ms)")
# plt.ylabel("Mass Flowrate(kg/s)")
# plt.savefig(f"mdot.png", dpi=1200)
# plt.close()
# print(mdots[stab:,0] * 10**3 )

plt.figure()
axs = plt.axes()
colors = ["#ea5545"]
bplot = axs.boxplot(x=[mdots[stab:,1]], 
                 patch_artist=True)
axs.grid(True, axis='y')
# fill with colors
for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)
for median in bplot['medians']:
    median.set_color('black')
axs.set_xticks([y + 1 for y in range(1)],labels=[""])
plt.ylabel("ṁ (kg/ms)")
plt.savefig(f"mdot.png", dpi=1200)
plt.close()

x_m = plt.figure()
plt.plot(thrusts[:,0]  * 10**(3) ,thrusts[:,1] * 10**(-6),  color="#ea5545")
plt.grid()
plt.xlabel("Time (ms)")
plt.ylabel("Thrust")
plt.savefig(f"thrust.png", dpi=1200)
plt.close()




print(np.mean(vel[stab:,1]))