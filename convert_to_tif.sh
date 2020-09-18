#Script Name: Converting to a tif
#Date Created: 16/09/2020
#Date Modified: 16/09/2020
#Licence: JNCC
#Abstract: Script written for the Copernicus User Uptake project on illegal waste

#!/bin/sh
for f in ./Output/*data/*img;
	do echo "Processing $f";
	do gdalwarp -s_srs EPSG:4326 -t_srs EPSG:27700 -dstnodata 0 -r near -of GTiff -tr 10.0 10.0 -co "COMPRESS=DEFLATE" $f ${f%.*}.tif;
	do mv ${f%.*}.tif ./Output/
done
