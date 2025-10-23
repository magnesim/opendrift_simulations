from datetime import datetime, timedelta 
#from opendrift.models.oceandrift import OceanDrift
from opendrift.models.radionuclides import RadionuclideDrift
from opendrift.readers import reader_netCDF_CF_generic




## Basic OpenDrift simulation with Norkystv3 800m data from THREDDS
#o = OceanDrift(loglevel=20)  # Set loglevel to 0 for debug information
o = RadionuclideDrift(loglevel=20, seed=0)  # Set loglevel to 0 for debug information



# Configuration
release_time     = datetime(2025,10,14,12,0)  # UTC
#td=datetime.today()
#release_time = datetime(td.year, td.month, td.day, 0)

total_time       = 48  # hours 
time_step        = 400   # seconds
end_time         = release_time + timedelta(hours=total_time)
#release_latitude   = 58.9 
#release_longitude  = 10.5
release_longitude  =10.62
release_latitude   =59.66



# Path to Norkystv3 800m data on THREDDS
#norkyst_thredds_url = 'https://thredds.met.no/thredds/dodsC/fou-hi/norkystv3_800m_m00_be'
norkyst_thredds_url = 'https://thredds.met.no/thredds/dodsC/fou-hi/norkystv3_160m_m71_be'





# Add readers
reader_norkyst = reader_netCDF_CF_generic.Reader (norkyst_thredds_url)
o.add_reader([reader_norkyst, ])





# Adjust configuration
o.set_config('general:coastline_action','previous')
#o.set_config('general:coastline_action','stranding')        # let particles go on land
o.set_config('general:seafloor_action','lift_to_seafloor')


o.set_config('seed:LMM_fraction', 0.5)                      # fraction of particles to be seeded in LMM form
o.set_config('seed:particle_fraction', 0.5)                 # fraction of particles to be seeded in particle form
o.set_config('seed:total_release', 1.0e12)                  # total activity to be released (Bq)



#o.set_config('drift:vertical_advection', False)             # disable vertical advection
o.set_config('drift:horizontal_diffusivity', 1.)         # horizontal diffusivity in m2/s
o.set_config('drift:vertical_mixing', True)
o.set_config('vertical_mixing:diffusivitymodel','environment')  # apply vertical diffusivity from ocean model
o.set_config('vertical_mixing:timestep', 600.) # seconds     # Vertical mixing requires fast time step

o.set_config('radionuclide:output:depthintervals', '-5')  # depth intervals for output of radionuclide density map


# Seed particles
o.seed_elements(lon=release_longitude, lat=release_latitude, z=0, radius=50, number=1000, time=[release_time, end_time] )





# Run the model
o.list_configspec()   # List the configuration specification




o.run(steps=total_time*3600/time_step +1, time_step=time_step, time_step_output=3600, outfile='radionuclide.nc') 




#if True:
if False:
    o.plot_vertical_distribution()
    o.plot(linecolor='specie',vmin=0,vmax=o.nspecies-1,fast=True,)


o.animation( color='z',
            # color='specie',
            # vmin=0,vmax=o.nspecies-1,
            # colorbar=False,
            # legend=[o.specie_num2name(i) for i in range(o.nspecies)],
#            fast = True
#            background=['x_sea_water_velocity', 'y_sea_water_velocity'], scale=100,
            )



if False:
#if True:
    conc_filename = 'concentration_rad320.nc'
    o.write_netcdf_radionuclide_density_map(conc_filename, 
                                            pixelsize_m = 400.,                 # grid cell size in meter 
#                                            llcrnrlon=10.54, llcrnrlat=59.52,
#                                            urcrnrlon=10.66, urcrnrlat=59.62, 
                                            llcrnrlon=release_longitude-0.3, llcrnrlat=release_latitude-0.15,
                                            urcrnrlon=release_longitude+0.3, urcrnrlat=release_latitude+0.15, 
                                            horizontal_smoothing = True,
                                            smoothing_cells = 1,
                                            )


    o.guipp_plotandsaveconc(filename=conc_filename, outfilename='rad320', specie=['Total'])


