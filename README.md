# Chess Game

## Overview
This is a Python-based chess game developed by **Fadi Abbara** and **Ans Zahran**. It includes an AI-powered opponent, with AI logic sourced from external files: `engine.py` and `chessAi.py`. The game features a graphical interface and supports standard chess rules.

## Features
- Play chess against an AI opponent.
- Graphical user interface with chess piece images.
- Move validation and game state handling.
- Sounds for moves and captures.

## Installation & Setup

### Prerequisites
Ensure you have Python installed (Python 3.x is recommended). You can check your Python version with:
```sh
python --version
```

### Install Required Dependencies
Navigate to the project folder and install dependencies using:
```sh
pip install -r requirements.txt
```

If a `requirements.txt` file is not available, manually install necessary libraries:
```sh
pip install pygame numpy
```

### Running the Game
Execute the following command to start the game:
```sh
python Run.py
```

## Project Structure
```
Chess_Game/
│── chess/                  # AI engine files
│   ├── engine.py           # Chess AI logic
│   ├── chessAi.py         # AI strategy file
│── assets/                 # Game assets (images, fonts, sounds)
│── images/                 # Additional piece images
│── sounds/                 # Sound effects
│── main.py                 # Main game script
│── mainmenu.py             # Menu handling script
│── Run.py                  # Game entry point
│── README.md               # Project documentation
│── .git/                   # Git repository files
```

## Compatibility
### Visual Studio Code
To make this project compatible with **VS Code**, ensure you have the following extensions installed:
- Python extension
- Pygame support (optional)

You can set up a `launch.json` file inside `.vscode/` for debugging:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Chess Game",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/Run.py"
        }
    ]
}
```


## Contributors
- **Fadi Abbara**
- **Ans Zahran**

## License
This project is open-source. Modify and distribute as needed.

---
Enjoy playing chess with AI!

