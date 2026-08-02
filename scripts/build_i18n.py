#!/usr/bin/env python3
"""Build language-specific /en and /pt pages from the bilingual index.html source."""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

try:
    from bs4 import BeautifulSoup, Comment
except ImportError:
    sys.stderr.write("Install BeautifulSoup: python3 -m venv .venv && .venv/bin/pip install beautifulsoup4\n")
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "index.html"
DOMAIN = "https://gustavolevandowski.com"

PT_META = {
    "title": "Gustavo Levandowski · Engenheiro Android · 1M+ Dispositivos · Mentoria",
    "description": "Android Enterprise Expert certificado pelo Google. MDM, WebRTC, AOSP e sistemas em plataformas que protegem mais de 1 milhão de dispositivos. Referência técnica em Android em escala e carreira em programação. Fundador da mentoria LeCode.",
    "og_title": "Gustavo Levandowski · Engenheiro Android · 1M+ Dispositivos · Mentoria",
    "og_description": "Android Enterprise Expert certificado pelo Google. MDM, WebRTC, AOSP e sistemas em plataformas que protegem mais de 1 milhão de dispositivos. Referência técnica em Android em escala e carreira em programação.",
    "og_image_alt": "Gustavo Levandowski · Engenheiro Android · sistemas em plataformas que protegem 1M+ dispositivos · mentoria",
}


def unwrap_lang(soup: BeautifulSoup, keep: str, drop: str) -> None:
    for el in list(soup.select(f".{drop}")):
        el.decompose()
    for el in list(soup.select(f".{keep}")):
        el.unwrap()


def set_lang_toggle(soup: BeautifulSoup, lang: str) -> None:
    toggle = soup.select_one(".lang-toggle")
    if not toggle:
        return
    toggle.clear()
    en = soup.new_tag("a", href="/en/", hreflang="en")
    en["lang"] = "en"
    en.string = "EN"
    pt = soup.new_tag("a", href="/pt/", hreflang="pt-BR")
    pt["lang"] = "pt-BR"
    pt.string = "PT"
    if lang == "en":
        en["class"] = ["active"]
        en["aria-current"] = "page"
    else:
        pt["class"] = ["active"]
        pt["aria-current"] = "page"
    toggle.append(en)
    toggle.append(pt)


def rebuild_faq_jsonld(soup: BeautifulSoup) -> None:
    items = []
    for details in soup.select("details.faq-item"):
        summary = details.find("summary")
        answer = details.select_one(".faq-a")
        if not summary or not answer:
            continue
        # clone summary text without the + marker
        q = " ".join(summary.stripped_strings)
        q = re.sub(r"\s*\+\s*$", "", q).strip()
        a = " ".join(answer.stripped_strings)
        if q and a:
            items.append(
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a},
                }
            )
    if not items:
        return
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            data = json.loads(script.string or "")
        except Exception:
            continue
        if data.get("@type") == "FAQPage":
            data["mainEntity"] = items
            script.string = json.dumps(data, ensure_ascii=False, indent=2)
            break


def patch_head(soup: BeautifulSoup, lang: str) -> None:
    html = soup.find("html")
    path = "/en/" if lang == "en" else "/pt/"
    url = f"{DOMAIN}{path}"

    if lang == "pt":
        html["lang"] = "pt-BR"
        if soup.body:
            classes = soup.body.get("class", [])
            if "pt" not in classes:
                soup.body["class"] = list(classes) + ["pt"]
        title = soup.find("title")
        if title:
            title.string = PT_META["title"]
        for name, key in (
            ("description", "description"),
        ):
            tag = soup.find("meta", attrs={"name": name})
            if tag:
                tag["content"] = PT_META[key]
        for prop, key in (
            ("og:title", "og_title"),
            ("og:description", "og_description"),
            ("og:image:alt", "og_image_alt"),
            ("twitter:title", "og_title"),
            ("twitter:description", "og_description"),
            ("twitter:image:alt", "og_image_alt"),
        ):
            tag = soup.find("meta", attrs={"property": prop}) or soup.find("meta", attrs={"name": prop})
            if tag:
                tag["content"] = PT_META[key]
        og_locale = soup.find("meta", attrs={"property": "og:locale"})
        if og_locale:
            og_locale["content"] = "pt_BR"
        alt = soup.find("meta", attrs={"property": "og:locale:alternate"})
        if alt:
            alt["content"] = "en_US"
    else:
        html["lang"] = "en"
        if soup.body and soup.body.has_attr("class"):
            soup.body["class"] = [c for c in soup.body.get("class", []) if c != "pt"]

    # canonical + hreflang + og:url
    for link in soup.find_all("link", attrs={"rel": "canonical"}):
        link["href"] = url
    for link in soup.find_all("link", attrs={"rel": "alternate"}):
        hl = link.get("hreflang")
        if hl == "x-default" or hl == "en":
            link["href"] = f"{DOMAIN}/en/"
        elif hl == "pt-BR":
            link["href"] = f"{DOMAIN}/pt/"
    og_url = soup.find("meta", attrs={"property": "og:url"})
    if og_url:
        og_url["content"] = url

    # JSON-LD url fields for page entities
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            data = json.loads(script.string or "")
        except Exception:
            continue
        changed = False
        if data.get("@type") in {"WebSite", "ProfilePage"}:
            if "url" in data:
                data["url"] = url
                changed = True
            if data.get("@type") == "WebSite" and lang == "pt":
                data["inLanguage"] = ["pt-BR", "en"]
                changed = True
        if changed:
            script.string = json.dumps(data, ensure_ascii=False, indent=2)


def strip_source_comments(soup: BeautifulSoup) -> None:
    for c in soup.find_all(string=lambda t: isinstance(t, Comment)):
        if "Language URLs" in c or "PRODUCTION NOTE" in c:
            c.extract()


def build_variant(lang: str) -> Path:
    soup = BeautifulSoup(SOURCE.read_text(encoding="utf-8"), "html.parser")
    keep = "lang-en-el" if lang == "en" else "lang-pt-el"
    drop = "lang-pt-el" if lang == "en" else "lang-en-el"
    unwrap_lang(soup, keep, drop)
    # Remove now-unused bilingual CSS helpers? keep for safety.
    set_lang_toggle(soup, lang)
    patch_head(soup, lang)
    rebuild_faq_jsonld(soup)
    strip_source_comments(soup)

    out_dir = ROOT / lang
    out_dir.mkdir(exist_ok=True)
    out = out_dir / "index.html"
    # BeautifulSoup may alter formatting; fine for deploy.
    html = str(soup)
    # Ensure doctype
    if not html.lstrip().lower().startswith("<!doctype"):
        html = "<!DOCTYPE html>\n" + html
    out.write_text(html, encoding="utf-8")
    return out


def write_sitemap() -> None:
    today = date.today().isoformat()
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>{DOMAIN}/en/</loc>
    <xhtml:link rel="alternate" hreflang="en" href="{DOMAIN}/en/"/>
    <xhtml:link rel="alternate" hreflang="pt-BR" href="{DOMAIN}/pt/"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{DOMAIN}/en/"/>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>{DOMAIN}/pt/</loc>
    <xhtml:link rel="alternate" hreflang="en" href="{DOMAIN}/en/"/>
    <xhtml:link rel="alternate" hreflang="pt-BR" href="{DOMAIN}/pt/"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{DOMAIN}/en/"/>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
"""
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")


def main() -> None:
    if not SOURCE.exists():
        sys.exit(f"Missing source: {SOURCE}")
    en = build_variant("en")
    pt = build_variant("pt")
    write_sitemap()
    print(f"Wrote {en.relative_to(ROOT)} ({en.stat().st_size:,} bytes)")
    print(f"Wrote {pt.relative_to(ROOT)} ({pt.stat().st_size:,} bytes)")
    print("Updated sitemap.xml")


if __name__ == "__main__":
    main()
