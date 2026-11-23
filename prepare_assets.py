#!/usr/bin/env python3
"""Prepare optimized WebP screenshots, icons, OG social banner, and sample Korean MP3s for KoreanGo-Website."""
from __future__ import annotations

import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SITE_DIR = Path("/Users/kevin/.gemini/antigravity/scratch/KoreanGo-Website")
PUB_IMG = SITE_DIR / "public/images"
PUB_AUD = SITE_DIR / "public/audio"

SHOTS_ROOT = Path("/Users/kevin/.gemini/antigravity/scratch/KoreanGo_AppStore_Release/Screenshots")
ICON_SRC = Path("/Users/kevin/.gemini/antigravity/scratch/KoreanGo_AppStore_Release/AppIcon/KoreanGo_AppIcon_1024x1024.png")
AUDIO_SRC = Path("/Users/kevin/.gemini/antigravity/scratch/KoreanGo.swiftpm/Resources/Audio")

LANG_MAP = {
    "en": "en-US",
    "zh-Hant": "zh-Hant",
    "zh-Hans": "zh-Hans",
    "ja": "ja",
}

SCENES = [
    ("01_LearnPath.png", "s01"),
    ("02_VoiceTutor.png", "s02"),
    ("03_Interpreter.png", "s03"),
    ("04_VideoScenarios.png", "s04"),
    ("05_HangulPairs.png", "s05"),
]

AUDIO_SAMPLES = [
    ("vocab_ex_v_079.mp3", "split.mp3"),
    ("vocab_ex_v_087.mp3", "transfer.mp3"),
    ("vocab_ex_v_120.mp3", "checkout.mp3"),
    ("vocab_ex_v_024.mp3", "slowly.mp3"),
]


def round_icon(im: Image.Image, radius_ratio: float = 0.22) -> Image.Image:
    w, h = im.size
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w, h), radius=int(w * radius_ratio), fill=255)
    out = im.convert("RGBA")
    out.putalpha(mask)
    return out


def build_og_image(icon_img: Image.Image) -> None:
    w, h = 1200, 630
    bg = Image.new("RGB", (w, h), (9, 11, 22))
    px = bg.load()
    for y in range(h):
        ty = y / (h - 1)
        for x in range(w):
            tx = x / (w - 1)
            r = int(12 + 30 * (1 - tx) * 0.6 + 18 * ty)
            g = int(20 + 30 * ty + 42 * tx * 0.5)
            b = int(42 + 64 * (1 - ty * 0.5) + 32 * tx * 0.3)
            px[x, y] = (min(255, r), min(255, g), min(255, b))

    canvas = bg.convert("RGBA")
    ic = round_icon(icon_img.resize((220, 220), Image.Resampling.LANCZOS), 0.22)
    canvas.paste(ic, (96, (h - 220) // 2), ic)

    draw = ImageDraw.Draw(canvas)
    f_title = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 78, index=1)
    f_sub = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 34, index=0)
    f_pill = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 24, index=1)

    tx_x = 368
    draw.text((tx_x, 178), "KoreanGo", font=f_title, fill=(255, 255, 255, 255))
    draw.text((tx_x, 276), "100 Seoul Travel Video Dialogues", font=f_sub, fill=(180, 224, 245, 245))
    draw.text((tx_x, 324), "Guided Voice Practice & Live Translation", font=f_sub, fill=(203, 213, 225, 235))
    draw.text((tx_x, 404), "iPhone  ·  iPad 13\"  |  AE Interactive", font=f_pill, fill=(94, 234, 212, 245))

    canvas.convert("RGB").save(PUB_IMG / "og.png", format="PNG", optimize=True)


def main() -> None:
    PUB_IMG.mkdir(parents=True, exist_ok=True)
    PUB_AUD.mkdir(parents=True, exist_ok=True)

    icon = Image.open(ICON_SRC).convert("RGB")
    round_icon(icon.resize((256, 256), Image.Resampling.LANCZOS)).save(PUB_IMG / "icon.webp", format="WEBP", quality=88)
    round_icon(icon.resize((512, 512), Image.Resampling.LANCZOS)).save(PUB_IMG / "icon.png", format="PNG", optimize=True)
    build_og_image(icon)

    for site_lang, rel_folder in LANG_MAP.items():
        for src_name, short in SCENES:
            src = SHOTS_ROOT / rel_folder / "iPhone_6.9" / src_name
            im = Image.open(src).convert("RGB")
            im_s = im.resize((640, 1390), Image.Resampling.LANCZOS)
            im_s.save(PUB_IMG / f"{site_lang}_{short}.webp", format="WEBP", quality=84)

        ipad_src = SHOTS_ROOT / rel_folder / "iPad_13" / "01_LearnPath.png"
        ipad_im = Image.open(ipad_src).convert("RGB").resize((760, 1013), Image.Resampling.LANCZOS)
        ipad_im.save(PUB_IMG / f"{site_lang}_ipad.webp", format="WEBP", quality=84)

    for src_name, dst_name in AUDIO_SAMPLES:
        shutil.copy2(AUDIO_SRC / src_name, PUB_AUD / dst_name)

    total_img = sum(p.stat().st_size for p in PUB_IMG.glob("*"))
    total_aud = sum(p.stat().st_size for p in PUB_AUD.glob("*"))
    print(
        f"ASSETS_READY: images={len(list(PUB_IMG.glob('*')))} ({total_img / 1024:.1f} KB), "
        f"audio={len(list(PUB_AUD.glob('*')))} ({total_aud / 1024:.1f} KB)"
    )


if __name__ == "__main__":
    main()
