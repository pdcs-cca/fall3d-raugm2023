#!/usr/bin/env python
import numpy as np
import xarray as xr
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import cartopy, cartopy.crs as ccrs 
import pytz
import geopandas as gpd
from matplotlib.colors import LinearSegmentedColormap
import json
import os
import sys


if (len(sys.argv) < 4):
    print("Faltan argumentos")
    sys.exit()

hora = sys.argv[1]
altura = sys.argv[2]
date= sys.argv[3]

gdf = gpd.read_file('archivos_extra/destdv1gw/destdv1gw.shp')
gdf2 = gpd.read_file('archivos_extra/muni_2012gw//Muni_2012gw.shp')




with open('config.json') as file:
    config= json.load(file)
    Dir_out =config['d_salida']+"/"+sys.argv[3]
    Dir_in = config['d_entrada']+"/"+date
    Dir_ext =config['d_extra']
    Descrip= config["panel_fl"]['Descrip']
    unidades= config["panel_fl"]['unidades']
    
    fname = 'p_'+ hora +'h_'+ altura+'M.res.nc'
    ffile = os.path.join(Dir_in, fname)
    if(not os.path.exists(ffile)):
        print("El archivo ({}) no existe.".format(ffile))
        sys.exit()
    else:
        print(ffile)
        
    path = Dir_out
    try:
        working_path = path+ '/Hora_'+hora+ '/Altura_'+ altura +"/PANEL"
        print(working_path)
        os.makedirs(working_path)
    except:
        print("Creation of the directory %s failed" ,working_path )
         
    
    data=xr.open_dataset(ffile)
    lon_max=np.max(data.lon.values)
    lon_min=np.min(data.lon.values)
    lat_max=np.max(data.lat.values)
    lat_min=np.min(data.lat.values)
    
    niveles= data.fl.values

    bounds =(lon_min,lon_max,lat_min,lat_max)
    
    
    estados = Dir_ext+"destdv1gw/destdv1gw.shp"
    muni = Dir_ext+"muni_2012gw/Muni_2012gw.shp"
    
    for hr in range(data.time.shape[0]):
        hrst = "{0:0=3d}".format(hr)
        data.date[7].values
        dateB = data.date[hr].values.tobytes()
        st = dateB.decode('UTF-8').rstrip('\x00').rstrip(' ')
        dTSt = datetime.strptime(st, '%d%b%Y_%H:%M')
        utc_st = pytz.utc.localize(dTSt)
        pst_now = utc_st.astimezone(pytz.timezone("Mexico/General"))
        local_date=pst_now.strftime("%H:%M:%S %d/%m/%y ")
        if hr==0:
            explo_date=pst_now.strftime("%H:%M:%S %d/%m/%y ")

        
        F1 = data.tephra_fl[hr, :, :, :].values
        values = F1
        #values[values<.001]=np.nan
        
        fig, axs = plt.subplots(2, 3, figsize=(10, 8), layout='constrained')
        index=1    
        for ax in axs.flat:
            
           # ax = plt.axes(projection=ccrs.PlateCarree()
            img=ax.contourf(values[index-1,:,:], extent = bounds, origin='lower', levels=[0.001,0.0025,0.005,0.0075,0.01,0.025,0.05,0.075,0.1,2,10,100]  ,colors=["#FFFFFF","#9BC8DA","#5C9FC0","#438CB1","#C2DB91","#7DA430","#A99656","#9C7A3B","#905E20", "#8B1614","#560000"], linewidths=2)
            im2=gdf.plot(ax=ax, edgecolor='black', color='none',linewidth=.3)
            
            #im3=gdf2.plot(ax=ax, edgecolor='gray', color='none',linewidth=.15)
            
            ax.title.set_text( '{:,.0f}'.format(niveles[index-1]*100  )+" ft" )
            ax.set_xlim(lon_min,lon_max)
            ax.set_xticklabels(["","100°W","99°W","98°W","97°W"],fontsize=8 )
            ax.set_ylim(lat_min, lat_max)
            ax.set_yticklabels(["17°N","","18°N","","19°N","","20°N","","21°N"], fontsize=8)
    
            
            index+=1
        
        cbar=fig.colorbar(img, ax=axs, extend='both', orientation='horizontal',ticks=[0.001,0.0025,0.005,0.0075,0.01,0.025,0.05,0.075,0.1,2,10,100], pad=0.1, fraction=0.05)
        cbar.ax.set_title(Descrip +"   (" +unidades+")" ,fontsize = 9)
        fig.suptitle("Modelo Fall3D\n  "+"Erupción hipotética: "+ explo_date +"   con emisión de ceniazs a "+  altura + "km"+"\n Pronóstico a : " +hrst + "hrs  "+ local_date,fontsize = 9) 
        plt.savefig(working_path+"/Panel_" +hora+"_"+altura + "_" + hrst+".png",bbox_inches = 'tight',pad_inches = 0.2)
          
        
    
    





