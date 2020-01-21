"""Write output to an HTML file."""

import html
from itertools import cycle
from collections import namedtuple, deque
from datetime import datetime
import regex
from jinja2 import Environment, FileSystemLoader
import traiter_efloras.trait_groups as tg


# CSS colors
CLASSES = ['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8']
COLORS = cycle(CLASSES)

Cut = namedtuple('Cut', 'pos open len id end type')


def html_writer(args, families, df):
    """Output the data frame."""
    pattern = regex.compile(r'data/raw/\w+/(.+)\.html')
    df['link'] = df['path'].str.replace(pattern, r'\1')
    df = df.fillna('')
    other_cols = [c for c in df.columns if c not in tg.TRAIT_NAMES]

    trait_cols = sorted([c for c in df.columns if c in tg.TRAIT_NAMES])
    df = df.reindex(other_cols + trait_cols, axis='columns')

    trait_cols = {f'{c}_data': c for c in trait_cols}

    df = df.rename(columns={v: k for k, v in trait_cols.items()})

    for col in trait_cols.values():
        df[col] = ''

    df = df.sort_values(by=['family', 'taxon'])

    rows = [x.to_dict() for i, x in df.iterrows()]
    colors = {t: next(COLORS) for t in trait_cols}
    trait_headers = [f'<span class="{colors[k]}">{v}</span>'
                     for k, v in trait_cols.items()]
    tags = build_tags()
    for row in rows:
        format_traits(trait_cols, row)
        format_text(trait_cols, row, tags, colors)

    env = Environment(
        loader=FileSystemLoader('./pylib/writers/templates'),
        autoescape=True)

    template = env.get_template('html_writer.html').render(
        now=datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M'),
        args=args,
        families=families,
        headers=trait_headers,
        traits=trait_cols.values(),
        rows=rows)
    args.output_file.write(template)
    args.output_file.close()


def build_tags():
    """
    Make tags for HTML text color highlighting.

    Tag keys are the the CSS class and if it's an open or close tag.
    For example:
        (css_class, is_open) -> <span class="css_class">
        (css_class, not_open) -> </span>
    """
    tags = {
        ('bold', True): '<strong>',
        ('bold', False): '</strong>'}

    for color in CLASSES:
        tags[(color, True)] = f'<span class={color}>'
        tags[(color, False)] = '</span>'

    return tags


def format_traits(trait_cols, row):
    """Format the traits for HTML."""
    for old, new in trait_cols.items():
        parses = []
        for parse in row[old]:
            attrs = []
            for key, value in parse.__dict__.items():
                if key not in ['start', 'end', 'trait_group']:
                    attrs.append(f'<b>{key}</b>:&nbsp;{value}')
            parses.append('<br/>'.join(attrs))
        row[new] = '<hr/>'.join(parses)


def format_text(trait_cols, row, tags, colors):
    """Colorize and format the text for HTML."""
    text = row['text']

    cuts = []

    cut_id = 0

    for col in trait_cols:
        for trait in row[col]:
            cut_id = append_endpoints(
                cuts, cut_id, trait.start, trait.end, colors[col])

    for trait in tg.TRAIT_GROUPS_RE.finditer(text):
        cut_id = append_endpoints(
            cuts, cut_id, trait.start(), trait.end(), 'bold')

    row['text'] = insert_markup(text, cuts, tags)


def insert_markup(text, cuts, tags):
    """Insert formatting markup for text highlighting etc."""
    # Extract function here
    stack = deque()
    parts = []

    prev_end = 0
    for cut in sorted(cuts):

        # Add text before the tag
        if cut.pos != prev_end:
            parts.append(html.escape(text[prev_end:cut.pos]))
            prev_end = cut.pos

        # Add an open tag
        if cut.open:
            parts.append(tags[(cut.type, True)])  # Add tag to output
            stack.appendleft(cut)                 # Prepend open cut to stack

        # Close tags are more complicated. We have to search for the
        # matching open tag on the stack & remove it. We also need to
        # reopen any intervening open tags. All while adding the
        # appropriate close tags.
        else:
            # Find matching open tag while keeping any intervening tags
            for idx in range(len(stack)):
                # Append closing tag to output
                parts.append(tags[(stack[0].type, False)])

                # Is this the open tag we are looking for?
                # Open tags have a negative ID and close tags are positive.
                # This pushes the tags to the correct position for sorted
                if abs(stack[0].id) == cut.id:
                    break
                stack.rotate(-1)
            else:
                raise IndexError('Matching open tag not found in stack.')
            # Get rid of matching open tag
            stack.popleft()

            # Put intervening open tags back on stack & reopen in text
            for _ in range(idx):
                stack.rotate(1)
                parts.append(tags[(stack[0].type, True)])

    # Handle text after the last closing tag
    if prev_end != len(text):
        parts.append(html.escape(text[prev_end:]))

    return ''.join(parts)


def append_endpoints(cuts, cut_id, start, end, tag_type):
    """
    Append endpoints to the cuts.

    The only interesting point is that open cuts have a negative len and
    matching close cuts have a positive len. This will push the cuts to the
    correct position during a sort. Longer cuts need to surround inner cuts.

    Like so:
    [open_cut(len=-2), open_cut(len=-1), close_cut(len=1), close_cut(len=2)]

    The same logic applies to the ID field. We push later tags outward:
    [open_cut(id=-2), open_cut(id=-1), close_cut(id=1), close_cut(id=2)]
    """
    cut_id += 1            # Absolute value is the ID
    trait_len = end - start

    cuts.append(Cut(
        pos=start,
        open=True,              # Close tags come before open tags
        len=-trait_len,         # Longest tags open first
        id=-cut_id,             # Force an order. Push open tags leftward
        end=end,
        type=tag_type))

    cuts.append(Cut(
        pos=end,
        open=False,             # Close tags come before open tags
        len=trait_len,          # Longest tags close last
        id=cut_id,              # Force an order. Push close tags rightward
        end=end,
        type=tag_type))

    return cut_id
