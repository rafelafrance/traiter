"""Write the traiter output to an HTML file."""

# pylint: disable=import-error

import json
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from lib.writers.base_writer import BaseWriter


class HtmlWriter(BaseWriter):
    """Write the traiter output to a file."""

    def __init__(self, args):
        """Build the writer."""
        super().__init__(args)
        self.index = 0
        self.rows = []
        self.started = None

    def start(self):
        """Start the report."""
        self.started = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M')
        self.rows = []

    def record(self, raw_record, parsed_record):
        """Output a row to the file."""
        self.index += 1
        if self.args.log_every and self.index % self.args.log_every == 0:
            print(self.index)
        for _, record in parsed_record.items():
            for parse in record:
                if parse.get('value'):
                    parse['value'] = json.dumps(parse['value'])
        self.rows.append(
            {'raw': raw_record, 'parsed': parsed_record, 'index': self.index})

    def end(self):
        """End the report."""
        env = Environment(loader=FileSystemLoader('./lib/writers/templates'))
        args = {k: v for k, v in vars(self.args).items() if k
                in ('as_is', 'extra_field', 'search_field', 'trait')}
        template = env.get_template('html_writer.html').render(
            now=self.started,
            as_is=sorted({f for fds in self.args.as_is.values() for f in fds}),
            args=args,
            rows=self.rows,
        )
        self.args.outfile.write(template)
        self.args.outfile.close()
