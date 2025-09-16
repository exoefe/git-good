#!/usr/bin/env python3
import os, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
IMAGES = ROOT / "images"
TEMPLATE = (ROOT / "index.template.html").read_text(encoding="utf-8")

cards = []
users = set()

# walk images/<user>/** for common image types
exts = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif", ".svg"}
for user_dir in sorted([p for p in IMAGES.glob("*") if p.is_dir()]):
    user = user_dir.name
    users.add(user)
    for img in sorted(user_dir.rglob("*")):
        if img.suffix.lower() in exts:
            rel = img.relative_to(ROOT).as_posix()
            alt = f"{user}'s image"
            cards.append(f"""
<figure class="card">
  <img src="{html.escape(rel)}" alt="{html.escape(alt)}" loading="lazy" />
  <figcaption>
    <div class="caption">{html.escape(user)}</div>
    <div class="meta">{html.escape(img.name)}</div>
  </figcaption>
</figure>""")

html_out = TEMPLATE.replace("{{CONTRIB_COUNT}}", str(len(users))) \
                   .replace("{{IMAGE_COUNT}}", str(len(cards))) \
                   .replace("{{CARDS}}", "\n".join(cards))

# write index.html at repo root so it renders on GitHub too
(ROOT / "index.html").write_text(html_out, encoding="utf-8")
print(f"Built index.html with {len(cards)} images from {len(users)} contributors.")

