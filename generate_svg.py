
import random, html
 
text = "We hunt vulnerabilities before they hunt you."
glyphs = list("!?#|@$%~^*+=-")
 
FRAME_MS = 90
SCRAMBLE_COUNT = 5
total_ms = len(text) * FRAME_MS + SCRAMBLE_COUNT * FRAME_MS + 500
total_s = total_ms / 1000
 
width = 860
height = 50
font_size = 18
char_width = 10.85
start_x = (width - len(text) * char_width) / 2
y = 33
 
elements = []
 
for i, ch in enumerate(text):
    delay_ms = i * FRAME_MS
    display_char = html.escape(ch) if ch != ' ' else '&#160;'
    glyph_char = html.escape(random.choice(glyphs))
    x = start_x + i * char_width
 
    t_show   = round(delay_ms / total_ms, 4)
    t_hide   = round((delay_ms + SCRAMBLE_COUNT * FRAME_MS) / total_ms, 4)
    t_show   = max(0.0001, min(t_show, 0.9998))
    t_hide   = max(t_show + 0.0001, min(t_hide, 0.9999))
 
    eps = 0.0001
 
    # Glyph vert (apparaît à t_show, disparaît à t_hide)
    kt_g  = f"0;{max(0,t_show-eps):.4f};{t_show:.4f};{t_hide:.4f};{min(1,t_hide+eps):.4f};1"
    val_g = "0;0;1;1;0;0"
    elements.append(
        f'<text x="{x:.1f}" y="{y}" font-family="Courier New,monospace" '
        f'font-size="{font_size}" fill="#39ff14" opacity="0">'
        f'<animate attributeName="opacity" values="{val_g}" keyTimes="{kt_g}" '
        f'dur="{total_s:.2f}s" begin="0s" fill="freeze" calcMode="discrete"/>'
        f'{glyph_char}</text>'
    )
 
    # Caractère blanc (apparaît à t_hide, reste)
    kt_f  = f"0;{max(0,t_hide-eps):.4f};{t_hide:.4f};1"
    val_f = "0;0;1;1"
    elements.append(
        f'<text x="{x:.1f}" y="{y}" font-family="Courier New,monospace" '
        f'font-size="{font_size}" fill="#ffffff" opacity="0">'
        f'<animate attributeName="opacity" values="{val_f}" keyTimes="{kt_f}" '
        f'dur="{total_s:.2f}s" begin="0s" fill="freeze" calcMode="discrete"/>'
        f'{display_char}</text>'
    )
 
# Curseur clignotant SMIL
cursor_x = start_x + len(text) * char_width + 3
elements.append(
    f'<text x="{cursor_x:.1f}" y="{y}" font-family="Courier New,monospace" '
    f'font-size="{font_size}" fill="#39ff14">'
    f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.49;0.5;1" '
    f'dur="0.7s" repeatCount="indefinite" calcMode="discrete"/>'
    f'|</text>'
)
 
# Préfixe ">/ ! -"
raw_prefix = ">/ ! - "
for pi, pc in enumerate(raw_prefix):
    px = start_x - (len(raw_prefix) - pi) * char_width
    dur = round(1.4 + pi * 0.15, 2)
    elements.append(
        f'<text x="{px:.1f}" y="{y}" font-family="Courier New,monospace" '
        f'font-size="{font_size}" fill="#39ff14">'
        f'<animate attributeName="opacity" values="1;0.4;1;0.9;1" '
        f'keyTimes="0;0.25;0.5;0.75;1" dur="{dur}s" repeatCount="indefinite"/>'
        f'{html.escape(pc)}</text>'
    )
 
svg = (
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
    f'viewBox="0 0 {width} {height}">\n'
    f'<rect width="{width}" height="{height}" fill="transparent"/>\n'
    + "\n".join(elements)
    + "\n</svg>"
)
 
import os, xml.etree.ElementTree as ET
out = "/mnt/user-data/outputs/assets/typing.svg"
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w", encoding="utf-8") as f:
    f.write(svg)
 
try:
    ET.parse(out)
    print(f"OK — {os.path.getsize(out)/1024:.1f} KB — XML valide ✓")
except ET.ParseError as e:
    print(f"XML invalide: {e}")
