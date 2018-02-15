Changelog
=========

0.2.2 (2018-02-15)
------------------

New
~~~
- Sort the entries in the generated bib-file. [Jonathan Verner]

  This change makes sure the bib-file does not change on each run
  (and thus makes things easier if it is kept under VCS).


0.2.1 (2017-04-12)
------------------

New
~~~
- Use altkeys field to search for additional citekeys. [Jonathan Verner]

  This change allows a BibTeX entry to have an altkeys field, which is a
  comma separated list of additional citekeys by which the entry may
  be cited in the document.


0.2.0 (2017-04-03)
------------------

New
~~~
- Refuse to overwrite preexistent files. [Jonathan Verner]
- Implement the show bibentry subcommand. [Jonathan Verner]

Fix
~~~
- Update the documentation. [Jonathan Verner]
- Properly pass arguments to BibTeX. [Jonathan Verner]


0.1.0 (2017-04-03)
------------------
- Create a Python package installable via pip. [Jonathan Verner]
- Fix list markup in README.md. [Jonathan L. Verner]
- Merge branch 'master' of gitlab.com:Verner/makebib. [Jonathan Verner]
- Add license. [Jonathan L. Verner]
- Prepare for public release. [Jonathan Verner]
- Initial commit. [Jonathan Verner]
- Initial project import from KDevelop. [Jonathan Verner]


