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
        f'      <figure class="group relative mb-4 break-inside-avoid" data-photo="{escape(p.name)}">\n'
        f'        <img src="gallery-photos/{escape(p.name)}" alt="MauriceMark" loading="lazy" class="w-full rounded shadow-sm hover:shadow-md transition">\n'
        f'        <button onclick="removePhoto(this)" title="Remove this photo" class="absolute top-2 right-2 w-7 h-7 flex items-center justify-center rounded-full bg-black/50 text-white text-lg leading-none opacity-0 group-hover:opacity-100 focus:opacity-100 transition">&times;</button>\n'
        f'      </figure>'
        for p in photos
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MauriceMark — Birthday Gallery</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
  <style>
    body {{ font-family: 'Inter', sans-serif; }}
    .serif {{ font-family: 'Cormorant Garamond', serif; }}
    @keyframes float-balloon {{ 0%, 100% {{ transform: translateY(0) rotate(-3deg); }} 50% {{ transform: translateY(-22px) rotate(3deg); }} }}
    .balloon {{ animation: float-balloon 4.5s ease-in-out infinite; }}
    .balloon:nth-child(2) {{ animation-delay: 0.8s; }}
    .balloon:nth-child(3) {{ animation-delay: 1.6s; }}
    .balloon:nth-child(4) {{ animation-delay: 2.4s; }}
    @keyframes banner-wave {{ 0%, 100% {{ transform: rotate(-1deg); }} 50% {{ transform: rotate(1deg); }} }}
    #bdayBanner {{ animation: banner-wave 3s ease-in-out infinite; }}
  </style>
</head>
<body class="bg-stone-50 text-stone-900 antialiased overflow-x-hidden">
  <div class="flex justify-center gap-6 md:gap-10 text-4xl md:text-6xl pt-6 select-none pointer-events-none">
    <span class="balloon">🎈</span>
    <span class="balloon">🎂</span>
    <span class="balloon">🎉</span>
    <span class="balloon">🎈</span>
  </div>

  <header class="text-center pt-6 pb-8 px-6">
    <p id="bdayBanner" class="inline-block text-xs md:text-sm uppercase tracking-[0.3em] bg-stone-900 text-white px-4 py-2 rounded-full mb-5 shadow">🎉 Happy Birthday, MauriceMark! 🎉</p>
    <h1 class="serif text-5xl md:text-7xl font-semibold leading-tight mb-4">For MauriceMark</h1>
    <p class="text-lg md:text-xl text-stone-600 italic serif mb-6">August 2, 2026</p>
    <a href="index.html" class="text-sm text-stone-500 underline hover:text-stone-800">Read the birthday letter</a>
  </header>

  <audio id="bgMusic" loop preload="auto">
    <source src="audio/celebrate-good-times.mp3" type="audio/mpeg">
  </audio>
  <button id="musicToggle" onclick="toggleMusic()" class="fixed bottom-6 right-6 z-50 flex items-center gap-2 bg-stone-900 text-white px-5 py-3 rounded-full shadow-lg hover:bg-stone-700 transition">
    <span id="musicIcon">🎵</span>
    <span id="musicLabel" class="text-sm font-medium">Play Music</span>
  </button>
  <button id="confettiBtn" onclick="burstConfetti()" class="fixed bottom-6 left-6 z-50 flex items-center gap-2 bg-pink-600 text-white px-5 py-3 rounded-full shadow-lg hover:bg-pink-500 transition">
    <span>🎊</span>
    <span class="text-sm font-medium">Celebrate!</span>
  </button>

  <main class="columns-1 sm:columns-2 md:columns-3 lg:columns-4 gap-4 px-4 pb-20 max-w-7xl mx-auto">
{images_html}
  </main>

  <footer class="text-center text-stone-400 text-xs pb-10">
    <p>Music: "Keep it Up - Funky Uplifting" by Davide Bozzaro, via Jamendo/Internet Archive (CC BY-NC-ND 3.0)</p>
  </footer>

  <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"></script>
  <script>
    const bgMusic = document.getElementById('bgMusic');

    function setMusicUI(icon, label) {{
      document.getElementById('musicIcon').textContent = icon;
      document.getElementById('musicLabel').textContent = label;
    }}

    function toggleMusic() {{
      if (bgMusic.paused) {{
        bgMusic.play().catch((err) => console.error('Music playback failed:', err));
      }} else {{
        bgMusic.pause();
      }}
    }}

    let confettiPending = false;
    bgMusic.addEventListener('play', () => {{
      confettiPending = true;
      setMusicUI('⏳', 'Loading…');
    }});
    bgMusic.addEventListener('playing', () => {{
      setMusicUI('🔊', 'Pause Music');
      if (confettiPending) {{
        confettiPending = false;
        burstConfetti();
      }}
    }});
    bgMusic.addEventListener('pause', () => setMusicUI('🎵', 'Play Music'));
    bgMusic.addEventListener('error', () => setMusicUI('🎵', 'Play Music'));

    function burstConfetti() {{
      if (typeof confetti !== 'function') return;
      const colors = ['#f43f5e', '#f59e0b', '#10b981', '#3b82f6', '#a855f7'];
      confetti({{ particleCount: 120, spread: 90, origin: {{ y: 0.3 }}, colors }});
      confetti({{ particleCount: 60, angle: 60, spread: 70, origin: {{ x: 0 }}, colors }});
      confetti({{ particleCount: 60, angle: 120, spread: 70, origin: {{ x: 1 }}, colors }});
    }}

    window.addEventListener('load', () => {{
      setTimeout(burstConfetti, 500);
    }});

    const SUPABASE_URL = 'https://vyxtuojutazzhtvwookc.supabase.co';
    const SUPABASE_KEY = 'sb_publishable_NiRuO9blo_8ir6gzar2h9Q_ybFzCgBU';
    const SB_HEADERS = {{
      'apikey': SUPABASE_KEY,
      'Authorization': 'Bearer ' + SUPABASE_KEY,
      'Content-Type': 'application/json'
    }};

    async function applyHiddenPhotos() {{
      try {{
        const res = await fetch(SUPABASE_URL + '/rest/v1/hidden_photos?select=src', {{ headers: SB_HEADERS }});
        if (!res.ok) throw new Error('HTTP ' + res.status);
        const hidden = new Set((await res.json()).map((row) => row.src));
        if (!hidden.size) return;
        document.querySelectorAll('figure[data-photo]').forEach((fig) => {{
          if (hidden.has(fig.dataset.photo)) fig.remove();
        }});
      }} catch (err) {{
        console.error('Failed to load hidden photo list:', err);
      }}
    }}

    async function removePhoto(btn) {{
      const fig = btn.closest('figure[data-photo]');
      if (!fig) return;
      const password = prompt('Enter the moderation password to remove this photo:');
      if (!password) return;
      try {{
        const res = await fetch(SUPABASE_URL + '/rest/v1/rpc/hide_photo', {{
          method: 'POST',
          headers: SB_HEADERS,
          body: JSON.stringify({{ photo_src: fig.dataset.photo, password }})
        }});
        if (!res.ok) {{
          const detail = await res.text();
          if (detail.includes('INVALID_PASSWORD')) {{
            alert('Incorrect password.');
            return;
          }}
          throw new Error('HTTP ' + res.status + ': ' + detail);
        }}
        fig.remove();
      }} catch (err) {{
        console.error('Failed to remove photo:', err);
        alert('Sorry, the photo could not be removed. Please try again.');
      }}
    }}

    applyHiddenPhotos();
  </script>
</body>
</html>
"""

    gallery_path = Path("gallery.html")
    gallery_path.write_text(html)
    print(f"Wrote {len(photos)} photos to {gallery_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
