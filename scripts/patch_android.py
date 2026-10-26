"""Run after `npx cap add android`: adds Share-menu support and the VALIRYAN launcher icon."""
import re, os
from PIL import Image

A = 'android/app/src/main'

# 1) Share menu: accept audio, video, images and text/links
mf = f'{A}/AndroidManifest.xml'
s = open(mf, encoding='utf-8').read()
filters = ''
for act in ('SEND', 'SEND_MULTIPLE'):
    for mime in ('audio/*', 'video/*', 'image/*', 'text/*'):
        if act == 'SEND_MULTIPLE' and mime == 'text/*':
            continue
        filters += f'''
            <intent-filter>
                <action android:name="android.intent.action.{act}" />
                <category android:name="android.intent.category.DEFAULT" />
                <data android:mimeType="{mime}" />
            </intent-filter>'''
if 'android.intent.action.SEND' not in s:
    s = s.replace('</activity>', filters + '\n        </activity>', 1)
open(mf, 'w', encoding='utf-8').write(s)

# 2) Launcher icon (adaptive foreground + legacy PNGs)
src = Image.open('icon-512.png').convert('RGBA')
bg = src.getpixel((6, 6))[:3]
hexbg = '#%02x%02x%02x' % bg
res = A + '/res'
for d, legacy, fg in (('mdpi', 48, 108), ('hdpi', 72, 162), ('xhdpi', 96, 216), ('xxhdpi', 144, 324), ('xxxhdpi', 192, 432)):
    p = f'{res}/mipmap-{d}'
    os.makedirs(p, exist_ok=True)
    ic = src.resize((legacy, legacy), Image.LANCZOS)
    ic.save(f'{p}/ic_launcher.png')
    ic.save(f'{p}/ic_launcher_round.png')
    canvas = Image.new('RGBA', (fg, fg), (0, 0, 0, 0))
    k = int(fg * 0.62)
    canvas.paste(src.resize((k, k), Image.LANCZOS), ((fg - k) // 2, (fg - k) // 2))
    canvas.save(f'{p}/ic_launcher_foreground.png')
vd = f'{res}/values'
os.makedirs(vd, exist_ok=True)
open(f'{vd}/ic_launcher_background.xml', 'w').write(
    f'<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">{hexbg}</color>\n</resources>\n')
print('patched; icon background', hexbg)
