# Image optimization

Images served from `static/` are committed as-is by Hugo. Large images
slow down page loads, especially on mobile. This note records the
workflow used to optimize the screenshot in the automatic link checker
post; the same approach applies to other screenshots and flat-color
images.

## Prerequisites

```bash
sudo apt install -y imagemagick
```

## Why not JPEG for screenshots

JPEG performs poorly on screenshots: flat color regions and crisp text
produce larger files than the original PNG. Lossless WebP is the better
choice for this kind of image — it is typically 70-80% smaller than PNG
with zero quality loss.

## Convert PNG to lossless WebP

```bash
convert static/posts/automatic-link-checker/summary.png \
    -define webp:lossless=true \
    static/posts/automatic-link-checker/summary.webp
```

Then remove the original PNG and update the image reference in the
markdown (`.png` → `.webp`):

```bash
rm static/posts/automatic-link-checker/summary.png
```

## Verify the conversion is lossless

Compare the two images pixel by pixel. A result of `0` means no
difference:

```bash
compare -metric AE static/posts/automatic-link-checker/summary.png \
    static/posts/automatic-link-checker/summary.webp null:
```

Check the size reduction:

```bash
du -h static/posts/automatic-link-checker/summary.webp
```

## Benchmark

The following benchmark was run on the link checker summary screenshot
(original: 2138×4056 PNG, 688K, alpha channel fully opaque). It compares
formats and resizing options using ImageMagick.

The commands used to generate each variant:

```bash
# Check that the alpha channel is actually used (1.0 = fully opaque)
convert summary.png -alpha extract -format "%[fx:mean]" info:

# JPEG (full size)
convert summary.png -quality 85 jpg_q85.jpg
convert summary.png -quality 90 jpg_q90.jpg

# WebP lossy (full size)
convert summary.png -quality 85 webp_q85.webp
convert summary.png -quality 90 webp_q90.webp

# WebP lossless (full size) — the winner
convert summary.png -define webp:lossless=true webp_lossless.webp

# Resized to 1200px wide (PNG lossless)
convert summary.png -resize 1200 png_1200.png

# Resized to 1200px wide (WebP lossy q85)
convert summary.png -resize 1200 -quality 85 webp_1200_q85.webp

# Resized to 800px wide (PNG lossless)
convert summary.png -resize 800 png_800.png
```

Check the file sizes with `du -h`:

```bash
du -h summary.png jpg_q85.jpg webp_q85.webp webp_lossless.webp \
       png_1200.png webp_1200_q85.webp png_800.png
```

| Option | Size | Reduction | Quality |
|---|---|---|---|
| Original PNG (2138×4056) | 688K | — | lossless |
| **WebP lossless, full size** | **148K** | **-78%** | **lossless (0 pixel diff)** |
| WebP q85, full size | 772K | -12% | lossy |
| JPEG q85, full size | 1.3M | +89% (worse) | lossy |
| WebP q85, resized 1200w | 356K | -48% | lossy + downscaled |
| PNG lossless, resized 800w | 600K | -13% | lossless + downscaled |

Takeaways:

* **Lossless WebP is the clear winner** for screenshots: 78% smaller
  than PNG with zero quality loss.
* **JPEG is worse than the original** for screenshots — flat color
  regions and crisp text are exactly what JPEG compresses badly.
* **Lossy WebP is not worth it** for this image type — the lossless
  variant is already smaller than lossy WebP q85, because the image
  compresses well without discarding information.
* **Resizing helps lossy formats** but is unnecessary for lossless WebP,
  which is already small at full resolution.

## Browser support

WebP is supported by all modern browsers (Chrome, Firefox, Safari,
Edge). No fallback is needed for a technical blog in 2026.
