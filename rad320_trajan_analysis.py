
import xarray as xr
import trajan as ta 
import matplotlib.pyplot as plt
import numpy as np 
import cartopy.crs as ccrs
import cartopy.feature as cfeature



# ###############
# Load OpenDrift trajectory data
filename = 'radionuclide.nc'
#filename = 'surface.nc'

d = xr.open_dataset(filename, decode_coords=False)
d = d.where(d.status>=0)                # only active particles

# Read activity per element from attributes
try:
    activity_per_element  = d.attrs['config_seed:total_release'] / d.sizes['trajectory']
    print('activity_per_element',activity_per_element,'Bq')
except KeyError:
    activity_per_element = 1.


# ###############
# Plot trajectories
d.traj.plot(land='mask')
ax = plt.gca()
ax.set_title('Trajectories')





# ###############
# Compute gridded concentration and
# Plot concentration maps
# at selected times
gridsize=400 # meters
grid = d.traj.make_grid(dx=gridsize, z=[0,-5])


for tt in [12,24]:    # add more time indices as needed
    fig=plt.figure(figsize=[7,8])
    ax=plt.subplot(1,1,1, projection=ccrs.Orthographic(central_longitude=10.0, central_latitude=60.0))
    ds_time = d.isel(time=tt) # pick a time index
    #ds_time = ds_time.where( ds_time.specie==0 )   # Extract only one specie if needed
    ds_c = ds_time.traj.concentration(grid) *activity_per_element

    ds_vc = ds_c.number_volume_concentration.sel(z=-2.5)
    ds_vc = ds_vc.fillna(0.)  # set nans to zero
    ds_vc = ds_vc.rolling(lat=3,lon=3, center=True).mean()  # spatial smoothing
    ds_vc = ds_vc.fillna(0.)  # set nans to zero
    ds_vc.plot(cmap='hot_r',transform=ccrs.PlateCarree())
    plt.title(f'Radionuclide concentration at t={tt} hours\n{d.time.values[tt]}')
    
#    ax.set_extent([10.3, 10.9, 59, 60], crs=ccrs.PlateCarree())
#    ax.add_feature( cfeature.GSHHSFeature(scale='f') )
    ax.add_feature( cfeature.GSHHSFeature(scale='h') )

    print('Max concentration:', np.max(ds_vc.values), 'Bq/m3')






if False:

    # ###############
    # Time series at a chosen position
    pos = [10.625, 59.595]                          # lon, lat
    time_smooth_win = 5                             # number of time steps for smoothing

    # Compute time series of concentration at given position
    ds_c = d.traj.concentration(grid).sel(lon=pos[0], lat=pos[1], z=0, method='nearest') *activity_per_element
    ts2 = ds_c.number_volume_concentration
    ts2 = ts2.fillna(0.)                                                        # set nans to zero
    sm_smooth_conc = ts2.rolling( time=time_smooth_win, center=True).mean()     # time smoothing

    # Plot time series
    fig=plt.figure(figsize=[9,7])
    ax=plt.subplot(1,1,1)
    ts2.plot(ax=ax,  label='',color='C0', lw=0.4 )
    sm_smooth_conc.plot( ax=ax, #label='smooth' , 
                        color='C0', lw=.9, ls='-')
    ax.grid()
    ax.set_title(f'Radionuclide concentration at lon={pos[0]}, lat={pos[1]}')
    ax.set_ylabel('Bq/m3')
    ax.legend()



plt.show()