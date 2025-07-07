import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # 3D描画用
import config
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
    # 3Dプロットのセットアップ
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    Qdata = pd.read_csv(f"../../2025/June/DAQ_Data/DAQ{config.RunNumber}/C0_dataframe.csv")

    omega = -51.0 #deg
    Q_xyz = Qdata[['Qx', 'Qy', 'Qz']].values  # shape: (N, 3)
    Q_xyz_rotated = rotate_z_cw(Q_xyz, -omega)
    ax.scatter(Q_xyz[:,0], Q_xyz[:,1], Q_xyz[:,2], cmap='viridis',marker='o',s=0.1)
    ax.scatter(Q_xyz_rotated[:,0], Q_xyz_rotated[:,1], Q_xyz_rotated[:,2], cmap='viridis',marker='o',s=0.1)
    ax.set_xlabel("Qx [A$^{-1}$]")
    ax.set_ylabel("Qy [A$^{-1}$]")
    ax.set_zlabel("Qz [A$^{-1}$]")
    ax.set_xlim(0,2)
    ax.set_ylim(0,2)
    ax.set_zlim(-1,1)
    plt.show()