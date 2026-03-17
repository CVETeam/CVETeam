import random, html
 
text = "We hunt vulnerabilities before they hunt you."
# Uniquement des glyphs XML-safe
glyphs = list("!<>-_?#|@$%~^*+=")
 
FRAME_MS = 90
SCRAMBLE_COUNT = 5
total_duration = len(text) * FRAME_MS + SCRAMBLE_COUNT * FRAME_MS + 500
 
width = 860
height = 50
font_size = 18
char_width = 10.85
start_x = (width - len(text) * char_width) / 2
y = 33
 
css_rules = []
char_elements = []
 
for i, ch in enumerate(text):
    delay_ms = i * FRAME_MS
    # Escape le caractère pour XML
    display_char = html.escape(ch) if ch != ' ' else '&#160;'
    glyph_char = html.escape(random.choice(glyphs))
 
    pct_start = round(delay_ms / total_duration * 100, 2)
    pct_end   = round((delay_ms + SCRAMBLE_COUNT * FRAME_MS) / total_duration * 100, 2)
    pct_final = pct_end
    total_s   = total_duration / 1000
    eps = 0.01
 
    css_rules.append(
        f"@keyframes g{i}{{" 
        f"0%,{max(0,pct_start-eps):.2f}%{{opacity:0}}"
        f"{pct_start:.2f}%{{opacity:1}}"
        f"{pct_end:.2f}%,100%{{opacity:0}}}}"
        f"#g{i}{{animation:g{i} {total_s:.2f}s steps(1) forwards;opacity:0}}"
    )
    css_rules.append(
        f"@keyframes f{i}{{" 
        f"0%,{max(0,pct_final-eps):.2f}%{{opacity:0}}"
        f"{pct_final:.2f}%,100%{{opacity:1}}}}"
        f"#f{i}{{animation:f{i} {total_s:.2f}s steps(1) forwards;opacity:0}}"
    )
 
    x = start_x + i * char_width
    char_elements.append(f'<text id="g{i}" x="{x:.1f}" y="{y}" fill="#39ff14">{glyph_char}</text>')
    char_elements.append(f'<text id="f{i}" x="{x:.1f}" y="{y}" fill="#ffffff">{display_char}</text>')
 
# Curseur
cursor_x = start_x + len(text) * char_width + 3
css_rules.append("#cur{animation:blink 0.7s step-end infinite}@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}")
cursor_el = f'<text id="cur" x="{cursor_x:.1f}" y="{y}" fill="#39ff14">|</text>'
 
# Préfixe
prefix = "&gt;/ ! - "
prefix_els = []
raw_prefix = ">/ ! - "
for pi, pc in enumerate(raw_prefix):
    px = start_x - (len(raw_prefix) - pi) * char_width
    css_rules.append(
        f"@keyframes pf{pi}{{0%,100%{{opacity:1}}{30+pi*7}%{{opacity:0.4}}}}"
        f"#pf{pi}{{animation:pf{pi} {1.4+pi*0.15:.2f}s ease-in-out infinite}}"
    )
    prefix_els.append(f'<text id="pf{pi}" x="{px:.1f}" y="{y}" fill="#39ff14">{html.escape(pc)}</text>')
 
css_block = (
    "<style>"
    "text{font-family:&apos;Courier New&apos;,monospace;font-size:18px}"
    + "".join(css_rules)
    + "</style>"
)
 
parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
    css_block,
    f'<rect width="{width}" height="{height}" fill="transparent"/>',
    "".join(prefix_els),
    "".join(char_elements),
    cursor_el,
    "</svg>"
]
 
svg = "\n".join(parts)
 
import os
os.makedirs("/mnt/user-data/outputs/assets", exist_ok=True)
with open("/mnt/user-data/outputs/assets/typing.svg", "w", encoding="utf-8") as f:
    f.write(svg)
 
size = os.path.getsize("/mnt/user-data/outputs/assets/typing.svg")
print(f"OK — {size/1024:.1f} KB")
 
# Validate XML
import xml.etree.ElementTree as ET
try:
    ET.parse("/mnt/user-data/outputs/assets/typing.svg")
    print("XML valide ✓")
except ET.ParseError as e:
    print(f"XML invalide: {e}")
