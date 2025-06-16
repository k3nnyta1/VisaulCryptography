# 延伸式視覺密碼學（Extended Visual Cryptography）專案說明

## 專案簡介

本專案實現了「延伸式視覺密碼學」的產生與互動式展示。使用者可將一張秘密圖片（secret）與一張偽裝圖片（cover）結合，產生兩張分享圖（share1、share2）。這兩張分享圖分別無法看出秘密內容，但只要將兩張圖重疊，即可還原出原始的秘密圖像。專案同時提供 GUI 互動介面，讓使用者直觀觀察分享圖的重疊效果。

---

## 目錄結構

```
.
├── evc_visual_cryptography.py   # 產生分享圖的主程式
├── visual_crypto_gui.py         # 分享圖重疊效果展示 GUI
├── secret.jpeg                  # 秘密圖片（使用者自備或範例）
├── cover.jpeg                   # 偽裝圖片（使用者自備或範例）
├── share1.jpeg                  # 產生的分享圖1
├── share2.jpeg                  # 產生的分享圖2
```

---

## 執行環境需求

- Python 3.8 以上
- 套件：numpy、Pillow（PIL）、tkinter（標準庫）

安裝依賴：
```bash
pip install numpy pillow
```

---

## 功能說明

### 1. 分享圖產生（evc_visual_cryptography.py）

- **圖片預處理**：將 secret.jpeg 與 cover.jpeg 轉為灰階並調整為 256x256 大小。
- **半色調處理**：採用 Floyd–Steinberg 誤差擴散法將圖片二值化，提升視覺密碼學效果。
- **分享圖生成**：每個像素展開為 2x2 區塊，根據秘密圖與偽裝圖的像素值，決定每張分享圖的棋盤樣式（黑白分布）。
- **輸出**：產生 share1.jpeg 與 share2.jpeg 兩張分享圖。

### 2. 分享圖重疊展示（visual_crypto_gui.py）

- **GUI 介面**：以 tkinter 製作，載入 share1.jpeg 與 share2.jpeg。
- **互動滑桿**：可拖曳滑桿，動態調整兩張分享圖的相對位置，觀察從分開到完全重疊的過程。
- **重疊區域處理**：重疊區域以 0.5 透明度混合，真實模擬紙本重疊效果。
- **錯誤處理**：自動檢查圖片是否存在與尺寸一致性。

---

## 使用方式

### 1. 準備圖片

請準備兩張 256x256 的灰階圖片，分別命名為 `secret.jpeg`（秘密圖）與 `cover.jpeg`（偽裝圖），放在專案目錄下。

### 2. 產生分享圖

```bash
python evc_visual_cryptography.py
```
執行後會產生 `share1.jpeg` 與 `share2.jpeg`。

### 3. 互動式展示

```bash
python visual_crypto_gui.py
```
啟動後會出現 GUI 視窗，可拖曳滑桿觀察分享圖的重疊效果。

---

## 原理說明

- **延伸式視覺密碼學**：將一張秘密圖與一張偽裝圖結合，產生兩張分享圖。單獨觀察任一分享圖無法得知秘密內容，只有將兩張圖重疊，才能還原秘密。
- **重疊區域處理**：每個像素以 2x2 棋盤格方式展開，根據秘密圖與偽裝圖的像素值決定黑白分布。重疊時，黑白棋盤格會產生視覺干涉，還原出秘密圖像。
- **GUI 混合顯示**：重疊區域以透明度混合，模擬現實中兩張透明片重疊的效果。

---

## 注意事項

- 輸入圖片需為 256x256 像素，否則程式會自動縮放。
- 輸入圖片需為灰階（或會自動轉換）。
- 若找不到圖片或圖片尺寸不符，GUI 會自動提示錯誤。

---

## 參考文獻

- Naor, M., & Shamir, A. (1994). Visual cryptography. Advances in Cryptology—EUROCRYPT'94, 1-12.
- Floyd, R. W., & Steinberg, L. (1976). An adaptive algorithm for spatial grey scale. Proceedings of the Society for Information Display, 17(2), 75-77.

---

如需更進階的功能或有任何問題，歡迎提出！ 