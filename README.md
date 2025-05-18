# codex_test

This repository now contains a minimal console implementation of **Puyo Puyo** in Python.

## Running the game

Run the script with Python 3:

```bash
python puyo.py
```

Controls:

- `a`: move left
- `d`: move right
- `w`: rotate piece
- `s`: drop piece immediately
- `q`: quit the game

The board displays falling pieces in lowercase letters and placed pieces in uppercase. Groups of four or more matching colors vanish and gravity pulls remaining pieces down. The game ends when new pieces can no longer spawn.

## Colors

Pieces are represented by single letters corresponding to their colors:

- `R` = Red
- `G` = Green
- `B` = Blue
- `O` = Yellow
- `P` = Purple

You can run the following command to check that the script compiles:

```bash
python -m py_compile puyo.py
```
