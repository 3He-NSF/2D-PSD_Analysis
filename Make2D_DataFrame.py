import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # 3D描画用
import config
import xarray as xr
import pandas as pd

#z軸に対してHorizontal方向にある角度回す関数
def rotate_z_cw(vec: np.ndarray, deg: float) -> np.ndarray:
    theta = np.deg2rad(-deg)
    c, s = np.cos(theta), np.sin(theta)
    Rz = np.array([[c, -s, 0],
                   [s,  c, 0],
                   [0,  0, 1]])
    return vec @ Rz.T


if __name__ == "__main__":

    #y軸にkiの線を描画
    k_len = 2.0*np.pi/config.WL
    ki = np.array([1,0, 0])*k_len

    #検出器中心のx,y channelの位置を描画　(kfの描画)
    kf = np.array([config.SDD,config.DW*config.XCPN,config.DH*config.YCPN])
    #kfを回転
    kf_rotated = rotate_z_cw(kf, config.D2th)
    # ─── 2. 公転：回転後の中心点を取得 ───────────────
    kf_C = np.append(kf_rotated[:2], 0.0)         # shape (3,)

    #kfを検出器のch分用意する。64x64のch分
    kf_ch = np.zeros((config.XPN*config.YPN, 3))
    for i in range(config.XPN):
        for j in range(config.YPN):
            kf_ch_temp = np.array([config.SDD,config.YPS*(j-config.YCPN),config.XPS*(i-config.XCPN)])
            kf_ch_unit = kf_ch_temp/np.linalg.norm(kf_ch_temp)*k_len
            kf_ch_rotated = rotate_z_cw(kf_ch_unit, config.D2th)
            kf_ch_tilted = rotate_z_cw((kf_ch_rotated-kf_C), config.DTilt) + kf_C
            kf_ch[i*config.XPN+j,:] = kf_ch_tilted
    Q0 = ki-kf_ch
    print(Q0)


    #ScanListの読み込み
    ScanList = pd.read_csv(f"../../2025/June/DAQ_Data/DAQ{config.RunNumber}/DAQ{config.RunNumber}_{config.csvName}.csv", header=None, names=["Scan No.","omega","start","end"],skiprows=1)

    data_list = []
    for i in range(len(ScanList)):
        #ファイル名
        filename = f"../../2025/June/DAQ_Data/DAQ{config.RunNumber}/01_102+q/DAQ{config.RunNumber:04d}_Scan{int(ScanList['Scan No.'][i]):04d}.txt"
        #ファイルを読み込む
        df = pd.read_csv(filename, header=None, skiprows=3, sep="\s+",names=["X ch","Y ch","Int"])
        for j in range(len(df)):
            data_list.append(
                {
                    "Scan No.": ScanList['Scan No.'][i],
                    "omega": ScanList['omega'][i],
                    "X ch": df['X ch'][j],
                    "Y ch": df['Y ch'][j],
                    "Int": df['Int'][j],
                    "Qx": rotate_z_cw(Q0[j,:], float(ScanList['omega'][i]))[0],
                    "Qy": rotate_z_cw(Q0[j,:], float(ScanList['omega'][i]))[1],
                    "Qz": rotate_z_cw(Q0[j,:], float(ScanList['omega'][i]))[2]
                }
            )
    Scan_dataframe = pd.DataFrame(data_list)
    Scan_dataframe.to_csv(f"../../2025/June/DAQ_Data/DAQ{config.RunNumber}/Scan_dataframe.csv", index=False)