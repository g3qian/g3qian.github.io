"""Extract the two selected equipment photos; no manual pages or student data are copied.

Requires Pillow and pypdf. The explanatory SVGs are maintained directly.
"""
from pathlib import Path
from io import BytesIO
import json
from pypdf import PdfReader
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent/'supporting-material/SE 168-268/Lab5.1 (test lab)/Data Collection/SE 168-268 Data Acquisition System Guide.pdf'
OUT = ROOT/'images/vibration-testing-model-correlation/excitation-hardware.webp'
reader = PdfReader(SOURCE)
photos = []
for page in [9, 11]:
    im = Image.open(BytesIO(reader.pages[page-1].images[0].data)).convert('RGB')
    im.thumbnail((720, 620), Image.Resampling.LANCZOS)
    photos.append(im)
canvas = Image.new('RGB', (1600, 800), 'white')
draw = ImageDraw.Draw(canvas)
font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 34)
for i, (im, label) in enumerate(zip(photos, ['Instrumented impact hammer', 'Electrodynamic shaker'])):
    x = i*800
    draw.text((x+50, 40), label, font=font, fill='#1F5C7A')
    canvas.paste(im, (x+(800-im.width)//2, 125+(620-im.height)//2))
canvas.save(OUT, 'WEBP', quality=88, method=6)
manifest = ROOT/'data/media-sources.json'
rows = json.loads(manifest.read_text())
for row in rows:
    if row['file'] == str(OUT.relative_to(ROOT)):
        row.update(width=1600, height=800, bytes=OUT.stat().st_size)
manifest.write_text(json.dumps(rows, indent=2)+'\n')
print(OUT)
