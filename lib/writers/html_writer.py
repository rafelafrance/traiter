"""Write the traiter output to an HTML file."""

from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from lib.writers.base_writer import BaseWriter

SPAN_OPEN = '<span class="found">'
SPAN_CLOSE = '</span>'
OPEN = 1
CLOSE = 0
WHITE = 0
GREEN = 1


class HtmlWriter(BaseWriter):
    """Write the traiter output to a file."""

    def __init__(self, args):
        """Build the writer."""
        super().__init__(args)
        self.writer = args.outfile
        self.index = 0
        self.env = Environment(
            loader=FileSystemLoader('./lib/writers/templates'))
        self.row_template = self.env.get_template('row.html')
        self.as_is = sorted(
            {f for fds in self.args.as_is.values() for f in fds})

    def start(self):
        """Start the report."""
        template = self.env.get_template('start.html')
        header = template.render(
            now=datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M'),
            as_is=self.as_is,
            args=self.args)
        self.writer.write(header)

    def record(self, raw_record, parsed_record):
        """Output a row to the file."""
        self.index += 1
        if self.index % 1000 == 0:
            print(self.index)
        row = self.row_template.render(
            args=self.args,
            as_is=self.as_is,
            index=self.index,
            parsed=self.format_parsed_record(parsed_record),
            record=self.format_raw_record(raw_record, parsed_record))
        self.writer.write(row)

    def end(self):
        """End the report."""
        template = self.env.get_template('end.html')
        footer = template.render()
        self.writer.write(footer)
        self.writer.close()

    # #########################################################################
    # HACK: : I hope that this is a temporary set of actions

    @staticmethod
    def format_parsed_record(raw_record):
        """Format the parsed record data."""
        traits = {}
        for trait, data in raw_record.items():
            traits[trait] = []
            for _, value in data['flags'].items():
                traits[trait].append({'msg': value})
            for parse in data['parsed']:
                parse['new_flags'] = []
                for key, val in parse['flags'].items():
                    if key in ('as_is', ):
                        continue
                    key = key.replace('_', ' ')
                    if val is True:
                        parse['new_flags'].append('{}'.format(key))
                    else:
                        parse['new_flags'].append('{} {}'.format(key, val))
                parse['new_flags'] = sorted(parse['new_flags'])
                traits[trait].append(parse)
        return traits

    def format_raw_record(self, raw_record, parsed_record):
        """Format the record for output."""
        colors = {f: [WHITE] * len(raw_record[f])
                  for f in self.args.search_field + self.as_is}

        for _, data in parsed_record.items():
            for parse in data['parsed']:
                field = parse['field']
                start = parse['start']
                end = parse['end']
                colors[field][start:end] = [GREEN] * (end - start)

        for field, color in colors.items():
            if not color:
                continue
            ends = [0]
            ends += [i for i in range(1, len(color)-1)
                     if color[i-1] != color[i]]
            parts = [SPAN_OPEN] if color[0] == GREEN else []
            for i, end in enumerate(ends[1:], 1):
                parts.append(raw_record[field][ends[i-1]:end])
                if color[end] == WHITE:
                    parts.append(SPAN_CLOSE)
                else:
                    parts.append(SPAN_OPEN)
            parts.append(raw_record[field][ends[-1]:])
            if color[-1] == GREEN:
                parts.append(SPAN_CLOSE)
            raw_record[field] = ''.join(parts)

        return raw_record

    # HACK: end
    # #########################################################################
