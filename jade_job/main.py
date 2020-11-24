import argparse
import sys
from jade_job import __version__ as jade_job_version


class DefaultHelpParser(argparse.ArgumentParser):
    def error(self, message):
        """Print help message by default."""
        sys.stderr.write(f'error: {message}\n')
        self.print_help()
        sys.exit(2)


def run(arguments=None):
    parser = DefaultHelpParser(description="A simple Jade Job CLI.")
    parser.add_argument('-V', '--version', action='version', version='%(prog)s ' + jade_job_version,
    )
    args = parser.parse_args(arguments)

    if not sys.argv[1:]:
        parser.error("No commands or arguments provided!")
