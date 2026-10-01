#!/usr/bin/env python3
"""Merge the source pages in src/ into one tabbed page (index.html)."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
PANES = ["builder", "plan", "guide", "tracker"]
ROOT_RE = re.compile(r'^(:root(?::not\(\[data-theme="light"\]\)|\[data-theme="dark"\])?)\s*(.*)$', re.S)


def scope_selector(sel, scope):
    sel = sel.strip()
    m = ROOT_RE.match(sel)
    if m:
        head, rest = m.group(1), m.group(2).strip()
        if head == ":root":
            return f"{scope} {rest}".strip()
        return f"{head} {scope} {rest}".strip()
    if sel in ("body", "html"):
        return scope
    return f"{scope} {sel}"


def scope_css(css, scope):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out, i = [], 0
    while True:
        j = css.find("{", i)
        if j == -1:
            break
        prelude = css[i:j].strip()
        depth, k = 1, j + 1
        while depth:
            if css[k] == "{":
                depth += 1
            elif css[k] == "}":
                depth -= 1
            k += 1
        body = css[j + 1:k - 1]
        if prelude.startswith(("@media", "@supports")):
            out.append(f"{prelude}{{\n{scope_css(body, scope)}\n}}")
        elif prelude.startswith("@"):
            out.append(f"{prelude}{{{body}}}")
        else:
            sels = ", ".join(scope_selector(s, scope) for s in prelude.split(","))
            out.append(f"{sels}{{{body.strip()}}}")
        i = k
    return "\n".join(out)


def drop_hero(markup):
    a = markup.find('<div class="hero">')
    if a == -1:
        return markup
    b = markup.find('\n<div class="wrap">', a)
    return markup[:a] + markup[b + 1:]


def split_page(name):
    text = (SRC / f"{name}.html").read_text()
    css = text[text.index("<style>") + 7:text.index("</style>")]
    rest = text[text.index("</style>") + 8:]
    symbols = re.findall(r"<symbol id=\"[^\"]+\".*?</symbol>", rest, flags=re.S)
    rest = re.sub(r"<svg style=\"display:none\".*?</svg>", "", rest, count=1, flags=re.S)
    cut = rest.find("<script")
    markup, scripts = (rest, "") if cut == -1 else (rest[:cut], rest[cut:])
    return css, symbols, markup.strip(), scripts.strip()


def retab(markup, scripts, name, fn):
    markup = markup.replace('onclick="showTab(', f'onclick="{fn}(')
    scripts = scripts.replace("window.showTab", f"window.{fn}")
    for cls in (".tab-btn", ".tabpanel"):
        scripts = scripts.replace(f'querySelectorAll("{cls}")', f'querySelectorAll("#p-{name} {cls}")')
    return markup, scripts


def main():
    shell = (SRC / "shell.html").read_text()
    pane_css, pane_scripts, sprite, seen = [], [], [], set()
    for name in PANES:
        css, symbols, markup, scripts = split_page(name)
        if name in ("guide", "tracker"):
            markup = drop_hero(markup)
            markup, scripts = retab(markup, scripts, name, f"{name}Tab")
        if name == "plan":
            markup = re.sub(r'<a href="https://claude\.ai/artifact/[^"]+" target="_blank" rel="noopener"',
                            '<a href="#builder" onclick="goTab(\'builder\');return false;"', markup)
        pane_css.append(f"/* {name} */\n" + scope_css(css, f"#p-{name}"))
        pane_scripts.append(scripts)
        for sym in symbols:
            sid = re.match(r'<symbol id="([^"]+)"', sym).group(1)
            if sid not in seen:
                seen.add(sid)
                sprite.append(sym)
        shell = shell.replace(f"<!--PANE:{name}-->", markup)

    credits = json.loads((ROOT / "img" / "credits.json").read_text())
    items = []
    for c in credits.values():
        title = html.escape(c["title"].replace("File:", "").rsplit(".", 1)[0])
        artist = html.escape(c["artist"] or "작가 미상")
        items.append(f'        <li><a href="{html.escape(c["page"])}" target="_blank" rel="noopener">{title}</a> · {artist} · {html.escape(c["license"])}</li>')

    shell = shell.replace("<!--PANE_CSS-->", "\n".join(pane_css))
    shell = shell.replace("<!--SPRITE-->", '<svg style="display:none" aria-hidden="true">\n' + "\n".join(sprite) + "\n</svg>")
    shell = shell.replace("<!--CREDITS-->", "\n".join(items))
    shell = shell.replace("<!--PANE_SCRIPTS-->", "\n".join(pane_scripts))
    (ROOT / "index.html").write_text(shell)
    print(f"index.html: {len(shell) / 1024:.0f} KB, {len(sprite)} icons, {len(items)} photo credits")


if __name__ == "__main__":
    main()
