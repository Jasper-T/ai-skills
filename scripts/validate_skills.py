"""Validate this repository's simple scalar metadata and local Markdown links."""
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


def validate(root):
    errors = []
    skills = sorted((root / 'skills').glob('*/SKILL.md'))
    if not skills:
        return ['No skills found']
    for path in skills:
        text = path.read_text()
        parts = text.split('---', 2)
        if len(parts) != 3 or parts[0].strip():
            errors.append(f'{path}: missing frontmatter')
            continue
        fields = dict(re.findall(r'^([\w-]+):\s*(.+)$', parts[1], re.M))
        name = fields.get('name', '').strip('\"\'')
        if name != path.parent.name or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or len(name) >= 64:
            errors.append(f'{path}: invalid or mismatched name')
        if not fields.get('description', '').strip('\"\' '):
            errors.append(f'{path}: missing description')
        interface = path.parent / 'agents/openai.yaml'
        if interface.exists():
            prompt = re.search(r'^\s*default_prompt:\s*(.+)$', interface.read_text(), re.M)
            if prompt:
                refs = re.findall(r'\$([a-z0-9-]+)', prompt[1])
                if name not in refs or any(not (root / 'skills' / ref / 'SKILL.md').is_file() for ref in refs):
                    errors.append(f'{interface}: invalid skill reference')
        for doc in path.parent.rglob('*.md'):
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', doc.read_text()):
                target = target.strip('<>')
                url = urlsplit(target)
                if url.scheme or target.startswith('#'):
                    continue
                if not (doc.parent / unquote(url.path)).exists():
                    errors.append(f'{doc}: missing resource {target}')
    return errors


if __name__ == '__main__':
    errors = validate(Path(__file__).resolve().parents[1])
    print('\n'.join(errors) if errors else 'Skill metadata and resource links valid.')
    sys.exit(bool(errors))
