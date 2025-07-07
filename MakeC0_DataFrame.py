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

    data_list = []
    for i in range(config.XPN):
        for j in range(config.YPN):
            kf_ch_temp = np.array([config.SDD,config.YPS*(j-config.YCPN),config.XPS*(i-config.XCPN)])
            kf_ch_unit = kf_ch_temp/np.linalg.norm(kf_ch_temp)*k_len
            kf_ch_rotated = rotate_z_cw(kf_ch_unit, config.D2th)
            kf_ch_tilted = rotate_z_cw((kf_ch_rotated-kf_C), config.DTilt) + kf_C
            kf_ch[i*config.XPN+j,:] = kf_ch_tilted
            print(i,j,kf_ch_tilted)

    Q0 = ki-kf_ch
    # print(Q0)

    for i in range(len(Q0)):
        data_list.append(
            {
                "x_ch": i%config.XPN,
                "y_ch": i//config.XPN,
                "Qx": Q0[i,0],
                "Qy": Q0[i,1],
                "Qz": Q0[i,2],
                "Int": 0
            }
        )
    C0_dataframe = pd.DataFrame(data_list)
    C0_dataframe.to_csv(f"../../2025/June/DAQ_Data/DAQ{config.RunNumber}/C0_dataframe.csv", index=False)