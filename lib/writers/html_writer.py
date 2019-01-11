"""Write the traiter output to an HTML file."""

from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from lib.writers.base_writer import BaseWriter

SPAN0 = '<span class="found">'
SPAN1 = '</span>'


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
    # HACK: : This is a temporary set of actions

    @staticmethod
    def format_parsed_record(raw_record):
        """Format the parsed record data."""
        traits = {}
        for trait, data in raw_record.items():
            traits[trait] = []
            for flag, value in data['flags'].items():
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
        colors = {f: bytearray(len(raw_record[f]))
                  for f in self.args.search_field + self.as_is}
        for trait, data in parsed_record.items():
            for parse in data['parsed']:
                field = parse['field']
                start = parse['start']
                end = parse['end']
                colors[field][start:end] = bytearray([1] * (end - start))

        for field, color_map in colors.items():
            last = len(color_map)
            parts = []
            find = b'\x01'
            start = 0
            end = color_map.find(find, start, last)
            while end > -1:
                parts.append(raw_record[field][start:end])
                span = SPAN1 if find == b'\x00' else SPAN0
                parts.append(span)
                find = b'\x00' if find == b'\x01' else b'\x01'
                start = end
                end = color_map.find(find, start, last)
            if find == b'\x00':
                parts.append(raw_record[field][start:last])
                parts.append(SPAN1)

            raw_record[field] = ''.join(parts)

        return raw_record

    # HACK: end
    # #########################################################################
