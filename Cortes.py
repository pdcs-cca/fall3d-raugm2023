#!/usr/bin/env python
# coding: utf-8

# In[1]:


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




hora = sys.argv[1]
altura = sys.argv[2]
date= sys.argv[3]


gdf = gpd.read_file('archivos_extra/destdv1gw/destdv1gw.shp')
gdf2 = gpd.read_file('archivos_extra/muni_2012gw//Muni_2012gw.shp')

with open('config.json') as file:
    config = json.load(file)
    
    Dir_out =config['d_salida']+"/"+sys.argv[3]
    Dir_in =config['d_entrada']+"/"+date
    Dir_ext =config['d_extra']
    
    fname = 'p_'+ hora +'h_'+ altura+'M.res.nc'
    ffile = os.path.join(Dir_in, fname)
        
    
    data=xr.open_dataset(ffile)
    lon_max=np.max(data.lon.values)
    lon_min=np.min(data.lon.values)
    lat_max=np.max(data.lat.values)
    lat_min=np.min(data.lat.values)

    datestr = data.date.values
    for setting in config['cortes']:
        varName = setting['nameVar']
        VarCode = setting['varCode']
        #unidades = data[VarCode].attributes['units']
        Descrip = setting['Descrip']
        
        if(not os.path.exists(ffile)):
            print("El archivo ({}) no existe.".format(ffile))
            sys.exit()
        else:
            print(ffile)
        
        path = Dir_out
        try:
            working_path = path+ '/Hora_'+hora+ '/Altura_'+ altura +"/"+varName.upper()
            print(working_path)
            os.makedirs(working_path)
        except:
            print("Creation of the directory %s failed" ,working_path )
            
        
        lbLabelStrings = list(setting['VLabelStrings'])   
        z=data.z.values
        if setting['tipo'] == "lat":
            F1 = data.tephra_con_yz
            xlabel=data.lon.values
            popoca=data.z_grn.sel(lat=19.02)
            unidades = data["tephra_con_yz"].attrs['units']
            
        else:
            F1 = data.tephra_con_xz
            xlabel=data.lat.values
            popoca=data.z_grn.sel(lon=-98.62)
            unidades = data["tephra_con_xz"].attrs['units']
            
        X, Y = np.meshgrid(xlabel,data.z.values )
        
        print("inicia horas")    
        for hr in range(F1.shape[0]):
            
            aux=F1[hr,0, :, :]
            
            dateB = datestr[hr].tobytes()
            st = dateB.decode('UTF-8').rstrip('\x00').rstrip(' ')
            dTSt = datetime.strptime(st, '%d%b%Y_%H:%M')
            utc_st = pytz.utc.localize(dTSt)
            pst_now = utc_st.astimezone(pytz.timezone("Mexico/General"))
            local_date=pst_now.strftime("%H:%M:%S %d/%m/%y ")
            if hr==0:
                explo_date=pst_now.strftime("%H:%M:%S %d/%m/%y ")
            
            hrst = "{0:0=3d}".format(hr)
            
            fig= plt.figure(figsize=(9,9))
            ax=plt.axes()
            
            img=ax.contourf(X,Y,aux,levels=setting['VLevels']  ,colors=setting['paleta'])
            plt.fill_between(xlabel,popoca.values,color='gray')
            cbar=plt.colorbar(img, extend='both', orientation='horizontal', pad=0.1, fraction=0.05)
            cbar.ax.set_title(Descrip +"   (" +unidades+")" ,fontsize = 9)
            ax.set_title("Corte latitud=19.02°N", fontsize = 9)
            ax.set_xlabel("Longitud", fontsize = 9)
            ax.set_ylabel("Elevación del terreno (m)",fontsize = 9)
            fig.suptitle("Modelo Fall3D\n  "+"Erupción hipotética: "+ explo_date +"   con emisión de cenizas a "+  altura + "km"+"\n Pronóstico a : " +hrst + "hrs  "+ local_date,fontsize = 10) 
            plt.savefig(working_path+"/"+varName+"_"+hora+"_"+altura + "_" + hrst+".png",bbox_inches = 'tight',pad_inches = 0.2)       