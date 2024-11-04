#!/apps/t3/sles12sp5/free/python/3.11.2/gcc4.8.5/bin/python3

### Set grd2ico parameters here
glev = 9
rlev = 3
hgrid_base = '/gs/hs1/jh230052/tutorial_package/NICAM_DATABASE/hgrid/gl09/rl03/grid'
vgrid_base = '/gs/hs1/jh230052/tutorial_package/NICAM_DATABASE/vgrid/vgrid78.dat'
ll_imax = 3600 #Confirm input netcdf
ll_jmax = 1801 #Confirm input netcdf
lon_ini = 0.0
lat_ini = -90.0
lon_inc = 0.1
lat_inc = 0.1
##### End of grd2ico parameter setting.

##### Outputting options
runico2ll = True
#####

import xarray, struct
from glob import glob
import numpy as np
import os
import f90nml
import subprocess
import shutil
#from xgrads import open_CtlDataset

os.environ['PYTHONPATH'] = '/home/2/varquez-a-aa/pip-local'
os.environ['PATH'] = '/home/2/varquez-a-aa/miniconda3/bin'

def convert_nc_to_binary(infold='input',outfold='output'):
    ahe_folder = infold
    filelist = glob(f'{ahe_folder}/*0.1deg.nc')
    for ifil in filelist:
        df = xarray.open_dataset(ifil)
        data = df['ahe'].values
        data = data.astype('float').flatten()
        df = None
        outfil = ifil.replace('.nc','.bin').replace(infold,outfold)
        if not os.path.exists(outfil):
            f = open(outfil,"wb")
            f.write(struct.pack(f">{data.shape[0]}f",*data))
            f.close()
        del(data)
        
def generate_grd2icocnf(ll_sfc_fname,ico_sfc_fname,outdir='./'):
        nmlorig = f90nml.read('grd2ico.cnf')
        nml = {
            'grd2ico_param': {
                'glevel': glev,
                'rlevel': rlev,
                'hgrid_basename': hgrid_base,
                'vgrid_filename': vgrid_base,
                'output_dir': outdir,
                'll_imax': ll_imax,
                'll_jmax': ll_jmax,
                'lon_ini': lon_ini,
                'lat_ini': lat_ini,
                'lon_inc': lon_inc,
                'lat_inc': lat_inc,
                'll_sfc_fname(1)': ll_sfc_fname,
                'ico_sfc_fname(1)': ico_sfc_fname,
            }
        }
        f90nml.patch('grd2ico_template.cnf', nml, 'grd2ico.cnf')
        
def runico2ll(iext):
    shutil.copyfile('check_template.info','check.info')
    with open('check.info','a') as file:
        file.write(f'{iext}')
    subprocess.run(['./ico2ll'])
    ctl = f'{iext}.ctl'
    subprocess.run(['cdo','-f','nc','import_binary',ctl,ctl.replace('.ctl','.nc')])
        
def run_grd2ico(infold,outfold):
    filelist = glob(f'{infold}/*_0.1deg*.bin')
    for ifil in filelist:
        generate_grd2icocnf(ifil,os.path.basename(ifil.replace('.bin','').replace('_0.1deg','')))
        subprocess.run(['./grd2ico'])
        if runico2ll:
            runico2ll(os.path.basename(ifil.replace('_0.1deg.bin','')))

convert_nc_to_binary()
run_grd2ico('./output/','./')
