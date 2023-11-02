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

#hora = '01' #sys.argv[1]
#altura = '03'#sys.argv[2]
#date='20230523'  #sys.argv[3]
#Dir_out ="../Salidas/"+date #data['d_salida']+"/"+sys.argv[3]
#Dir_in ="../Entradas/"+date #data['d_entrada']+"/"+date
#Dir_ext ="archivos_extra" #data['d_extra']

if (len(sys.argv) < 4):
    print("Faltan argumentos")
    sys.exit()

hora = sys.argv[1]
altura = sys.argv[2]
date= sys.argv[3]

gdf = gpd.read_file('archivos_extra/destdv1gw/destdv1gw.shp')
gdf2 = gpd.read_file('archivos_extra/muni_2012gw//Muni_2012gw.shp')



with open('config.json') as file:
    conf = json.load(file)
    Dir_out =conf['d_salida']+"/"+date
    Dir_in =conf['d_entrada']+"/"+date
    Dir_ext =conf['d_extra']
    fname = 'p_'+ hora +'h_'+ altura+'M.res.nc'
    ffile = os.path.join(Dir_in, fname)
    estados = Dir_ext+"destdv1gw/destdv1gw.shp"
    muni = Dir_ext+"muni_2012gw/Muni_2012gw.shp"
    
    if(not os.path.exists(ffile)):
        print("El archivo ({}) no existe.".format(ffile))

        sys.exit()
    else:
        print(ffile) 
        
    data=xr.open_dataset(ffile)
    lon_max=np.max(data.lon.values)
    lon_min=np.min(data.lon.values)
    lat_max=np.max(data.lat.values)
    lat_min=np.min(data.lat.values)

    bounds =(lon_min,lon_max,lat_min,lat_max)
    for setting in conf['2D']:
        if 'disable' in setting:
            continue
                       
        varName = setting['nameVar']
        VarCode = setting['varCode']
        unidades = data["tephra_fl"].attrs['units']
        Descrip = setting['Descrip']
        
         
        if type(setting['VLevels']) == str:
            lbLabelStrings = eval(setting['VLevels'])
        else:
            lbLabelStrings = setting['VLevels']
         
        path = Dir_out
        try:
            working_path = path+ '/Hora_'+hora+ '/Altura_'+ altura +"/"+varName
            print(working_path)
            os.makedirs(working_path)
        except:
            print("Creation of the directory %s failed" ,working_path )
                
        F1 = data[VarCode][:, :, :].values
                
        for hr in range(F1.shape[0]):
            hrst = "{0:0=3d}".format(hr)
            values = F1[hr, :, :]
            values[values<.001]=np.nan
            data.date[7].values
            dateB = data.date[hr].values.tobytes()
            st = dateB.decode('UTF-8').rstrip('\x00').rstrip(' ')
            dTSt = datetime.strptime(st, '%d%b%Y_%H:%M')
            utc_st = pytz.utc.localize(dTSt)
            pst_now = utc_st.astimezone(pytz.timezone("Mexico/General"))
            local_date=pst_now.strftime("%H:%M:%S %d/%m/%y ")
            if hr==0:
                explo_date=pst_now.strftime("%H:%M:%S %d/%m/%y ")
                    
            plt.figure(figsize=(9,9))
            ax = plt.axes()
            img=ax.contourf(values, extent = bounds, origin='lower', levels=setting['VLevels'] ,colors=setting['paleta'])
            cbar=plt.colorbar(img, extend='both', orientation='horizontal', pad=0.1, fraction=0.05)
            #cbar.ax.set_xticklabels(setting["VLabelStrings"], fontsize=5)
            cbar.ax.set_title(Descrip +"   (" +unidades+")" ,fontsize = 9)
            im2=gdf.plot(ax=ax, edgecolor='black', color='none',linewidth=.3)
            im3=gdf2.plot(ax=ax, edgecolor='gray', color='none',linewidth=.15)
            ax.set_xlim(lon_min, lon_max)
            ax.set_ylim(lat_min, lat_max)
            #gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=0.2, color='black',linestyle='--')
            #gl.top_labels = False
            #gl.right_labels = False
            plt.title("Modelo Fall3D\n",fontsize = 10) 
            plt.title("Erupción: "+ explo_date +"\n"+"Altura fumarola: "+  altura + "km", loc='left' ,fontsize = 9)
            plt.title("Pronóstico a : " +hrst + "hrs \n"+ local_date, loc='right',fontsize = 9)
            plt.savefig(working_path+"/"+varName+"_" +hora+"_"+altura + "_" + hrst+".png",bbox_inches = 'tight',pad_inches = 0.2)
          

    for setting in conf['3D']:
        if 'disable' in setting:
            continue

        desc2=[]
        
        if 'indexV' in setting:
            levname = setting['indexV']
            print(levname)
            pre = setting["prefix"]
            aux = data[levname][:].values.tolist()
            array_name = [pre+str(int(x)) for x in aux]
            array_inds = [x for x in range(len(aux))]
            array_label =[" FL-"+str(int(x)) for x in aux]
            print(aux)
            desc2 =[str(int(x)*100)+" ft" for x in aux]
            
        else:
            array_name = setting['indName']
            array_inds = setting['indexs']
            array_label =setting['indLabel']
            
        print(array_name)
        VarCode = setting['varCode']
        unidades = data["tephra_fl"].attrs['units']
        Descrip = setting['Descrip']
        
            
        if type(setting['VLabelStrings']) == str:
            lbLabelStrings = eval(setting['VLabelStrings'])
        else:
            lbLabelStrings = setting['VLabelStrings']
            
        for index in array_inds:
            sub=""
            if len(desc2)!=0:
                sub=desc2[index]

            varName = array_name[index]
            DescripI= array_label[index]

            path = Dir_out
            try:
                working_path = path+ '/Hora_'+hora+ '/Altura_'+ altura +"/"+varName
                print(working_path)
                os.makedirs(working_path)
            except:
                print("Creation of the directory %s failed" ,working_path )
                
            F1 = data[VarCode][:, index, :, :].values
                
            for hr in range(F1.shape[0]):
                hrst = "{0:0=3d}".format(hr)
                values = F1[hr, :, :]
                values[values<.001]=np.nan
                data.date[7].values
                dateB = data.date[hr].values.tobytes()
                st = dateB.decode('UTF-8').rstrip('\x00').rstrip(' ')
                dTSt = datetime.strptime(st, '%d%b%Y_%H:%M')
                utc_st = pytz.utc.localize(dTSt)
                pst_now = utc_st.astimezone(pytz.timezone("Mexico/General"))
                local_date=pst_now.strftime("%H:%M:%S %d/%m/%y ")
                if hr==0:
                    explo_date=pst_now.strftime("%H:%M:%S %d/%m/%y ")
                    
                plt.figure(figsize=(9,9))
                ax = plt.axes()
                img=ax.contourf(values, extent = bounds, origin='lower', levels=setting['VLevels']  ,colors=setting['paleta'])
                cbar=plt.colorbar(img, extend='both', orientation='horizontal', pad=0.1, fraction=0.05)
                #cbar.ax.set_xticklabels(setting["VLabelStrings"], fontsize=5)
                cbar.ax.set_title(setting["Descrip"] +" "+sub +" "+DescripI+"   (" +unidades+")" ,fontsize = 9)
                im2=gdf.plot(ax=ax, edgecolor='black', color='none',linewidth=.3)
                im3=gdf2.plot(ax=ax, edgecolor='gray', color='none',linewidth=.15)
                ax.set_xlim(lon_min, lon_max)
                ax.set_ylim(lat_min, lat_max)
               # gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=0.2, color='black',linestyle='--')
                #gl.top_labels = False
                #gl.right_labels = False
                plt.title("Modelo Fall3D\n",fontsize = 10) 
                plt.title("Erupción: "+ explo_date +"\n"+"Altura fumarola: "+  altura + "km", loc='left' ,fontsize = 9)
                plt.title("Pronóstico a : " +hrst + "hrs \n"+ local_date, loc='right',fontsize = 9)
                plt.savefig(working_path+"/"+varName+"_" +hora+"_"+altura + "_" + hrst+".png",bbox_inches = 'tight',pad_inches = 0.2)
                    
                    






