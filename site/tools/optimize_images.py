"""把 活动照/ 里的原图压缩成网站用的 WebP（去掉 EXIF/GPS），输出到 public/img/。

用法：python tools/optimize_images.py
HEIC 需要先用 ffmpeg 转成 JPG（脚本会自动调用 ffmpeg）。
新增照片：在 PHOTOS 里加一行 "网站文件名": "原图文件名"。
"""
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT.parent / "活动照"
OUT = ROOT / "public" / "img"

# 网站文件名 -> 原图
PHOTOS = {
    "hero": "IMG_5973.HEIC",            # SESI 现场，孩子戴气球皇冠
    "romeo": "IMG_4811.HEIC",           # 品牌快闪站台全身照（关于区主形象）
    "svc-kids": "IMG_5966.HEIC",        # SESI 现场制作
    "svc-giant": "6bc5695ba87cd7f104ceab60daae70.jpg",  # 发光大型造型
    "svc-decor": "15580542ba839832652ef10222a2ab.jpg",  # 装饰场景 + 气球伞
    "svc-business": "0df2e546df4f6384d641e7565aad02.jpg",  # 商场夜间活动人群
    "svc-seasonal": "7432.jpg",         # 圣诞老人合影
    "g-sesi": "275.jpg",
    "g-lobby": "3ce76c77ea66fe35e4c0a3f9634ef6.jpg",
    "g-party": "3da4c4a013850dae2d2d335bc61d93.jpg",
    "g-crown": "881c622d489c8ee7458285ccb498fb.jpg",
    "g-mascot": "af49d1bed752417f6ab5c40c460c16.jpg",
    "g-tigers": "bc1b5c17e3c96ab3193eff73df6e49.jpg",
    "g-show": "c33e3907c03c80ce0c79626f4cf167.jpg",
    "g-pose": "3043cb78d123137e348d5e862fde32.jpg",
}
WIDTHS = (800, 1600)
QUALITY = 78


def load(path: Path) -> Image.Image:
    if path.suffix.lower() == ".heic":
        tmp = Path(tempfile.gettempdir()) / (path.stem + ".jpg")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(path), "-frames:v", "1", "-q:v", "2", str(tmp)], check=True)
        path = tmp
    return ImageOps.exif_transpose(Image.open(path)).convert("RGB")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, src in PHOTOS.items():
        im = load(SRC / src)
        for w in WIDTHS:
            copy = im.copy()
            copy.thumbnail((w, w * 2))  # 按宽度缩放
            copy.save(OUT / f"{name}-{w}.webp", "WEBP", quality=QUALITY, method=6)
        print(f"{name}: {im.size}")

    # 社交分享卡片 1200x630（WhatsApp / Instagram 转发链接时的预览图）
    og = ImageOps.fit(load(SRC / PHOTOS["hero"]), (1200, 630), centering=(0.5, 0.35))
    og.save(ROOT / "public" / "og-image.jpg", "JPEG", quality=82, optimize=True, progressive=True)


if __name__ == "__main__":
    sys.exit(main())
