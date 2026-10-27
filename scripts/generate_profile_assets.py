"""Build self-contained SVG artwork for the profile. Standard library only."""
from pathlib import Path
import base64
from html import escape

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
PORTRAIT = 'data:image/png;base64,' + base64.b64encode((ASSETS / 'hasham-doodle-avatar.png').read_bytes()).decode()

def save(name, width, height, title, body, defs='', css=''):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title">
<title id="title">{escape(title)}</title>
<defs>{defs}</defs>
<style>text{{font-family:Inter,Segoe UI,Arial,sans-serif}}.mono{{font-family:ui-monospace,Consolas,monospace}}{css}@media(prefers-reduced-motion:reduce){{.motion,.motion *{{animation:none!important}}}}</style>
{body}
</svg>'''
    (ASSETS / name).write_text('\n'.join(line.rstrip() for line in svg.splitlines()) + '\n', encoding='utf-8')

gradients = '''
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#0a1223"/><stop offset=".6" stop-color="#10152b"/><stop offset="1" stop-color="#191533"/></linearGradient>
<linearGradient id="accent"><stop stop-color="#72f5cc"/><stop offset=".55" stop-color="#83c3ff"/><stop offset="1" stop-color="#c2a1ff"/></linearGradient>
<radialGradient id="glow"><stop stop-color="#8e70ff" stop-opacity=".30"/><stop offset="1" stop-color="#8e70ff" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#afbbef" opacity=".13"/></pattern>
'''
motion = '''.orbit{transform-origin:940px 214px;animation:orbit 30s linear infinite}.twinkle{animation:twinkle 4s ease-in-out infinite}.float{animation:float 6s ease-in-out infinite}@keyframes orbit{to{transform:rotate(360deg)}}@keyframes twinkle{50%{opacity:.3}}@keyframes float{50%{transform:translateY(-7px)}}'''

save('hero.svg', 1180, 430, 'Hasham Javed — Senior full-stack developer. React, Next.js, Node.js, NestJS, AI agents, SQL and cloud.', f'''
<rect width="1180" height="430" rx="28" fill="url(#bg)"/>
<rect width="1180" height="430" rx="28" fill="url(#grid)"/>
<ellipse cx="930" cy="220" rx="370" ry="300" fill="url(#glow)"/>
<path d="M30 429H1150" stroke="url(#accent)" stroke-width="3"/>
<path d="M620 0L742 430M697 0L819 430" stroke="#50528b" opacity=".18"/>
<circle cx="940" cy="214" r="173" fill="none" stroke="#a995ee" stroke-opacity=".2"/>
<g class="motion orbit"><circle cx="940" cy="214" r="194" fill="none" stroke="#91e8e1" stroke-opacity=".22" stroke-dasharray="4 15"/><circle cx="940" cy="20" r="5" fill="#72f5cc"/><circle cx="1108" cy="311" r="4" fill="#b9a4ff"/></g>
<rect x="52" y="36" width="310" height="30" rx="15" fill="#182a32" stroke="#2b5452"/>
<circle cx="69" cy="51" r="4" fill="#72f5cc"/>
<text class="mono" x="83" y="56" font-size="13" letter-spacing="1.1" fill="#a1f8df">SENIOR FULL-STACK DEVELOPER</text>
<text x="50" y="166" font-size="102" font-weight="800" letter-spacing="-5" fill="#f5f7ff">Hasham</text>
<text x="50" y="271" font-size="112" font-weight="800" letter-spacing="-5" fill="url(#accent)">Javed.</text>
<text x="55" y="316" font-size="23" fill="#c7d2ed">Code. Connect. Experiment.</text>
<g class="mono" font-size="14" fill="#b7c6e5">
<text x="55" y="382">REACT / NEXT.JS</text><text x="247" y="382">NODE / NESTJS</text><text x="434" y="382">AI / SQL / CLOUD</text></g>
<path d="M226 368v17M413 368v17" stroke="#485774"/>
<g class="motion float"><g transform="rotate(7 941 214)">
<rect x="805" y="75" width="278" height="306" rx="17" fill="#050914" opacity=".5" transform="translate(8 10)"/>
<rect x="805" y="75" width="278" height="306" rx="17" fill="#fff"/>
<image x="815" y="79" width="258" height="258" xlink:href="{PORTRAIT}"/>
<text class="mono" x="944" y="363" font-size="13" text-anchor="middle" fill="#243c45" letter-spacing="1.5">STAY CURIOUS. BUILD.</text>
<rect x="896" y="64" width="94" height="24" rx="3" fill="#a8e4d5" opacity=".86"/>
</g></g>
<g class="motion twinkle" stroke="#9eeed9" stroke-width="2"><path d="M738 95v18m-9-9h18M1110 359v18m-9-9h18"/></g>
<text class="mono" x="720" y="300" fill="#92a5e6" font-size="28" transform="rotate(-13 720 300)">&lt;/&gt;</text>
''', gradients, motion)

save('hero-mobile.svg', 620, 700, 'Hasham Javed — Senior full-stack developer. Code. Connect. Experiment.', f'''
<rect width="620" height="700" rx="28" fill="url(#bg)"/><rect width="620" height="700" rx="28" fill="url(#grid)"/>
<ellipse cx="310" cy="490" rx="310" ry="265" fill="url(#glow)"/>
<text class="mono" x="310" y="49" text-anchor="middle" font-size="18" letter-spacing="2" fill="#a1f8df">SENIOR FULL-STACK DEVELOPER</text>
<text x="310" y="163" text-anchor="middle" font-size="108" font-weight="800" letter-spacing="-5" fill="#f5f7ff">Hasham</text>
<text x="310" y="269" text-anchor="middle" font-size="116" font-weight="800" letter-spacing="-5" fill="url(#accent)">Javed.</text>
<text x="310" y="315" text-anchor="middle" font-size="24" fill="#c7d2ed">Code. Connect. Experiment.</text>
<circle cx="310" cy="493" r="151" fill="none" stroke="#a995ee" stroke-opacity=".3" stroke-dasharray="5 12"/>
<g transform="rotate(5 310 492)"><rect x="195" y="365" width="230" height="264" rx="14" fill="#fff"/>
<image x="201" y="370" width="218" height="218" xlink:href="{PORTRAIT}"/>
<text class="mono" x="310" y="611" font-size="12" text-anchor="middle" fill="#243c45" letter-spacing="1">STAY CURIOUS. BUILD.</text>
<rect x="270" y="354" width="80" height="22" rx="3" fill="#a8e4d5" opacity=".9"/></g>
<g class="motion twinkle" stroke="#9eeed9" stroke-width="2"><path d="M125 431v22m-11-11h22M492 546v22m-11-11h22"/></g>
<text class="mono" x="310" y="677" text-anchor="middle" font-size="18" letter-spacing="1" fill="#b7c6e5">REACT → APIS → AI → CLOUD</text>
<path d="M28 699H592" stroke="url(#accent)" stroke-width="3"/>
''', gradients, '.twinkle{animation:twinkle 4s ease-in-out infinite}@keyframes twinkle{50%{opacity:.3}}')

save('typing.svg', 560, 58, 'React. Node. TypeScript. From React to cloud. Building with AI agents.', '''
<defs><clipPath id="reveal"><rect class="motion reveal" x="35" y="5" width="490" height="47"/></clipPath></defs>
<g class="mono" font-size="25" font-weight="600" fill="#8fe8d2" text-anchor="middle" clip-path="url(#reveal)">
<text class="motion line first" x="280" y="37">React. Node. TypeScript.</text>
<text class="motion line second" x="280" y="37">From React to cloud.</text>
<text class="motion line third" x="280" y="37">Building with AI agents.</text>
</g>
''', css='''.line{opacity:0}.first{opacity:1;animation:first 15s infinite}.second{animation:second 15s infinite}.third{animation:third 15s infinite}.reveal{animation:type 5s steps(28,end) infinite}@keyframes first{0%,32%{opacity:1}33.33%,99%{opacity:0}100%{opacity:1}}@keyframes second{0%,33.32%{opacity:0}33.33%,65.32%{opacity:1}66.66%,100%{opacity:0}}@keyframes third{0%,66.65%{opacity:0}66.66%,99%{opacity:1}100%{opacity:0}}@keyframes type{0%{width:0}55%,86%{width:490px}99%,100%{width:0}}''')

for name, label, fill, ink in [('repos','Browse repositories','#7ce7ca','#0a1821'),('activity','Watch the snake','#22213e','#d7caff'),('email','Say hello','#19263c','#a9d4ff')]:
    save(f'button-{name}.svg',184,44,label,f'<rect x="1" y="1" width="182" height="42" rx="10" fill="{fill}" stroke="{ink}" stroke-opacity=".18"/><text x="92" y="28" text-anchor="middle" font-size="15" font-weight="600" fill="{ink}">{label} ↗</text>')
print('Generated 6 self-contained SVG assets.')
