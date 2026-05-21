import os
from pathlib import Path

def main():
    base = Path(__file__).resolve().parent.parent / 'static' / 'images' / 'ev-placeholders'
    base.mkdir(parents=True, exist_ok=True)
    colors = [
        '#0a1628', '#003a5b', '#004d7a', '#005f8d', '#0078a0', '#008db3',
        '#009fc5', '#00b6d8', '#00ccee', '#00f5ff', '#053742', '#0a5f7a',
        '#0d718e', '#0f84a1', '#1197b5', '#16a8c7', '#18bac9', '#1bcddf',
        '#1ae3ff', '#136b7f', '#0f5670', '#0d445c', '#0c364b', '#0d2d3c',
        '#0f2330'
    ]

    template = '''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="500" viewBox="0 0 800 500">
  <defs>
    <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{color}" />
      <stop offset="100%" stop-color="#002d44" />
    </linearGradient>
  </defs>
  <rect width="800" height="500" fill="url(#g)" />
  <circle cx="130" cy="110" r="72" fill="rgba(255,255,255,0.1)" />
  <rect x="120" y="210" width="560" height="220" rx="30" fill="rgba(255,255,255,0.08)" />
  <path d="M230 280h340v100a24 24 0 0 1-24 24H254a24 24 0 0 1-24-24V280Z" fill="rgba(255,255,255,0.14)" />
  <path d="M330 225h140a18 18 0 0 1 18 18v120a18 18 0 0 1-18 18H330a18 18 0 0 1-18-18V243a18 18 0 0 1 18-18Z" fill="#fff" opacity="0.95" />
  <path d="M370 250h40v60h-40v44l-26-34h-24l44-58Z" fill="{color}" />
  <text x="400" y="420" text-anchor="middle" font-family="Segoe UI, sans-serif" font-size="42" fill="#fff" letter-spacing="1">EV CHARGING STATION</text>
  <text x="400" y="460" text-anchor="middle" font-family="Segoe UI, sans-serif" font-size="26" fill="#cde8ff">Station image #{index}</text>
</svg>'''

    for i in range(1, 51):
        color = colors[i % len(colors)]
        svg_text = template.format(color=color, index=i)
        out_path = base / f'ev-{i:02}.svg'
        out_path.write_text(svg_text, encoding='utf-8')

    print(f'Generated {len(range(1,51))} placeholder SVG images in {base}')

if __name__ == '__main__':
    main()
