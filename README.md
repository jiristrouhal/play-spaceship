# Introduction

A simple ReAct agent built from scratch, with a purpose to control and land a spaceship using a short list of tools to control the ship, read its state and verify the landing.

# Setup

## Dependencies

Create and activate a virtual environment and install Python packages:

```bash
python3 -m venv .venv  && \
source .venv/bin/activate && \
pip install -r requirements.txt
```

## Clone the game

Choose a `<game-path>`, go to it and run

```bash
git clone https://github.com/jiristrouhal/spaceship.git
```

## Environment variables

Create the following environment variables:

```bash
OPENAI_API_KEY = "<your-openai-api-key>"
SPACESHIP_GAME_PATH = "<game-path>"
```

# Run the game

Go to the root directory and run

```bash
python3 -m spaceship
```

The game window pops up and the agent starts controlling the spaceship using simulated keyboard presses.

The game automatically closes after the landing is verified.