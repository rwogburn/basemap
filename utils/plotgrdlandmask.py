from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import gzip, os
from netCDF4 import Dataset

# create a land/sea mask using GMT grdlandmask utility.
# this script reads the file generated by grdlandmask, plots it, 
# and saves it in the format that Basemap._readlsmask expects.


# run grdlandmask
#resolution = 'i' # gshhs resolution
#grid = '5' # grid size in minutes
athresh={}
athresh['c']=10000
athresh['l']=1000
athresh['i']=100
athresh['h']=10
athresh['f']=1

for resolution in ['c','l','i']:
    for grid in [2.5,5]:

        filename = 'grdlandmask%smin_%s.nc' % (grid,resolution)
        cmd = \
        'grdlandmask -F -G%s -I%sm -R-180/180/-90/90 -D%s -N0/1/2/1/2 -A%s+l' % \
        (filename, grid, resolution, athresh[resolution])
        print cmd
        os.system(cmd)
        
        # read in data.
        nc = Dataset(filename)
        lons = nc.variables['x'][:]
        nlons = len(lons)
        lats = nc.variables['y'][:]
        nlats = len(lats)
        lsmask = nc.variables['z'][:].astype(np.uint8)
        
        # plot
        fig = plt.figure()
        m =\
        Basemap(llcrnrlon=-180,llcrnrlat=-90,urcrnrlon=180,urcrnrlat=90,resolution=resolution,projection='mill')
        m.drawcoastlines() # coastlines should line up with land/sea mask.
        m.drawlsmask(land_color='coral',ocean_color='aqua',lsmask=lsmask,lsmask_lons=lons,lsmask_lats=lats,lakes=True)
        plt.title('%s by %s land-sea mask (resolution = %s) from grdlandmask' %\
                (nlons,nlats,resolution))
        
        # write out.
        f = gzip.open('lsmask_%smin_%s.bin' % (grid,resolution),'wb')
        print lsmask.dtype, lsmask.shape
        f.write(lsmask.tostring())
        f.close()

plt.show()