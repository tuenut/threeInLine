from argparse import ArgumentParser, RawDescriptionHelpFormatter


def parse_arguments():
    args_parser = ArgumentParser(
        prog='Three In Line Game',
        formatter_class=RawDescriptionHelpFormatter,
        description='Three In Line Game made by tuenut.',
        epilog='Author: tuenut'
    )

    parsed_arguments = args_parser.parse_args()

    return parsed_arguments
