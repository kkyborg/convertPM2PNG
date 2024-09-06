`python3 -m venv path/to/venv`\
`source path/to/venv/bin/activate`

`for file in *.pm; do python3 convertPM2PNG.py "$file" Palette.pal --color-list recognize.txt; done`
