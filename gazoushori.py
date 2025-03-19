import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np

# Tkinter の GUI を非表示
root = tk.Tk()
root.withdraw()

# 画像ファイルを選択
file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])

# 画像が選択されなかった場合、プログラム終了
if not file_path:
    print("画像が選択されませんでした。プログラムを終了します。")
    exit()

# 画像を読み込む
img = cv2.imread(file_path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# 画像保存用の変数（メモリ上に保持）
Processing_img = None

# マウス操作の関数
def mouseEvents(event, x, y, flags, param):
    global Processing_img  

    if event == cv2.EVENT_LBUTTONDOWN:
        param['drawing'] = True
        param['start_x'] = x
        param['start_y'] = y
        print(f"開始: ({x}, {y}) - RGB値: {img[y, x]}")

    elif event == cv2.EVENT_MOUSEMOVE:
        if param['drawing']:
            img_copy = img.copy()
            cv2.rectangle(img_copy, (param['start_x'], param['start_y']), (x, y), (0, 0, 0), 2)
            cv2.imshow("image", img_copy)

    elif event == cv2.EVENT_LBUTTONUP:
        param["drawing"] = False
        param['goal_x'] = x
        param['goal_y'] = y

        img_copy = img.copy()
        cv2.rectangle(img_copy, (param['start_x'], param['start_y']), (x, y), (0, 0, 0), 2)
        cv2.imshow("image", img_copy)
        cv2.waitKey(500)
        cv2.destroyAllWindows()
        print(f"終了: ({x}, {y}) - RGB値: {img[y, x]}")

        # 画像の切り出し
        x1, y1, x2, y2 = min(param['start_x'], param['goal_x']), min(param['start_y'], param['goal_y']), max(param['start_x'], param['goal_x']), max(param['start_y'], param['goal_y'])
        
        Processing_img = img[y1:y2, x1:x2].copy()  # 切り取った画像をコピー

        if Processing_img.size == 0:
            print("選択範囲が無効です。")
            Processing_img = None
            return

        print("画像をメモリ上に保存しました。")

# 参照用パラメータ
Processing_img = None
mouse_param = {'drawing': False, 'mode': True, 'start_x': -1, 'start_y': -1, 'goal_x': -1, 'goal_y': -1}

# 画像を表示
cv2.imshow("image", img)
cv2.setMouseCallback("image", mouseEvents, mouse_param)

# ウィンドウを閉じるまで待機
cv2.waitKey(0)
cv2.destroyAllWindows()

# 画像処理
if Processing_img is None:
    print("画像が選択されていません。処理を終了します。")
    exit()

# 何も処理をしない場合のコールバック関数
def nothing(x):
    pass

# 画像を表示する
cv2.namedWindow('change')

# RGB色空間で色を変更するトラックバーの作成
cv2.createTrackbar('Red', 'change', 0, 255, nothing)
cv2.createTrackbar('Green', 'change', 0, 255, nothing)
cv2.createTrackbar('Blue', 'change', 0, 255, nothing)

# HSV色空間で色を変更するトラックバーの作成
cv2.createTrackbar('Hue', 'change', 0, 255, nothing)
cv2.createTrackbar('Saturation', 'change', 0, 255, nothing)
cv2.createTrackbar('Value', 'change', 0, 255, nothing)

# ON時にRGB色空間の色を表示、OFF時にHSV色空間の色を表示するトラックバーの作成
cv2.createTrackbar('switch', 'change', 0, 1, nothing)

while True:
    switch = cv2.getTrackbarPos('switch', 'change')

    # 元の画像をコピー
    modified_img = Processing_img.copy()

    # RGB色空間の色を変更
    if switch == 1:
        r = cv2.getTrackbarPos('Red', 'change')
        g = cv2.getTrackbarPos('Green', 'change')
        b = cv2.getTrackbarPos('Blue', 'change')

        # RGBの値を適用
        modified_img[:, :, 0] = b
        modified_img[:, :, 1] = g
        modified_img[:, :, 2] = r
    
    # HSV色空間の色を変更
    else:
        h = cv2.getTrackbarPos('Hue', 'change')
        s = cv2.getTrackbarPos('Saturation', 'change')
        v = cv2.getTrackbarPos('Value', 'change')

        # 画像をHSVに変換
        hsv_img = cv2.cvtColor(modified_img, cv2.COLOR_RGB2HSV)

        # HSV値を変更
        hsv_img[:, :, 0] = h
        hsv_img[:, :, 1] = s
        hsv_img[:, :, 2] = v

        # HSVをBGRに戻す
        modified_img = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2RGB)

    # 表示
    cv2.imshow('change', modified_img)

    # キーが押されたらループを抜ける
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
