# Favicon setup

The site uses an SVG favicon (`static/style/img/f4inx-black.svg`) declared
in `layouts/partials/head.html`. Browsers and Google also request
`/favicon.ico` at the site root by default; without it, Google Search
Console reports a 404.

The ICO file is generated from the SVG source and committed to
`static/favicon.ico` so Hugo copies it to the site root on build.

## Prerequisites

```bash
sudo apt install -y inkscape imagemagick
```

## Generate the ICO

Render the SVG to PNG at each size, then combine into a multi-resolution ICO:

```bash
inkscape -w 16 -h 16 static/style/img/f4inx-black.svg -o /tmp/f4inx-16.png
inkscape -w 32 -h 32 static/style/img/f4inx-black.svg -o /tmp/f4inx-32.png
inkscape -w 48 -h 48 static/style/img/f4inx-black.svg -o /tmp/f4inx-48.png

magick /tmp/f4inx-16.png /tmp/f4inx-32.png /tmp/f4inx-48.png static/favicon.ico
```

## Verify

Check the ICO contains all three sizes:

```bash
python3 -c "from PIL import Image; img = Image.open('static/favicon.ico'); print(img.info.get('sizes'))"
```

Expected output:

```
{(16, 16), (32, 32), (48, 48)}
```

Verify Hugo copies it to the build output:

```bash
hugo --minify --baseURL "https://f4inx.github.io/" --destination /tmp/hugo-test
ls -la /tmp/hugo-test/favicon.ico
```

Once deployed, check the live URL:

```bash
curl -sI https://f4inx.github.io/favicon.ico | head -5
```

Expected: `HTTP/2 200` with `content-type: image/x-icon`.
