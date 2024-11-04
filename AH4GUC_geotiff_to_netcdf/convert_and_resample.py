import xarray as xr
from glob import glob
import xesmf as xe
import numpy as np
from cdo import *
import subprocess
import pandas as pd
import os

cdo  = Cdo()
comp = dict(zlib=True,complevel=5)

for ifil in glob('*.tif'):
    hr=ifil.split('_')[4][0:2]
    outfil=f"{ifil.replace('.tif','_2.5deg.nc')}"
    if os.path.exists(outfil):
        print(f"{outfil} exists. Skipping...")
        continue
    print(f"Creating {outfil}")
    geotiff_da = xr.open_rasterio(ifil)
    test = geotiff_da[0,:,:]

    ds = xr.Dataset(
        data_vars=dict(
            ahe=(["lat","lon"],test[:,:].values,{'standard_name':'AHE',
                                                 'long_name':'Anthropogenic Heat Flux (AH4GUC)',
                                                 'units':'W/m^2',
                                                 'coordinates':'lat lon',
                                                 'scale_factor':test.scales[0],
                                                 'dtype':'int16'})
            ),
        coords=dict(
            lon=(["lon"],test.x.values,{'standard_name':'longitude',
                                        'long_name':'Longitude',
                                        'units':'degrees_east',
                                        'dtype':'float32'}),
            lat=(["lat"],test.y.values,{'standard_name':'latitude',
                                        'long_name':'Latitude',
                                        'units':'degrees_north',
                                        'dtype':'float32'}),
            time=pd.Timestamp(f"2010-07-16 {hr}:00:00")
            ),
        attrs=dict(
            title="Anthropogenic Heat for Global Urban Climatology (AH4GUC) Data",
            source="https://urbanclimate.tse.ens.titech.ac.jp/2020/12/14/global-1-km-present-and-future-hourly-anthropogenic-heat-flux/",
            references="Varquez, A.C.G., Kiyomoto, S., Khanh, D.N. et al. Global 1-km present and future hourly anthropogenic heat flux. Sci Data 8, 64 (2021). https://doi.org/10.1038/s41597-021-00850-w",
            comment = "Original dataset in GeoTIFF format"
            ),
        )

    comp = dict(zlib=True,complevel=5)
    encoding = {var: comp for var in ds.data_vars}
    ds.to_netcdf(f"{ifil.replace('.tif','.nc')}",encoding=encoding) #Stores raw AH4GUC geotiffs to netcdfs
    ds = None
    geotiff_da = None
    cdo.remapcon("r144x73", input=f"{ifil.replace('.tif','.nc')}", output=outfil) #Creates 2.5 degree version for coarse runs.
