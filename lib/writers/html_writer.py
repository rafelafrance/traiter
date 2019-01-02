"""Write the traiter output to an HTML file."""

# from datetime import datetime
# from jinja2 import Environment, FileSystemLoader, Template
from lib.writers.base_writer import BaseWriter

# TEMPLATE = Template(
#     '{{ left }}<span class="found">{{ middle }}</span>{{ right }}')


class HtmlWriter(BaseWriter):
    """Write the traiter output to a file."""

    def __init__(self, args):
        """Build the writer."""

    def start(self):
        """Start the report."""
        # return []

    def row(self):
        """Build a report row."""
        # writer.append(out_row)

    def cell(self):
        """Build a report cell."""
        # if parsed['found']:
        #     field_name = parsed['field']
        #     field = row[field_name]
        #     start = parsed['start']
        #     end = parsed['end']
        #     left = field[:start] if start else ''
        #     middle = field[start:end]
        #     right = field[end:] if end <= len(field) else ''
        #     row[field_name] = TEMPLATE.render(
        #         left=left, middle=middle, right=right)
        # return parsed

    def end(self):
        """End the report."""
        # env = Environment(loader=FileSystemLoader('./lib/templates'))
        # template = env.get_template('traiter.html')
        # report = template.render(
        #     args=vars(args),
        #     now=datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M'),
        #     rows=writer,
        #     preferred_columns=preferred_columns,
        #     totals=totals)
        # args.outfile.write(report)
