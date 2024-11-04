# ahe_to_nicam
Converts the AH4GUC files to NICAM compatible surface boundaries. Prepared by ACGV.

## Inputs
The inputs must be netcdf versions of the AH4GUC. Kindly read the python scripts. Current version is not that flexible. Will be improved in the future.

The script can be ran using python. The output fulders can be also specified in the script.

### AH4GUC_geotiff_to_netcdf
In the folder, the AH4GUC geotiffs from the website can be converted into netcdfs. Be sure to use the files that are in UTC.

#### download.bash
The script to download from the server. Needs wget.

#### convert_and_resample.py
The python script needed to convert from geotiff to netcdfs. See required modules in the script.

####  resample_0.1bash
Converts the netcdfs to the 0.1 degree resolution using conservative regridding. Needs cdo installed.
