import re

def top_blocks(text):
    """Split text into top-level <div>...</div> blocks, honouring nesting."""
    text = re.sub(r'\n?<!--\s*colbreak\s*-->\n?', '\n', text)   # drop stale breaks
    blocks, depth, start = [], 0, None
    for m in re.finditer(r'<div\b[^>]*>|</div>', text):
        if not m.group(0).startswith('</'):
            if depth == 0: start = m.start()
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                blocks.append(text[start:m.end()])
    return blocks
