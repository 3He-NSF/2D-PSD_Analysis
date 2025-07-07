import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # 3D描画用
import config
import xarray as xr
import pandas as pd


if __name__ == "__main__":

    Intensity=np.zeros((int(config.mesh_size),int(config.mesh_size)))
    dataNum=np.zeros((int(config.mesh_size),int(config.mesh_size)))

    Scan_dataframe = pd.read_csv(f"../../2025/June/DAQ_Data/DAQ{config.RunNumber}/DAQ{config.RunNumber}_ScanDataframe.csv")
    dQx=(config.Qx_range[1]-config.Qx_range[0])/config.mesh_size
    dQy=(config.Qy_range[1]-config.Qy_range[0])/config.mesh_size
    print(Scan_dataframe)

    for i in range(len(Scan_dataframe)):
        Qx = Scan_dataframe['Qx'][i]
        Qy = Scan_dataframe['Qy'][i]
        Qz = Scan_dataframe['Qz'][i]
        # print(Qx,Qy,Qz)
        if (config.Qx_range[0] <= Qx <=config.Qx_range[1]) and (config.Qy_range[0] <= Qy <=config.Qy_range[1]) and (config.Qz_range[0] <= Qz <=config.Qz_range[1]):
            # print("True")
            i_Qx = int(((Qx-config.Qx_range[0])/dQx))
            j_Qy = int(((Qy-config.Qy_range[0])/dQy))
            Intensity[i_Qx][j_Qy]+=float(Scan_dataframe['Int'][i])
            dataNum[i_Qx][j_Qy]+=1
            # print(Qx,Qy,Qz,Intensity[i_Qx][j_Qy])

    plt.figure(figsize=(8, 8))
    # FHR= open(f"../../2025/June/DAQ_Data/DAQ{config.RunNumber}/Qmap.txt","w")
    FHR= open("Qmap.txt","w")
    for i in range(int(config.mesh_size)):
        for j in range(int(config.mesh_size)):
            Qx=config.Qx_range[0]+dQx*i
            Qy=config.Qy_range[0]+dQy*j
            if Intensity[i][j] > 0:
                FHR.write("{0}  {1}  {2}  {3}\n".format(Qx,Qy,Intensity[i][j],dataNum[i][j]))
                print(i,j,Qx,Qy,Intensity[i][j])
            else:
                FHR.write("{0}  {1}  {2}  {3}\n".format(Qx,Qy,-1000,dataNum[i][j]))
                Intensity[i][j]=-1000
    FHR.close()
    QX,QY = np.meshgrid(np.linspace(config.Qx_range[0],config.Qx_range[1],config.mesh_size),np.linspace(config.Qy_range[0],config.Qy_range[1],config.mesh_size))
    im = plt.pcolormesh(QX,QY,Intensity, cmap='viridis', vmin=-2000, vmax=5000)
    cbar = plt.colorbar(im)
    cbar.set_label("Intensity")
    plt.xlabel("Qx [A$^{-1}$]")
    plt.ylabel("Qy [A$^{-1}$]")
    plt.show()



