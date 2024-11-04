#!/bin/bash
# Script used to construct inputs for the 14-km runs.
ls -1 *UTC.nc | sed 's/.nc//' | xargs -I {} cdo remapcon,r3600x1801 {}.nc {}_0.1deg.nc
