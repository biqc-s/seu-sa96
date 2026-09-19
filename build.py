#!/usr/bin/env python3
"""يدمج الملفات المنفصلة في ملف index.html واحد مكتفٍ ذاتيًا داخل dist/.
الاستخدام:  python3 build.py
"""
import base64, pathlib, re

root = pathlib.Path(__file__).parent
dist = root / "dist"; dist.mkdir(exist_ok=True)

def data_uri(rel):
    b = (root / rel).read_bytes()
    return "data:image/png;base64," + base64.b64encode(b).decode()

html  = (root / "index.html").read_text(encoding="utf-8")
css   = (root / "src/styles.css").read_text(encoding="utf-8")
data  = (root / "src/data.js").read_text(encoding="utf-8")
game  = (root / "src/game.js").read_text(encoding="utf-8")

icon, word, full = (data_uri(f"assets/logo-{n}.png") for n in ("icon", "word", "full"))

html = html.replace('<link rel="stylesheet" href="src/styles.css">',
                    "<style>\n" + css + "\n</style>")
html = html.replace('<script>const LOGO_SRC="assets/logo-full.png";</script>\n'
                    '<script src="src/data.js"></script>\n'
                    '<script src="src/game.js"></script>',
                    '<script>\nconst LOGO_SRC="' + full + '";\n'
                    + data + "\n" + game + "\n</script>")
html = html.replace("assets/logo-icon.png", icon).replace("assets/logo-word.png", word)

out = dist / "index.html"
out.write_text(html, encoding="utf-8")
assert "assets/" not in html and "src/" not in html, "بقيت مراجع خارجية"
print(f"تم البناء: {out}  ({out.stat().st_size/1024:.0f} كيلوبايت)")
