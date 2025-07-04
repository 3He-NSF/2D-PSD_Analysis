


#検出器のパラメーター
SDD = 766 #Sample-Detector Distance #mm
XPS, YPS = 4,4 #PixelSize #mm
XPN, YPN = 64, 64 #PixelNumber
XCPN, YCPN = 31.5, 31.5 #CenterPixelNumber
DW = XPS * XPN #DetectorWidth #mm
DH = YPS * YPN #DetectorHeight #mm
dH = 0 #検出器の高さ方向のズレ #mm
D2th = 32 #検出器2theta #deg
# D2th = 0
DTilt = 0 #検出器傾斜角 #deg

#波長
WL = 2.36 #nm


#データの読み込み
RunNumber = 413
csvName = "102+q"


mesh_size = 500
Qx_range = [-2.0, 0.0]
Qy_range = [0.0, 2.0]
Qz_range = [-0.1, 0.1]








