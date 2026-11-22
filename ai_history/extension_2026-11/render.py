# -*- coding: utf-8 -*-
"""鎵╁睍鐗?AI 鍙戝睍鏃堕棿杞?v2锛?026.10.18 -> 2026.11.23锛?6 澶╋級"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import os

W, H = 1600, 1120
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "timeline_2026-11-23.png")

GOLD = (232, 184, 75)
GOLD_HI = (255, 216, 140)
WHITE = (233, 229, 219)
GRAY = (152, 146, 135)
DIM = (98, 92, 84)

F = r"C:\Windows\Fonts"
def font(name, size):
    return ImageFont.truetype(os.path.join(F, name), size)

f_title = font("STSONG.TTF", 74)
f_head = font("msyhbd.ttc", 21)
f_label = font("msyh.ttc", 13)
f_labelb = font("msyhbd.ttc", 14)
f_sub = font("msyh.ttc", 12)
f_big = font("msyhbd.ttc", 40)
f_mid = font("msyhbd.ttc", 23)
f_tiny = font("msyh.ttc", 11)
f_date = font("msyhbd.ttc", 14)
f_row = font("msyh.ttc", 19)

# ---------- background ----------
arr = np.zeros((H, W, 3), dtype=np.float32)
for y in range(H):
    k = y / H
    arr[y, :, :] = np.array([7, 5, 3]) * (1 - k) + np.array([20, 14, 8]) * k
base = Image.fromarray(arr.astype(np.uint8))

glow_bg = Image.new("RGB", (W, H), (0, 0, 0))
ImageDraw.Draw(glow_bg).ellipse([1000 - 300, 400 - 240, 1000 + 300, 400 + 240], fill=(58, 40, 17))
glow_bg = glow_bg.filter(ImageFilter.GaussianBlur(95))
base = Image.fromarray(np.clip(np.asarray(base).astype(np.int16) + np.asarray(glow_bg).astype(np.int16), 0, 255).astype(np.uint8))

# ---------- main curve ----------
anchors = [
    (1943, 80, 0.02), (1956, 215, 0.06), (1958, 255, 0.07),
    (1974, 350, 0.05), (1986, 450, 0.09), (1987, 478, 0.07),
    (1997, 565, 0.13), (2012, 680, 0.18), (2016, 740, 0.24),
    (2017, 780, 0.28), (2020, 830, 0.36), (2022.92, 878, 0.50),
    (2023.2, 894, 0.56), (2024.7, 918, 0.63), (2025.05, 934, 0.69),
    (2025.55, 948, 0.74), (2026.38, 980, 0.80), (2026.69, 1006, 0.87),
    (2026.80, 1040, 0.93),
]
xs = np.array([a[1] for a in anchors], dtype=float)
lv = np.array([a[2] for a in anchors], dtype=float)
BASE_Y, AMP = 700.0, 380.0

def level_at(x): return float(np.interp(x, xs, lv))
def y_at(x): return BASE_Y - level_at(x) * AMP
def curve_points():
    return [(float(x), y_at(float(x))) for x in np.arange(80, 1040.5, 1.0)]

glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(glow).line(curve_points(), fill=(255, 185, 70, 210), width=10, joint="curve")
glow = glow.filter(ImageFilter.GaussianBlur(10))
base = Image.alpha_composite(base.convert("RGBA"), glow).convert("RGB")
d = ImageDraw.Draw(base)

overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(overlay).polygon(curve_points() + [(1040, BASE_Y + 6), (80, BASE_Y + 6)], fill=(150, 100, 30, 26))
base = Image.alpha_composite(base.convert("RGBA"), overlay).convert("RGB")
d = ImageDraw.Draw(base)

d.line(curve_points(), fill=(255, 208, 108), width=2, joint="curve")
d.line([(80, BASE_Y + 6), (1040, BASE_Y + 6)], fill=(70, 58, 36), width=1)

axis = [(1943, 80, "la"), (1960, 222, "ma"), (1980, 385, "ma"), (2000, 550, "ma"),
        (2012, 680, "ma"), (2020, 830, "ma"), (2026, 1040, "ra")]
for yr, x, anc in axis:
    d.line([(x, BASE_Y + 2), (x, BASE_Y + 11)], fill=(90, 72, 40), width=1)
    d.text((x, BASE_Y + 20), str(yr), font=f_tiny, fill=DIM, anchor=anc)

# ---------- left/mid labels ----------
labels = [
    (80, "1943 绁炵粡鍏冩ā鍨?, 1),
    (215, "1956 杈剧壒鑼呮柉浼氳", 2),
    (255, "1958 鎰熺煡鏈?, 0),
    (350, "1974 绗竴娆″瘨鍐?, 1),
    (462, "1986 鍙嶅悜浼犳挱", 0),
    (478, "1987 绗簩娆″瘨鍐?, 2),
    (565, "1997 娣辫摑", 1),
    (680, "2012 AlexNet", 0),
    (740, "2016 AlphaGo", 1),
    (780, "2017 Transformer", 2),
    (830, "2020 GPT-3", 0),
]
for x, text, tier in labels:
    cy = y_at(x)
    ly = cy - 22 - tier * 26
    d.line([(x, cy - 5), (x, ly + 10)], fill=(110, 88, 46), width=1)
    d.text((x, ly), text, font=f_label, fill=WHITE, anchor="mb")
    d.ellipse([x - 2.4, cy - 2.4, x + 2.4, cy + 2.4], fill=(255, 226, 160))
    d.ellipse([x - 5.6, cy - 5.6, x + 5.6, cy + 5.6], outline=(180, 130, 50), width=1)

# ---------- late labels: staircase to upper-right ----------
late = [
    (878, "2022.11 ChatGPT", 878 + 14, 0),
    (894, "2023.03 GPT-4", 894 + 14, -40),
    (918, "2024.09 o1", 918 + 14, -66),
    (934, "2025.01 R1", 934 + 14, -92),
    (948, "2025.07 濂ユ暟閲戠墝", 948 + 14, -118),
    (980, "2026.05 Erd艖s", 980 + 14, -146),
    (1006, "2026.09 鍗冪Η棰?, 1006 + 14, -172),
]
for x, text, tx, dy in late:
    cy = y_at(x)
    ly = cy + dy
    d.line([(x + 4, cy - 2), (tx - 4, ly + 4)], fill=(120, 94, 48), width=1)
    d.text((tx, ly), text, font=f_label, fill=GOLD_HI if text.startswith("2026") else WHITE, anchor="lm")
    d.ellipse([x - 2.4, cy - 2.4, x + 2.4, cy + 2.4], fill=(255, 226, 160))
    d.ellipse([x - 5.6, cy - 5.6, x + 5.6, cy + 5.6], outline=(180, 130, 50), width=1)

# ---------- peak ----------
px, py = 1040, y_at(1040)
gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(gl).ellipse([px - 46, py - 46, px + 46, py + 46], fill=(255, 200, 100, 130))
gl = gl.filter(ImageFilter.GaussianBlur(17))
base = Image.alpha_composite(base.convert("RGBA"), gl).convert("RGB")
d = ImageDraw.Draw(base)
d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=(255, 240, 200))

# zoom connector
def dashed(x0, y0, x1, y1, n=18):
    for i in range(n):
        t0, t1 = i / n, (i + 0.55) / n
        d.line([(x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0),
                (x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1)], fill=(140, 108, 46), width=1)
dashed(px, py, 1092, py)
dashed(1092, py, 1092, 894)

# epigraph
d.line([(60, 172), (150, 172)], fill=(170, 130, 55), width=1)
d.text((60, 208), "浠庝笂涓€鐗堝埌浠婂ぉ锛屽彧杩囦簡 36 澶┿€?, font=font("msyh.ttc", 22), fill=GRAY, anchor="lm")
t1, t2 = "涓ら亾鍗冪Η棰?, "锛屽悇琚帹杩涗簡涓€澶ф銆?
d.text((60, 256), t1, font=font("msyhbd.ttc", 34), fill=GOLD_HI, anchor="lm")
w1 = d.textlength(t1, font=font("msyhbd.ttc", 34))
d.text((60 + w1, 256), t2, font=font("msyhbd.ttc", 34), fill=WHITE, anchor="lm")

# ---------- right panel ----------
PANEL = 1120
d.line([(PANEL, 292), (PANEL, 916)], fill=(70, 58, 36), width=1)
d.text((PANEL + 18, 236), "鏈€鍚?36 澶?, font=f_head, fill=GOLD_HI, anchor="lm")
d.text((PANEL + 18, 262), "2026.10.18 鈫?11.23", font=f_sub, fill=GRAY, anchor="lm")

entries = [
    ("10.18", "涓婁竴鐗堢粓鐐?, "1418 澶?, DIM, 292),
    ("11.08", "閲忓瓙鍔犻€熺寽鎯?, "Aaronson鈥揂mbainis 路 3 澶?, GOLD, 392),
    ("11.11", "鏉ㄢ€撶背灏旀柉銆屽瓨鍦ㄦ€с€?, "鍗冪Η棰樹箣涓€ 路 璐ㄩ噺闂撮殭鏈В", GOLD, 492),
    ("11.20", "GPT-6.2锛?4 鍒嗛挓褰㈠紡鍖栭璇?, "棣栦釜 Lean 璇佹槑 路 鑷€犳柊璇佹硶", GOLD, 598),
    ("11.20", "Claude锛氶粠鏇肩寽鎯?, "1,700 涓囪 Lean 路 167 骞?, GOLD_HI, 700),
    ("11.21", "Lean 绀惧尯鏍搁獙閫氳繃", "175,187 涓ā鍧?路 澶氬妫€鏌ュ櫒", GOLD, 800),
    ("11.23", "浠婂ぉ", "1454 澶?路 Clay 浠嶅垪鏈В", WHITE, 894),
]
for date, title, sub, col, y in entries:
    if date == "11.23":
        gl2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(gl2).ellipse([PANEL - 30, y - 30, PANEL + 30, y + 30], fill=(255, 210, 120, 150))
        gl2 = gl2.filter(ImageFilter.GaussianBlur(13))
        base = Image.alpha_composite(base.convert("RGBA"), gl2).convert("RGB")
        d = ImageDraw.Draw(base)
    d.text((PANEL - 12, y), date, font=f_date, fill=GOLD_HI if date != "10.18" else DIM, anchor="rm")
    d.ellipse([PANEL - 5, y - 5, PANEL + 5, y + 5], fill=(255, 238, 190) if date == "11.23" else (255, 210, 130))
    d.ellipse([PANEL - 11, y - 11, PANEL + 11, y + 11], outline=(150, 110, 45), width=1)
    d.text((PANEL + 24, y - 9), title, font=f_labelb, fill=col, anchor="lm")
    d.text((PANEL + 24, y + 13), sub, font=f_sub, fill=GRAY, anchor="lm")

d.text((PANEL + 24, 728), "鍚屾棩锛氫汉绫?12 骞?/ 940 椤垫墜绋匡紙鏃?AI锛?, font=f_sub, fill=(122, 114, 102), anchor="lm")

# ---------- comparisons ----------
d.line([(60, 742), (1080, 742)], fill=(60, 50, 32), width=1)
rows = [
    ("浠庨粠鏇?1859 骞存彁鍑猴紝鍒?AI 鍙備笌鐨勮瘉鏄?, "167 骞?),
    ("浠庤瘉鏄庡叕寮€锛屽埌绀惧尯鐙珛鏍搁獙", "1 澶?),
    ("浠庝竴閬撳崈绂ч锛屽埌鍙︿竴閬撳崈绂ч", "73 澶?),
]
y = 775
for text, num in rows:
    d.text((60, y), text, font=f_row, fill=WHITE, anchor="lm")
    d.text((720, y), num, font=f_big, fill=GOLD_HI, anchor="rm")
    y += 52

d.text((60, 930), "1943 鈫?GPT-3.5锛?9 骞?, font=f_mid, fill=GOLD, anchor="lm")
d.text((1080, 930), "GPT-3.5 鈫?浠婂ぉ锛?454 澶?, font=f_mid, fill=GOLD_HI, anchor="rm")

# ---------- header ----------
d.text((60, 46), "AI 鍙戝睍", font=f_head, fill=GRAY, anchor="lm")
d.text((60, 74), "1943 鈥?2026.11.23", font=f_sub, fill=DIM, anchor="lm")
d.text((1540, 40), "2026.11.23", font=f_title, fill=GOLD_HI, anchor="ra")
d.text((1540, 120), "浠婂ぉ", font=font("msyh.ttc", 18), fill=GRAY, anchor="ra")

# ---------- flash strip ----------
d.text((60, 966), "鍚屼竴鏃堕棿锛屼竴闂€岃繃鐨?, font=font("msyh.ttc", 15), fill=GRAY, anchor="lm")
d.text((1540, 966), "鏃ユ湡 + 鍚嶅瓧 + 鍋氫簡浠€涔?, font=f_tiny, fill=(105, 99, 90), anchor="rm")

chips = [
    ("10.26", "Dessa", "绾煶棰?路 绔埌绔?, "鏂规硶"),
    ("11.13", "H-Net", "鏃犲垎璇嶅櫒 路 鏂版灦鏋?, "鏂规硶"),
    ("11.17", "GPT-6.2", "Astra / Sol 鍙屽彂", "妯″瀷"),
    ("11.17", "鑷垜鏀硅繘", "棣栦釜 High 绛夌骇", "鑳藉姏"),
    ("11.19", "AI 鐭墽", "鐪熶汉鎷嶆憚鐮嶄節鎴?, "搴旂敤"),
    ("11.22", "FSD V15", "瀹夊叏鍦烘櫙 脳25", "搴旂敤"),
]
cw, gap, ch = 238, 14, 52
cx = 60
for date, name, sub, kind in chips:
    d.rounded_rectangle([cx, 988, cx + cw, 988 + ch], radius=8, fill=(14, 10, 6), outline=(72, 58, 34), width=1)
    d.text((cx + 14, 1006), date, font=f_tiny, fill=GOLD_HI, anchor="lm")
    dw = d.textlength(date, font=f_tiny)
    d.text((cx + 14 + dw + 8, 1006), name, font=f_label, fill=WHITE, anchor="lm")
    d.text((cx + 14, 1026), sub, font=f_tiny, fill=(128, 121, 110), anchor="lm")
    d.text((cx + cw - 12, 1006), kind, font=font("msyh.ttc", 10), fill=(112, 92, 48), anchor="rm")
    cx += cw + gap

# ---------- footnote ----------
d.text((60, 1072), "娉細榛庢浖鐚滄兂鐢?Lean/Mathlib 绀惧尯鐙珛鏍搁獙閫氳繃锛汣lay 浠嶅垪涓烘湭瑙ｏ紝灏氭湭杩涘叆鍚岃璇勫涓庢巿濂栨祦绋嬨€?, font=f_tiny, fill=(112, 106, 98), anchor="lm")
d.text((60, 1090), "鏉ㄢ€撶背灏旀柉浠呫€屽瓨鍦ㄦ€с€嶉儴鍒嗭紝璐ㄩ噺闂撮殭鏈В銆傚皬鏉′负鍙戝竷/鎶ラ亾鍙ｅ緞锛岄潪鐙珛璇勬祴銆傛洸绾块珮搴︿负绀烘剰锛屾í杞翠负闈炵嚎鎬ф椂闂磋酱銆?, font=f_tiny, fill=(112, 106, 98), anchor="lm")

base.save(OUT)
print("saved", OUT, base.size)

