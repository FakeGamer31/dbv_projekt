# DBV Project Brick Detection with OpenCV

This project was created in the context of the "Digitale Bildverarbeitung" module. The project is used to recognize simple building blocks. The project consists of 2 main components, the GUI, which was created using PyQt5 and the recognition logic, which was realized using OpenCV.
The recognition can be applied to a live or a static image. The recognized bricks are marked and labeled in the image and a list of all bricks is output.

## Project Setup

### Requirements

- Python 3.10.11
- Additional dependencies will be installed from the [requirmenets.txt](/requirmenets.txt)

### Installation and Run

- Create a virutal enviroment
  ```bash
  python -m venv .venv
  ```
- Activate the virutal enviroment
  ```bash
  .venv\Scripts\activate
  ```
- Install the dependencies from the [requirmenets.txt](/requirmenets.txt)
  ```bash
  pip install -r requirements.txt
  ```
- Run the [main.py](/src/main.py)
  ```bash
  py src\main.py
  ```
