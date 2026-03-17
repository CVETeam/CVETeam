import random
 
text = "We hunt vulnerabilities before they hunt you."
glyphs = list("!<>-_\\/[]{}=+*^?#|@$%&~")
 
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
    display_char = ch if ch != ' ' else '\u00a0'
    glyph_char = random.choice(glyphs)
 
    pct_start = round(delay_ms / total_duration * 100, 2)
    pct_end   = round((delay_ms + SCRAMBLE_COUNT * FRAME_MS) / total_duration * 100, 2)
    pct_final = pct_end
    total_s   = total_duration / 1000
 
    css_rules.append(f"@keyframes g{i}{{0%,{max(0,pct_start-0.01):.2f}%{{opacity:0}}{pct_start:.2f}%{{opacity:1}}{pct_end:.2f}%,100%{{opacity:0}}}}#g{i}{{animation:g{i} {total_s:.2f}s steps(1) forwards;opacity:0}}")
    css_rules.append(f"@keyframes f{i}{{0%,{max(0,pct_final-0.01):.2f}%{{opacity:0}}{pct_final:.2f}%,100%{{opacity:1}}}}#f{i}{{animation:f{i} {total_s:.2f}s steps(1) forwards;opacity:0}}")
 
    x = start_x + i * char_width
    char_elements.append(f'<text id="g{i}" x="{x:.1f}" y="{y}" fill="#39ff14">{glyph_char}</text>')
    char_elements.append(f'<text id="f{i}" x="{x:.1f}" y="{y}" fill="#ffffff">{display_char}</text>')
 
# Curseur
cursor_x = start_x + len(text) * char_width + 3
css_rules.append("#cur{animation:blink 0.7s step-end infinite}@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}")
cursor_el = f'<text id="cur" x="{cursor_x:.1f}" y="{y}" fill="#39ff14">|</text>'
 
# Préfixe
prefix = ">/ ! - "
prefix_els = []
for pi, pc in enumerate(prefix):
    px = start_x - (len(prefix) - pi) * char_width
    css_rules.append(f"@keyframes pf{pi}{{0%,100%{{opacity:1}}{30+pi*7}%{{opacity:0.4}}}}#pf{pi}{{animation:pf{pi} {1.4+pi*0.15:.2f}s ease-in-out infinite}}")
    prefix_els.append(f'<text id="pf{pi}" x="{px:.1f}" y="{y}" fill="#39ff14">{pc}</text>')
 
css_block = "<style>text{font-family:'Courier New',monospace;font-size:18px}" + "".join(css_rules) + "</style>"
 
svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">{css_block}<rect width="{width}" height="{height}" fill="transparent"/>{"".join(prefix_els)}{"".join(char_elements)}{cursor_el}</svg>'
 
import os
with open("assets/typing.svg","w",encoding="utf-8") as f:
    f.write(svg)
print(f"OK — {os.path.getsize('assets/typing.svg')/1024:.1f} KB")
