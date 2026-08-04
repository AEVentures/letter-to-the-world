#!/usr/bin/env python3
"""Generate a responsive masonry gallery.html from gallery-photos/*.jpg."""

import re
from html import escape
from pathlib import Path


def natural_key(name: str):
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", name)]


def main() -> int:
    photo_dir = Path("gallery-photos")
    photos = sorted(photo_dir.glob("*.jpg"), key=lambda p: natural_key(p.name))
    if not photos:
        print(f"No .jpg files found in {photo_dir}")
        return 1

    images_html = "\n".join(
        f'      <img src="gallery-photos/{escape(p.name)}" alt="Maurice Mark" loading="lazy" class="w-full mb-4 rounded shadow-sm hover:shadow-md transition break-inside-avoid">'
        for p in photos
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Maurice Mark — Birthday Gallery</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
  <style>
    body {{ font-family: 'Inter', sans-serif; }}
    .serif {{ font-family: 'Cormorant Garamond', serif; }}
  </style>
</head>
<body class="bg-stone-50 text-stone-900 antialiased">
  <header class="text-center pt-16 pb-8 px-6">
    <p class="text-xs uppercase tracking-[0.3em] text-stone-500 mb-5">A Birthday Gallery</p>
    <h1 class="serif text-5xl md:text-7xl font-semibold leading-tight mb-4">For Maurice Mark</h1>
    <p class="text-lg md:text-xl text-stone-600 italic serif mb-6">August 2, 2026</p>
    <a href="index.html" class="text-sm text-stone-500 underline hover:text-stone-800">Read the birthday letter</a>
  </header>
  <main class="columns-1 sm:columns-2 md:columns-3 lg:columns-4 gap-4 px-4 pb-20 max-w-7xl mx-auto">
{images_html}
  </main>
</body>
</html>
"""

    gallery_path = Path("gallery.html")
    gallery_path.write_text(html)
    print(f"Wrote {len(photos)} photos to {gallery_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
