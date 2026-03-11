#!/usr/bin/env python3
"""
Build script for page-mart.
Inlines minified libs (React, ReactDOM, Babel) into a single self-contained page-mart.html.
Usage: python3 build.py
"""
import re, os

base = os.path.dirname(os.path.abspath(__file__))

with open(f'{base}/index.html') as f: html = f.read()
with open(f'{base}/lib/react.production.min.js') as f: react = f.read().strip()
with open(f'{base}/lib/react-dom.production.min.js') as f: reactdom = f.read().strip()
with open(f'{base}/lib/babel.min.js') as f: babel = f.read().strip()

# Inline libs using lambdas (avoids backslash interpretation in replacement strings)
html = re.sub(r'<script src="lib/react\.development\.js"></script>', lambda m: f'<script>{react}</script>', html)
html = re.sub(r'<script src="lib/react-dom\.development\.js"></script>', lambda m: f'<script>{reactdom}</script>', html)
html = re.sub(r'<script src="lib/babel\.min\.js"></script>', lambda m: f'<script>{babel}</script>', html)

# Minify CSS block
def minify_css(m):
    css = m.group(1)
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
    css = re.sub(r'\s+', ' ', css)
    css = re.sub(r' ?([{};:,>~+]) ?', r'\1', css)
    return f'<style>{css.strip()}</style>'

html = re.sub(r'<style>(.*?)</style>', minify_css, html, flags=re.DOTALL)

# Remove HTML comments
html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)

# Collapse whitespace in non-script/style portions
def collapse_between_tags(text):
    parts = re.split(r'(<script[\s\S]*?</script>|<style[\s\S]*?</style>)', text)
    result = []
    for part in parts:
        if part.startswith('<script') or part.startswith('<style'):
            result.append(part)
        else:
            part = re.sub(r'[ \t]*\n[ \t]*', '\n', part)
            part = re.sub(r'\n{2,}', '\n', part)
            result.append(part)
    return ''.join(result)

html = collapse_between_tags(html)

out = f'{base}/page-mart.html'
with open(out, 'w') as f:
    f.write(html)

size = os.path.getsize(out)
print(f'Done. page-mart.html: {size:,} bytes ({size/1024/1024:.2f} MB)')
