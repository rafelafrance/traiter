"""Write the traiter output to a file."""

from abc import abstractmethod


class BaseWriter:
    """Write the traiter output to a file."""

    def __init__(self, args):
        """Build the writer."""
        self.args = args
        self.output_file = args.output_file
        self.index = 0
        self.rows = []

    def __enter__(self):
        """Use the writer in with statements."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Use the writer in with statements."""
        self.end()

    def progress(self):
        """Log progress."""
        self.index += 1
        if self.args.log_every and self.index % self.args.log_every == 0:
            print(self.index)

    @abstractmethod
    def start(self):
        """Start the report."""
        raise NotImplementedError('You need a start function.')

    @abstractmethod
    def record(self, raw_record, parsed_record):
        """Output a report record."""
        raise NotImplementedError('You need a record function.')

    @abstractmethod
    def end(self):
        """End the report."""
        raise NotImplementedError('You need a end function.')
