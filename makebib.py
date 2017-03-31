#!/usr/bin/env python3

'''
Documentation, License etc.

@package makebib
'''

import sys

from pybtex.__main__ import main as run_bibtex
from pybtex import auxfile
from pybtex import database

def make_bib(basename, bib_dbase):
    aux_data = auxfile.parse_file(basename+'.aux')
    db = database.parse_file(bib_dbase)
    outdb = database.BibliographyData({key:db.entries[key] for key in aux_data.citations if key in db.entries })
    outdb.to_file(aux_data.data[0]+'.bib',bib_format='bibtex')

def list_cited_keys(basename):
    aux_data = auxfile.parse_file(basename+'.aux')
    print('\n'.join(aux_data.citations))

def list_db_keys(bib_dbase):
    db = database.parse_file(bib_dbase)
    print('\n'.join(db.entries.keys()))

def list_missing_keys(basename, bib_dbase):
    aux_data = auxfile.parse_file(basename+'.aux')
    db = database.parse_file(bib_dbase)
    missing = [key for key in aux_data.citations if key not in db.entries]
    print('\n'.join(missing))


DB = '~/Documents/Matematika/references.bib'

if __name__ == '__main__':
    if sys.argv[1] == '--list':
        if sys.argv[2] == 'cited':
            list_cited_keys(sys.argv[3])
        elif sys.argv[2] == 'missing':
            list_missing_keys(sys.argv[3], DB)
        elif sys.argv[2] == 'all':
            list_db_keys(DB)
    else:
        make_bib(sys.argv[1], DB)
        run_bibtex()

