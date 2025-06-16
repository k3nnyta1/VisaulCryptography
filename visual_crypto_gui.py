# 視覺密碼學分享圖展示 GUI：用於展示兩張分享圖的重疊效果
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

class App:
    def __init__(self):
        # 初始化主視窗
        self.root = tk.Tk()
        self.root.title("視覺密碼學成果展示")

        # 載入兩張分享圖
        try:
            self.left_image = Image.open("share1.jpeg").convert("RGBA")  # 轉為 RGBA 以支援透明度
            self.right_image = Image.open("share2.jpeg").convert("RGBA")
        except Exception as e:
            messagebox.showerror("錯誤", f"找不到 share1.jpeg 或 share2.jpeg\n{e}")
            self.root.destroy()
            return

        # 確保兩張圖片尺寸相同
        if self.left_image.size != self.right_image.size:
            messagebox.showerror("錯誤", "兩張圖片尺寸不一致！")
            self.root.destroy()
            return

        # 設定畫布尺寸（略大於兩張圖片的總寬度）
        self.img_width, self.img_height = self.left_image.size
        self.canvas_width = self.img_width * 2 + 40
        self.canvas_height = self.img_height + 40

        # 建立畫布和說明文字
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(pady=10)
        self.label = tk.Label(self.root, text="請拖動滑桿觀察圖片靠攏與重疊區域透明效果", font=("微軟正黑體", 12))
        self.label.pack(pady=5)

        # 建立控制滑桿（0-100）
        self.scale = ttk.Scale(self.root, from_=0, to=100, orient="horizontal", command=self.update_image, length=self.canvas_width-40)
        self.scale.set(0)  # 預設位置：最左側
        self.scale.pack(pady=10)

        # 初始化顯示狀態
        self.display_photo = None
        self.image_on_canvas = None
        self.update_image(self.scale.get())

        # 固定視窗大小並啟動主迴圈
        self.root.resizable(False, False)
        self.root.mainloop()

    def update_image(self, value):
        # 將滑桿值轉換為 0-1 範圍的插值係數
        try:
            t = float(value) / 100  # t=0: 分開, t=1: 重疊
        except Exception:
            t = 0

        # 計算兩張圖片的位置
        left_start_x = 20  # 左圖起始位置
        right_start_x = self.canvas_width - self.img_width - 20  # 右圖起始位置
        center_x = (self.canvas_width - self.img_width) // 2  # 重疊時的中心位置
        y = (self.canvas_height - self.img_height) // 2  # 垂直置中

        # 根據插值係數計算當前位置
        left_x = int(left_start_x * (1-t) + center_x * t)
        right_x = int(right_start_x * (1-t) + center_x * t)

        # 建立透明背景的合成圖
        composite = Image.new("RGBA", (self.canvas_width, self.canvas_height), (255,255,255,0))
        
        # 貼上兩張圖片
        composite.paste(self.left_image, (left_x, y), self.left_image)
        composite.paste(self.right_image, (right_x, y), self.right_image)

        # 處理重疊區域
        overlap_x1 = max(left_x, right_x)
        overlap_x2 = min(left_x + self.img_width, right_x + self.img_width)
        if overlap_x2 > overlap_x1:  # 如果有重疊
            # 計算重疊區域的寬度
            overlap_width = overlap_x2 - overlap_x1
            # 取出重疊部分的圖片
            left_crop = self.left_image.crop((overlap_x1 - left_x, 0, overlap_x1 - left_x + overlap_width, self.img_height))
            right_crop = self.right_image.crop((overlap_x1 - right_x, 0, overlap_x1 - right_x + overlap_width, self.img_height))
            # 混合重疊區域（alpha = 0.5）
            blended = Image.blend(left_crop, right_crop, 0.5)
            # 將混合後的區域貼回合成圖
            composite.paste(blended, (overlap_x1, y), blended)

        # 更新畫布顯示
        self.display_photo = ImageTk.PhotoImage(composite)
        if self.image_on_canvas is None:
            self.image_on_canvas = self.canvas.create_image(0, 0, anchor="nw", image=self.display_photo)
        else:
            self.canvas.itemconfigure(self.image_on_canvas, image=self.display_photo)

if __name__ == "__main__":
    App() 