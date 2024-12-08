import logging
import optparse
import pymind
from logging import CRITICAL, DEBUG, WARNING

from yaml import load as yaml_load

logger = logging.getLogger("PYMIND")

########################################################################################################################


##======================================================================================================================
#
def parse_options(args=None, values=None):
    """
    Define and parse `optparse` options for command-line usage.
    """

    # Program description and use
    usage = """%prog [options] [INPUTDIR]"""
    desc = (
        "A Python implementation of a text-based second brain that just works. "
        "https://Python-Markdown.github.io/"
    )
    ver = str(pymind.__version__)

    # Optional flags
    parser = optparse.OptionParser(usage=usage, description=desc, version=ver)
    parser.add_option(
        "-i",
        "--input",
        dest="input",
        default="notes",
        metavar="INPUT_DIR",
        help="Relative path to a directory to recursively scan.",
    )
    parser.add_option(
        "-o",
        "--output",
        dest="output",
        default="doc",
        metavar="OUTPUT_DIR",
        help="Use to specify output directory, default is `doc`.",
    )
    parser.add_option(
        "-f",
        "--force",
        dest="force",
        default=False,
        help="Regenerate the entire project.",
        metavar="FORCE",
    )
    parser.add_option(
        "-d",
        "--dry_run",
        dest="dry_run",
        default=False,
        help="Do everything except generate the files.",
        metavar="DRY_RUN",
    )
    parser.add_option(
        "-e",
        "--engine",
        dest="engine",
        default=True,
        help="Run the script engine",
        metavar="ENGINE",
    )
    parser.add_option(
        "-c",
        "--config",
        dest="configfile",
        default=None,
        help="Read configurations from CONFIG_FILE."
        "CONFIG_FILE must be of YAML format. YAML"
        "format requires that a python YAML library be"
        "installed. ",
        metavar="CONFIG_FILE",
    )
    parser.add_option(
        "-q",
        "--quiet",
        default=CRITICAL,
        action="store_const",
        const=CRITICAL + 10,
        dest="verbose",
        help="Suppress all warnings.",
    )
    parser.add_option(
        "-v",
        "--verbose",
        action="store_const",
        const=WARNING,
        dest="verbose",
        help="Print all warnings.",
    )
    parser.add_option(
        "--noisy",
        action="store_const",
        const=DEBUG,
        dest="verbose",
        help="Print debug messages.",
    )

    # Parse the input arguments
    (options, args) = parser.parse_args(args, values)

    # Read configuration file
    config = {}
    if options.configfile:
        with codecs.open(options.configfile, mode="r", encoding=options.encoding) as fp:
            try:
                config = yaml_load(fp)
            except Exception as e:
                message = (
                    "Failed parsing extension config file: %s" % options.configfile
                )
                e.args = (message,) + e.args[1:]
                raise

    # Save the options
    opts = {
        "input": options.input,
        "output": options.output,
        "dry_run": options.dry_run,
        "force": options.force,
        "engine": options.engine,
        "config": config,
    }

    return opts, options.verbose


##======================================================================================================================
#
def run():
    """Run PyMind from the command line."""

    # Parse options and adjust logging level if necessary
    options, logging_level = parse_options()

    # If options is empty
    if not options:
        sys.exit(2)

    # Set the logging level
    logger.setLevel(logging_level)
    console_handler = logging.StreamHandler()
    logger.addHandler(console_handler)

    if logging_level <= WARNING:
        # Ensure deprecation warnings get displayed
        warnings.filterwarnings("default")
        logging.captureWarnings(True)
        warn_logger = logging.getLogger("py.warnings")
        warn_logger.addHandler(console_handler)

    # Run `PyMind`
    pymind.pymind(**options)
    return


########################################################################################################################

if __name__ == "__main__":  # pragma: no cover
    # Support running module as a command line command.
    #     python -m markdown [options] [args]
    run()
