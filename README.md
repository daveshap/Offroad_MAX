# Offroad_MAX
Simple prototype of a procedurally generated hill climbing game. Each run
creates new terrain so the course is never the same twice.

## Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Running

Launch the game using:

```bash
python game.py
```

Use the arrow keys to drive the truck across the terrain.

## Converting PDFs to Text

The repository includes a small utility script `convert_pdfs_to_txt.py` which
converts all PDF files in the current directory to text files. It uses
`PyPDF2` for extracting text. Install the extra dependency and run the script
as follows:

```bash
pip install PyPDF2
python convert_pdfs_to_txt.py
```

Every PDF in the same folder will generate a corresponding `.txt` file with the
same base name.
