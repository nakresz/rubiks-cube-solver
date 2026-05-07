# Rubik's Cube Solver

A step-by-step Rubik's Cube solver project built from scratch using Python.

This project starts by building a Rubik's Cube engine, then gradually adds scrambling, inverse algorithms, search-based solving, and visualization.

## Features

- 3x3 Rubik's Cube representation
- All basic face moves:
  - U, U', U2
  - D, D', D2
  - R, R', R2
  - L, L', L2
  - F, F', F2
  - B, B', B2
- Random scramble generation
- Inverse algorithm generation
- Cube state display in the terminal
- Clean project structure for future solver algorithms

## Project Structure

```text
rubiks-cube-solver/
│
├── src/
│   ├── __init__.py
│   ├── cube.py
│   ├── moves.py
│   └── scrambler.py
│
├── tests/
├── main.py
├── README.md
├── requirements.txt
└── .gitignore