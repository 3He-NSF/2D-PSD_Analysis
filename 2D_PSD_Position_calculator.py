import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # 3D描画用
import config
import xarray as xr

#z軸に対してHorizontal方向にある角度回す関数
def rotate_z_cw(vec: np.ndarray, deg: float) -> np.ndarray:
    theta = np.deg2rad(-deg)
    c, s = np.cos(theta), np.sin(theta)
    Rz = np.array([[c, -s, 0],
                   [s,  c, 0],
                   [0,  0, 1]])
    return vec @ Rz.T

def Figure_3D():
    # 3Dプロットのセットアップ
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    # 軸の範囲設定
    ax.set_xlim([-200, 800])
    ax.set_ylim([-800, 200])
    ax.set_zlim([-500, 500])

    # 軸ラベル
    ax.set_xlabel('ki direction')
    ax.set_ylabel('Horizontal')
    ax.set_zlabel('Vertical')

    # 中心に球体（試料）を描画
    r = 10  # 球の半径
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = r * np.outer(np.cos(u), np.sin(v))
    y = r * np.outer(np.sin(u), np.sin(v))
    z = r * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z, color='b', alpha=0.6)

    #x軸の点線に対してHorizontal方向にある角度回した線を描画
    y_line = np.array([config.SDD, 0, 0])
    rotated_y_line = rotate_z_cw(y_line, config.D2th)
    rotated_y_line_unit = rotated_y_line / np.linalg.norm(rotated_y_line)
    ax.plot([0, rotated_y_line[0]], [0, rotated_y_line[1]], [0, rotated_y_line[2]], color='blue', linestyle='-')

    # ── xy 平面内の法線 n を作る（v に直交） ─────────────
    n = np.array([-rotated_y_line[1], rotated_y_line[0], 0.0])
    n = n / np.linalg.norm(n)*config.DW
    # ── 可視化（rotated_y_lineから法線を描く） ───────────────────
    ax.plot([rotated_y_line[0]-n[0]/2, rotated_y_line[0] + n[0]/2],
            [rotated_y_line[1]-n[1]/2, rotated_y_line[1] + n[1]/2],
            [rotated_y_line[2]-n[2]/2, rotated_y_line[2] + n[2]/2],
            color='blue', linestyle='-')
    return ax


if __name__ == "__main__":
    ax = Figure_3D()

    #y軸にkiの線を描画
    k_len = 2.0*np.pi/config.WL
    ki = np.array([1,0, 0])*k_len
    ax.plot([0, ki[0]], [0, ki[1]], [0, ki[2]], color='gray', linestyle='--')

    #検出器をイメージした四角形を描画
    # --- 各頂点の座標 ---
    x_line_detector = np.array([config.SDD, config.SDD, config.SDD, config.SDD, config.SDD])           # y=0 で固定  →  x-z 平面になる
    y_line_detector = np.array([-config.DW/2,  config.DW/2,  config.DW/2,  -config.DW/2,  -config.DW/2])   # x 座標：左下→右下→右上→左上→左下
    z_line_detector = np.array([-config.DH/2+config.dH, -config.DH/2+config.dH, config.DH/2+config.dH, config.DH/2+config.dH, -config.DH/2+config.dH])   # z 座標：左下→右下→右上→左上→左下
    #Vectorを作成
    Detector_Rectangle = np.column_stack([x_line_detector, y_line_detector, z_line_detector])
    #回転
    Detector_Rectangle_rotated = rotate_z_cw(Detector_Rectangle, config.D2th)
    # ─── 2. 公転後の中心点を取得 ───────────────
    Det_center_xy = Detector_Rectangle_rotated[:, :2].mean(axis=0)
    Det_C = np.append(Det_center_xy, 0.0)         # shape (3,)
    # ─── 3. 自転：中心点まわりに β 回す ────────
    Detector_Rectangle_spinned = rotate_z_cw((Detector_Rectangle_rotated-Det_C), config.DTilt)
    Detector_Rectangle_tilted = Detector_Rectangle_spinned + Det_C
    ax.plot(Detector_Rectangle_tilted[:,0], Detector_Rectangle_tilted[:,1], Detector_Rectangle_tilted[:,2],color='gray', linestyle='-')

    #指定したx,y channelの位置を描画　(kfの描画)
    kf = np.array([config.SDD,config.DW*(config.x_ch-config.XCPN)/config.XPN,config.DH*(config.y_ch-config.YCPN)/config.YPN])
    #kfを回転
    kf_rotated = rotate_z_cw(kf, config.D2th)
    # ─── 2. 公転：回転後の中心点を取得 ───────────────
    kf_C = np.append(Det_center_xy, 0.0)         # shape (3,)
    # ─── 3. 自転：中心点まわりに β 回す ────────
    # ax.plot([0,kf_rotated[0]], [0,kf_rotated[1]], [0,kf_rotated[2]],color='red', linestyle='-')
    kf_spinned = rotate_z_cw((kf_rotated-kf_C), config.DTilt)
    kf_tilted = kf_spinned + kf_C
    ax.plot([0,kf_tilted[0]], [0,kf_tilted[1]], [0,kf_tilted[2]],color='red', linestyle='-')

    #kfを検出器のch分用意する。64x64のch分
    kf_ch = np.zeros((config.XPN, config.YPN, 3))
    print(kf_ch.shape)
    for i in range(config.XPN):
        for j in range(config.YPN):
            kf_ch_temp = np.array([config.SDD,config.YPS*(j-config.YCPN),config.XPS*(i-config.XCPN)])
            kf_ch_unit = kf_ch_temp/np.linalg.norm(kf_ch_temp)*k_len
            kf_ch_rotated = rotate_z_cw(kf_ch_unit, config.D2th)
            kf_ch_tilted = rotate_z_cw((kf_ch_rotated-kf_C), config.DTilt) + kf_C
            print(kf_ch_tilted)
            kf_ch[i,j,:] = kf_ch_tilted

    kf_da = xr.DataArray(
        kf_ch,
        dims=("y_ch", "x_ch", "kf"),
        coords={"y_ch": np.arange(config.YPN),
                "x_ch": np.arange(config.XPN),
                "kf": np.arange(3)},
        name="kf")
        # attrs={"units": "1/nm"})




    #kfを規格化
    kf_unit = kf_tilted / np.linalg.norm(kf_tilted)
    #kiを規格化
    ki_unit = ki / np.linalg.norm(ki)
    #Q vectorを描画
    Q = (kf_unit - ki_unit)
    print("Q",Q)

    plt.show()
