"""Build a dependency-free HTML file from public source and fictional examples."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def build():
    template = (ROOT / 'src/index.template.html').read_text(encoding='utf-8')
    data = json.loads((ROOT / 'examples/resume.example.json').read_text(encoding='utf-8'))
    replacements = {
        '__INITIAL_DATA__': json.dumps(data, ensure_ascii=False).replace('<', '\\u003c'),
        '__CUSTOM_CSS__': (ROOT / 'src/custom-layout.css').read_text(encoding='utf-8'),
        '__CUSTOM_JS__': (ROOT / 'src/custom-layout.js').read_text(encoding='utf-8'),
    }
    for marker, value in replacements.items():
        assert template.count(marker) == 1, f'Expected exactly one {marker}'
        template = template.replace(marker, value)
    return template

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Check that index.html matches source')
    args = parser.parse_args()
    result = build()
    output = ROOT / 'index.html'
    if args.check:
        assert output.read_text(encoding='utf-8') == result, 'Run python scripts/build.py to update index.html'
        print('Build is up to date.')
    else:
        output.write_text(result, encoding='utf-8')
        print('Built index.html')
