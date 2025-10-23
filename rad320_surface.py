from datetime import datetime, timedelta 
from opendrift.models.oceandrift import OceanDrift
from opendrift.readers import reader_netCDF_CF_generic




## Basic OpenDrift simulation with Norkystv3 800m data from THREDDS
o = OceanDrift(loglevel=20)  # Set loglevel to 0 for debug information



# Configuration
release_time     = datetime(2025,10,14,12,0)  # UTC

total_time       = 24  # hours 
time_step        = 400   # seconds
end_time         = release_time + timedelta(hours=total_time)
release_latitude   = 58.9 
release_longitude  = 10.5



# Path to Norkystv3 800m data on THREDDS
norkyst_thredds_url = 'https://thredds.met.no/thredds/dodsC/fou-hi/norkystv3_800m_m00_be'





# Add readers
reader_norkyst = reader_netCDF_CF_generic.Reader (norkyst_thredds_url)
o.add_reader([reader_norkyst, ])





# Adjust configuration
o.set_config('general:coastline_action','previous')
#o.set_config('general:coastline_action','stranding')        # let particles go on land
#o.set_config('general:seafloor_action','lift_to_seafloor')


o.set_config('drift:vertical_advection', False)             # disable vertical advection
o.set_config('drift:horizontal_diffusivity', 1.)         # horizontal diffusivity in m2/s



# Seed particles
o.seed_elements(lon=release_longitude, lat=release_latitude, z=0, radius=50, number=1000, time=release_time )





# Run the model
o.list_configspec()   # List the configuration specification




o.run(steps=total_time*3600/time_step +1, time_step=time_step, time_step_output=3600, 
      #outfile='surface.nc'
      ) 




if True:     # set True/False to enable/disable plotting
    o.plot()


o.animation(
#            fast = True
            #background=['x_sea_water_velocity', 'y_sea_water_velocity'], scale=100,
            #filename='surface_trajectory_animation_cur.mp4',
            #fps=10,
            #dpi=200
            )

