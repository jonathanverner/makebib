#!/usr/bin/env python3

'''
A simple script to generate a local bib file from a central
database so that only items actually cited appear.
'''

import os
import sys
import argparse

from pybtex.__main__ import main as run_bibtex
from pybtex import auxfile
from pybtex import database

DEFAULT_CFG = {
    'db': '~/.makebib/db.bib'
}
CFG_FILES = ['/etc/makebib', '~/.makebib', './.makebib']


def construct_argparser():
    parser = argparse.ArgumentParser(
        description='A simple script to generate a local bib file from a central database.',
        epilog="""
  CONFIGURATION

  The program reads its configuration from """+', '.join(CFG_FILES)+""".
  Each configuration option is given on a single line in the form of

        key = val

  Spaces around '=' are ignored as is everything following the first '#'.
  Lines not containing '=' are also ignored. The options are case-insensitive.
  Currently the following options (and their default values) are available:

"""+'\n'.join(["        " + k + " = " + v for k, v in DEFAULT_CFG.items()])
    )
    parser.add_argument('--db', help='Path to the central bib dbase')
    parser.add_argument('--config', help='Path to the configuration file')

    command_parsers = parser.add_subparsers(dest='action')

    compile_parser = command_parsers.add_parser('compile', help='Create a local bib file for the given TeX-file and run BibTeX')
    compile_parser.add_argument('document', help='base filename of the TeX source')
    compile_parser.add_argument('--nobibtex', help='do not run bibtex', action='store_true', default=False)

    show_parser = command_parsers.add_parser('show', help='Show various information')
    showcommand_parsers = show_parser.add_subparsers(help='Information types', dest='info_type')
    cited_parser = showcommand_parsers.add_parser('cited', help='Show all the keys cited by the specified TeX document')
    cited_parser.add_argument('document', help='base filename of the TeX source')

    missing_parser = showcommand_parsers.add_parser('missing', help='Show all the keys cited by the specified TeX document & missing from the central dbase')
    missing_parser.add_argument('document', help='base filename of the TeX source')

    all_parser = showcommand_parsers.add_parser('all', help='Show all the cite keys in the central dbase')

    entry_parser = showcommand_parsers.add_parser('bibentry', help='Show the database entry with the given key')
    entry_parser.add_argument('key', help='The citekey of the entry to show')

    cfg_parser = showcommand_parsers.add_parser('cfg', help='Show configuration')

    return parser


def make_bib(basename, bib_dbase):
    aux_data = auxfile.parse_file(basename + '.aux')
    db = database.parse_file(os.path.expanduser(bib_dbase))
    outdb = database.BibliographyData({key: db.entries[key] for key in aux_data.citations if key in db.entries})
    outdb.to_file(aux_data.data[0] + '.bib', bib_format='bibtex')


def list_cited_keys(basename):
    aux_data = auxfile.parse_file(basename + '.aux')
    print('\n'.join(aux_data.citations))


def list_db_keys(bib_dbase):
    db = database.parse_file(os.path.expanduser(bib_dbase))
    print('\n'.join(db.entries.keys()))


def list_missing_keys(basename, bib_dbase):
    aux_data = auxfile.parse_file(basename + '.aux')
    db = database.parse_file(os.path.expanduser(bib_dbase))
    missing = [key for key in aux_data.citations if key not in db.entries]
    print('\n'.join(missing))


def show_bibentry(key, bib_dbase):
    db = database.parse_file(os.path.expanduser(bib_dbase))
    if key in db.entries:
        data = database.BibliographyData(entries={key: db.entries[key]})
        print(data.to_string(bib_format='bibtex'))


def load_cfg(cfg_file=None):
    global CFG_FILES, DEFAULT_CFG
    cfg = {}
    for k, v in DEFAULT_CFG.items():
        cfg[k] = v
    if cfg_file is not None:
        CFG_FILES.append(cfg_file)
    for f in CFG_FILES:
        f = os.path.expanduser(f)
        if os.path.exists(f):
            with open(f, 'r') as IN:
                for ln in IN.readlines():
                    comment_pos = ln.find('#')
                    if comment_pos > -1:
                        ln = ln[:comment_pos]
                    try:
                        key, val = ln.split('=')
                        key = key.strip().lower()
                        val = val.strip()
                        if len(key) > 0:
                            cfg[key] = val
                    except:
                        pass
    return cfg


def main():
    args = construct_argparser().parse_args()
    CFG = load_cfg(args.config)

    if args.db:
        CFG['db'] = args.db

    if args.action == 'compile':
        make_bib(args.document, CFG['db'])
        if not args.nobibtex:
            run_bibtex()

    elif args.action == 'show':

        if args.info_type == 'cited':
            list_cited_keys(args.document)

        elif args.info_type == 'missing':
            list_missing_keys(args.document, CFG['db'])

        elif args.info_type == 'all':
            list_db_keys(CFG['db'])

        elif args.info_type == 'bibentry':
            show_bibentry(args.key, CFG['db'])
        elif args.info_type == 'cfg':
            for k, v in CFG.items():
                print(k, '=', v)
    else:
        print("No command specified, defaulting to compile")
        make_bib(args.action, CFG['db'])
        run_bibtex()
