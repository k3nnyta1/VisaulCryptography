from __future__ import annotations  # 支援型別提示 forward reference

import os
from typing import Tuple

import numpy as np
from PIL import Image


# --------------------------------------------------
# 1. 圖片準備函式
# --------------------------------------------------

def prepare_images(secret_path: str, cover_path: str, size: Tuple[int, int] = (256, 256)) -> Tuple[Image.Image, Image.Image]:
    # 讀取並預處理兩張圖片：轉為灰階並調整大小
    secret_img = Image.open(secret_path).convert("L").resize(size, Image.LANCZOS)
    cover_img = Image.open(cover_path).convert("L").resize(size, Image.LANCZOS)
    return secret_img, cover_img


# --------------------------------------------------
# 2. Floyd–Steinberg 誤差擴散半色調
# --------------------------------------------------

def apply_floyd_steinberg(image: Image.Image) -> np.ndarray:
    # 將圖片轉為浮點數陣列以便計算誤差
    arr = np.asarray(image, dtype=np.float32)
    height, width = arr.shape

    # 使用 Floyd-Steinberg 算法進行誤差擴散半色調處理
    for y in range(height):
        for x in range(width):
            # 將像素二值化（以 128 為閾值）
            old_pixel = arr[y, x]
            new_pixel = 255.0 if old_pixel >= 128 else 0.0
            arr[y, x] = new_pixel
            quant_error = old_pixel - new_pixel

            # 將量化誤差分散到鄰近像素（權重：7/16, 3/16, 5/16, 1/16）
            if x + 1 < width:
                arr[y, x + 1] += quant_error * 7 / 16  # 右側像素
            if x - 1 >= 0 and y + 1 < height:
                arr[y + 1, x - 1] += quant_error * 3 / 16  # 左下像素
            if y + 1 < height:
                arr[y + 1, x] += quant_error * 5 / 16  # 下方像素
            if x + 1 < width and y + 1 < height:
                arr[y + 1, x + 1] += quant_error * 1 / 16  # 右下像素

    # 將值限制在 0-255 範圍內並轉為整數
    return np.clip(arr, 0, 255).astype(np.uint8)


# --------------------------------------------------
# 3. 產生延伸式視覺密碼學分享圖
# --------------------------------------------------

def generate_shares(secret_ht: np.ndarray, cover_ht: np.ndarray) -> Tuple[Image.Image, Image.Image]:
    # 檢查輸入圖片尺寸是否一致
    if secret_ht.shape != cover_ht.shape:
        raise ValueError("secret_ht 與 cover_ht 必須具有相同尺寸！")

    height, width = secret_ht.shape
    # 建立兩張分享圖的陣列（每個像素展開為 2x2 區塊）
    share1_array = np.zeros((height * 2, width * 2), dtype=np.uint8)
    share2_array = np.zeros_like(share1_array)

    # 定義黑白棋盤樣式（用於生成分享圖）
    pattern_white = np.array([[255, 0], [0, 255]], dtype=np.uint8)  # 白色棋盤
    pattern_black = np.array([[0, 255], [255, 0]], dtype=np.uint8)  # 黑色棋盤

    # 根據秘密圖和偽裝圖的像素值生成分享圖
    for y in range(height):
        for x in range(width):
            secret_pixel = secret_ht[y, x]
            cover_pixel = cover_ht[y, x]

            # 根據秘密圖和偽裝圖的像素值選擇對應的 2x2 區塊
            if secret_pixel == 255:  # 秘密圖為白色
                block1 = block2 = pattern_white if cover_pixel == 255 else pattern_black
            else:  # 秘密圖為黑色
                if cover_pixel == 255:
                    block1, block2 = pattern_white, pattern_black
                else:
                    block1, block2 = pattern_black, pattern_white

            # 將 2x2 區塊放入對應位置
            y_pos, x_pos = y * 2, x * 2
            share1_array[y_pos:y_pos + 2, x_pos:x_pos + 2] = block1
            share2_array[y_pos:y_pos + 2, x_pos:x_pos + 2] = block2

    # 將陣列轉換為圖片並返回
    return Image.fromarray(share1_array, mode="L"), Image.fromarray(share2_array, mode="L")


# --------------------------------------------------
# 4. 主程式執行入口
# --------------------------------------------------

def main() -> None:
    # 設定輸入檔案路徑
    secret_path = "secret.jpeg"
    cover_path = "cover.jpeg"

    # 檢查輸入檔案是否存在
    if not (os.path.exists(secret_path) and os.path.exists(cover_path)):
        print("[ERROR] 找不到 secret.png 或 cover.png，請檢查檔案是否存在於腳本相同目錄。")
        return

    # 執行視覺密碼學流程
    secret_img, cover_img = prepare_images(secret_path, cover_path)
    print("[INFO] 已載入並預處理圖片 (灰階 & 調整尺寸)。")

    # 進行半色調處理
    secret_ht = apply_floyd_steinberg(secret_img)
    cover_ht = apply_floyd_steinberg(cover_img)
    print("[INFO] 完成 Floyd–Steinberg 半色調。")

    # 生成並儲存分享圖
    share1_img, share2_img = generate_shares(secret_ht, cover_ht)
    share1_img.save("share1.jpeg", format="JPEG")
    share2_img.save("share2.jpeg", format="JPEG")
    print("[SUCCESS] 程式執行完成！已產生 share1.jpeg 與 share2.jpeg。")


if __name__ == "__main__":
    main() 