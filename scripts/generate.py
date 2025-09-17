#!/usr/bin/env python3
import os, html, pathlib, json

ROOT = pathlib.Path(__file__).resolve().parents[1]
IMAGES = ROOT / "images"
TPL_INDEX = (ROOT / "index.template.html").read_text(encoding="utf-8")
TPL_PICK = (ROOT / "picker.template.html").read_text(encoding="utf-8")

def list_entries():
    """Return:
       - cards: list of dicts for ALL images
       - reps: list of dicts with one representative image per user
    """
    exts = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif", ".svg"}
    cards = []
    reps_map = {}  # user -> entry
    users = set()

    if not IMAGES.exists():
        return [], []

    for user_dir in sorted([p for p in IMAGES.glob("*") if p.is_dir()]):
        user = user_dir.name
        users.add(user)
        for img in sorted(user_dir.rglob("*")):
            if img.suffix.lower() in exts:
                rel = img.relative_to(ROOT).as_posix()
                entry = {
                    "user": user,
                    "src": rel,
                    "file": img.name
                }
                cards.append(entry)
                reps_map.setdefault(user, entry)  # first image becomes rep

    reps = [reps_map[u] for u in sorted(reps_map.keys())]
    return cards, reps

def build_index(cards):
    users = sorted({c["user"] for c in cards})
    card_html = []
    for c in cards:
        alt = f"{c['user']}'s image"
        card_html.append(f"""
<figure class="card">
  <img src="{html.escape(c['src'])}" alt="{html.escape(alt)}" loading="lazy" />
  <figcaption>
    <div class="caption">{html.escape(c['user'])}</div>
    <div class="meta">{html.escape(c['file'])}</div>
  </figcaption>
</figure>""")
    out = TPL_INDEX.replace("{{CONTRIB_COUNT}}", str(len(users))) \
                   .replace("{{IMAGE_COUNT}}", str(len(cards))) \
                   .replace("{{CARDS}}", "\n".join(card_html))
    (ROOT / "index.html").write_text(out, encoding="utf-8")

def build_picker(reps):
    entries_json = json.dumps(reps, ensure_ascii=False, indent=0)
    out = TPL_PICK.replace("{{ENTRIES_JSON}}", entries_json)
    (ROOT / "picker.html").write_text(out, encoding="utf-8")

def main():
    cards, reps = list_entries()
    build_index(cards)
    build_picker(reps)
    print(f"Built index.html ({len(cards)} images) and picker.html ({len(reps)} entrants).")

if __name__ == "__main__":
    main()

