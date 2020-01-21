"""Read pages scraped from the eFloras website."""

import sys
from collections import defaultdict
import regex
from lxml import html
import pandas as pd
import traiter_efloras.util as util
import traiter_efloras.trait_groups as tg

TAXA = {}


def efloras_reader(args, families):
    """Parse all pages for the given families."""
    rows = []
    for family in args.family:
        name = families[family]['name']
        root = util.RAW_DIR / f'{name}'
        for path in root.glob('**/*.html'):
            row = parse_efloras_page(args, path, family)
            rows.append(row)
    df = pd.DataFrame(rows)
    return df


def parse_efloras_page(args, path, family):
    """Parse the taxon page."""
    page = get_efloras_page(path)
    taxon = get_taxon(page)
    check_taxon(taxon, path)

    row = {
        'family': family,
        'taxon': taxon,
        'path': str(path),
        'text': ''}

    para, text = find_trait_groups_paragraph(page)
    if para is not None:
        check_trait_groups(para)
        row['text'] = text
        row = {**row, **parse_trait_groups(args, text)}
    return row


def check_taxon(taxon, path):
    """Make sure the taxon parse is reasonable."""
    if taxon in TAXA:
        print(f'Previously on {TAXA[taxon]}')
        sys.exit()
    TAXA[taxon] = path


def get_efloras_page(path):
    """Get the taxon description page."""
    with open(path) as in_file:
        page = in_file.read()
    return html.fromstring(page)


def get_taxon(page):
    """Get the taxon description."""
    taxon_id = 'lblTaxonDesc'
    taxon = page.xpath(f'//*[@id="{taxon_id}"]/b/text()')
    taxon = ' '.join(taxon)
    return taxon


def find_trait_groups_paragraph(page):
    """Scan the page for the traits paragraph."""
    treatment_id = 'panelTaxonTreatment'  # HTML ID of the plant treatment

    # Find the general area on the page with the trait groups
    paras = page.xpath(f'//*[@id="{treatment_id}"]//p')

    for para in paras:
        text = ' '.join(para.text_content().split())
        match = tg.TRAIT_GROUPS_RE.search(text)
        if match:
            return para, text

    return None, None


def check_trait_groups(para):  # , text):
    """Validate that we have all of the traits."""
    bold = para.xpath('.//b')  # Used to check the trait group parse

    # We are just using the bold items as a check on the trait groups
    bolds = [regex.sub('[:.,]', '', x.text_content()) for x in bold]
    bolds = [x.strip().lower() for x in bolds if x]

    # Fewer trait groups than bold items means something is wrong
    if set(bolds) > set(tg.TRAIT_GROUPS.keys()):
        diff = set(bolds) - set(tg.TRAIT_GROUPS.keys())
        sys.exit(f'Found new trait group: {diff}')


def parse_trait_groups(args, text):
    """Parse each trait group."""
    traits = defaultdict(list)
    slices = [(m.start(), m.end()) for m in tg.TRAIT_GROUPS_RE.finditer(text)]
    slices.append((-1, -1))
    for i, (start, end) in enumerate(slices[:-1]):
        after, _ = slices[i + 1]
        trait_group = text[start:end].lower()
        group_data = text[start:after]
        parser_group = [g for g in tg.TRAIT_GROUPS.get(trait_group)
                        if args.trait in g.name]
        for parser in parser_group:
            parses = parser.parse(group_data)
            if parses:
                for parse in parses:
                    setattr(parse, 'trait_group', trait_group)
                    parse.start += start
                    parse.end += start
                traits[parser.name] += parses
    return traits
