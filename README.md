# Zelda Miloutte

A 2D top-down Zelda-like adventure game built with [pygame-ce](https://pyga.me/) (Community Edition). Explore an overworld, fight enemies, collect items, and enter dungeons with boss fights.

All pixel art and sound effects are procedurally generated — no external image or audio assets needed.

## Table of Contents

- [Play Locally](#play-locally)
- [Play in the Browser (Mobile & Desktop)](#play-in-the-browser-mobile--desktop)
  - [How It Works](#how-it-works)
  - [Step 1: Code Changes for Web Compatibility](#step-1-code-changes-for-web-compatibility)
  - [Step 2: Build Locally and Test](#step-2-build-locally-and-test)
  - [Step 3: Create a GitHub Repository](#step-3-create-a-github-repository)
  - [Step 4: Add the GitHub Actions Workflow](#step-4-add-the-github-actions-workflow)
  - [Step 5: Configure Repository Permissions](#step-5-configure-repository-permissions)
  - [Step 6: Enable GitHub Pages](#step-6-enable-github-pages)
  - [Step 7: Trigger the First Deploy](#step-7-trigger-the-first-deploy)
  - [Step 8: Access Your Game](#step-8-access-your-game)
- [How Pygbag Works Under the Hood](#how-pygbag-works-under-the-hood)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)

---

## Play Locally

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (Python package manager)

### Run the Game

```bash
# Install dependencies
uv sync

# Run
uv run zelda-miloutte
```

### Controls (Keyboard)

| Action    | Keys              |
|-----------|-------------------|
| Move      | Arrow keys / WASD |
| Attack    | Space             |
| Interact  | E / Enter         |
| Pause     | Escape            |

---

## Play in the Browser (Mobile & Desktop)

This section explains how to deploy the game as a web app playable on any device (including phones) using **pygbag** and **GitHub Pages**. The total cost is **$0**.

### How It Works

[Pygbag](https://github.com/pygame-web/pygbag) compiles your Python + pygame-ce game into **WebAssembly (WASM)**, which runs natively in modern web browsers. It bundles your entire game (code, assets, Python interpreter) into static files (HTML + JS + WASM) that can be hosted on any static file server.

**GitHub Pages** serves those static files for free. A GitHub Actions workflow rebuilds and redeploys automatically on every `git push`.

The result: push your code, and within ~2 minutes your game is live at `https://<your-username>.github.io/<repo-name>/`.

---

### Step 1: Code Changes for Web Compatibility

Pygbag requires two changes to your game code:

#### 1a. Make the game loop async

Browsers cannot run a blocking `while True` loop — it would freeze the tab. Pygbag solves this by requiring your main game loop to be an `async` function that yields control back to the browser each frame with `await asyncio.sleep(0)`.

**In `zelda_miloutte/main.py`**, change:

```python
# BEFORE (desktop only)
from zelda_miloutte.game import Game
from zelda_miloutte.states.cinematic_state import CinematicState


def main():
    game = Game()
    game.push_state(CinematicState(game))
    game.run()


if __name__ == "__main__":
    main()
```

To:

```python
# AFTER (works on both desktop and web)
import asyncio
from zelda_miloutte.game import Game
from zelda_miloutte.states.cinematic_state import CinematicState


async def main():
    game = Game()
    game.push_state(CinematicState(game))
    await game.run()


asyncio.run(main())
```

**In `zelda_miloutte/game.py`**, make the `run()` method async:

```python
# BEFORE
def run(self):
    while self.running:
        dt = self.clock.tick(FPS) / 1000.0
        # ... game loop body ...
    pygame.quit()

# AFTER
async def run(self):
    while self.running:
        dt = self.clock.tick(FPS) / 1000.0
        # ... game loop body stays exactly the same ...

        await asyncio.sleep(0)  # <-- Add this as the LAST line inside the while loop

    pygame.quit()
```

Add `import asyncio` at the top of `game.py`.

The `await asyncio.sleep(0)` does nothing on desktop (it yields and immediately resumes). In the browser, it gives the browser event loop a chance to render the frame and process input. This one line is what makes the game work on the web.

#### 1b. Add touch controls for mobile

On a phone there is no keyboard, so you need virtual on-screen buttons. This means adding a transparent overlay with a D-pad and action buttons that inject pygame keyboard events when touched. This is a code change to the input handling and drawing systems (detailed implementation is a separate task).

---

### Step 2: Build Locally and Test

#### Install pygbag

```bash
uv pip install pygbag
```

Or add it to your dev dependencies:

```bash
uv add --dev pygbag
```

#### Build the web version

```bash
# This builds AND starts a local test server
uv run pygbag zelda_miloutte

# Or build only (no server)
uv run pygbag --build zelda_miloutte
```

When running without `--build`, pygbag starts a local server at **http://localhost:8000**. Open this URL in your browser (or on your phone if on the same WiFi network, using your computer's local IP like `http://192.168.x.x:8000`).

The build output goes to `zelda_miloutte/build/web/`. This folder contains everything needed to host the game:

```
zelda_miloutte/build/web/
  index.html          # The web page that loads the game
  *.js                # JavaScript loader/runtime
  *.wasm              # Compiled Python interpreter (WebAssembly)
  *.data              # Your game code + assets, packaged
```

#### What to verify

- The game loads (you see the title screen)
- Sound effects play (click/tap the page first — browsers require user interaction before playing audio)
- Touch controls work on mobile (D-pad + buttons)
- The game fits the phone screen without horizontal scrolling

---

### Step 3: Create a GitHub Repository

If you don't have a GitHub repo yet:

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit"

# Create repo on GitHub and push
# Using GitHub CLI (gh):
gh repo create zelda-miloutte --public --source=. --push

# Or using git directly (create the repo on github.com first, then):
git remote add origin https://github.com/<your-username>/zelda-miloutte.git
git branch -M main
git push -u origin main
```

The repo **must be public** for free GitHub Pages hosting.

---

### Step 4: Add the GitHub Actions Workflow

Create the file `.github/workflows/deploy.yml` in your repository with this content:

```yaml
name: Deploy to GitHub Pages

on:
  # Runs on pushes to main
  push:
    branches:
      - main

  # Allows manual trigger from the Actions tab
  workflow_dispatch:

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
      # 1. Check out the repository
      - name: Checkout
        uses: actions/checkout@v4

      # 2. Set up Python
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"

      # 3. Install pygbag
      - name: Install pygbag
        run: pip install pygbag

      # 4. Build the game for web
      - name: Build with pygbag
        run: python -m pygbag --build $GITHUB_WORKSPACE/zelda_miloutte

      # 5. Deploy to gh-pages branch
      - name: Deploy to GitHub Pages
        uses: JamesIves/github-pages-deploy-action@v4
        with:
          branch: gh-pages
          folder: zelda_miloutte/build/web
```

**What this does:**
1. On every push to `main` (or manual trigger), it spins up an Ubuntu VM
2. Installs Python 3.13 and pygbag
3. Runs `pygbag --build` to compile your game to WebAssembly
4. Copies the `build/web/` output to a `gh-pages` branch using the [JamesIves deploy action](https://github.com/JamesIves/github-pages-deploy-action)

Commit and push this file:

```bash
mkdir -p .github/workflows
# (create the file above)
git add .github/workflows/deploy.yml
git commit -m "Add GitHub Pages deploy workflow"
git push
```

---

### Step 5: Configure Repository Permissions

The GitHub Action needs write access to create the `gh-pages` branch.

1. Go to your repository on GitHub
2. Click **Settings** (top menu bar)
3. In the left sidebar, click **Actions** > **General**
4. Scroll down to **Workflow permissions**
5. Select **Read and write permissions**
6. Click **Save**

If you skip this step, the deploy action will fail with a permissions error.

---

### Step 6: Enable GitHub Pages

1. Go to **Settings** > **Pages** (in the left sidebar under "Code and automation")
2. Under **Source**, select **Deploy from a branch**
3. Under **Branch**, select **gh-pages** and **/ (root)**
4. Click **Save**

> **Note:** The `gh-pages` branch won't exist until the workflow runs for the first time. If you don't see it in the dropdown yet, proceed to Step 7 first, then come back here.

---

### Step 7: Trigger the First Deploy

The workflow runs automatically on push to `main`. If you already pushed the workflow file, it should be running. Check the status:

1. Go to the **Actions** tab in your repository
2. You should see the "Deploy to GitHub Pages" workflow
3. Click on it to see the progress
4. If it hasn't triggered, click **Run workflow** > **Run workflow** (manual trigger)

The first build takes ~2-3 minutes. Subsequent builds are similar (pygbag compiles from scratch each time).

If the build succeeds, you'll see a green checkmark. If it fails, click into the failed job to see the error logs.

---

### Step 8: Access Your Game

Once the deploy completes and Pages is enabled, your game is live at:

```
https://<your-username>.github.io/zelda-miloutte/
```

Open this URL on your phone's browser. That's it — you're playing your game on your phone.

**Share the link** with anyone — they can play instantly, no install required.

---

## How Pygbag Works Under the Hood

If you're curious about the technology:

1. **Emscripten + CPython**: Pygbag uses [Emscripten](https://emscripten.org/) to compile the CPython interpreter to WebAssembly. This means a real Python 3 runtime runs in your browser.

2. **pygame-ce → SDL2 → Emscripten**: pygame-ce is built on SDL2 for graphics/audio. Emscripten has SDL2 support that maps it to browser Canvas and Web Audio APIs.

3. **Async bridge**: The `await asyncio.sleep(0)` yields control from Python back to the browser's JavaScript event loop each frame. The browser renders, handles input events, and then resumes Python.

4. **Asset packaging**: Pygbag bundles all files in your game folder into a `.data` archive that gets fetched and mounted as a virtual filesystem when the page loads.

5. **First load**: The initial load downloads ~15-20 MB (Python runtime + your game). Browsers cache this, so subsequent visits load much faster.

---

## Troubleshooting

### The build fails in GitHub Actions

- Check that **workflow permissions** are set to "Read and write" (Step 5)
- Make sure your `main.py` has `import asyncio`, `async def main()`, and `asyncio.run(main())`
- Check the Actions log for the specific error message

### The game loads but shows a black screen

- Open the browser's developer console (F12 on desktop, or use remote debugging on mobile) and look for errors
- Make sure `await asyncio.sleep(0)` is inside the `while` loop, not after it
- Ensure the `run()` method is `async def run(self)` and is called with `await`

### No sound on mobile

- Mobile browsers require a user interaction (tap) before playing audio. The game should work after the first tap
- If sound still doesn't work, check that `pygame.mixer.init()` isn't called with unsupported parameters in the web context

### The game is too small / too big on phone

- The pygbag HTML template has a canvas that can be styled. You can customize the template to make the canvas fill the screen with CSS `width: 100vw; height: 100vh;` and proper viewport meta tags
- Use `pygbag --template custom.tmpl zelda_miloutte` with a custom HTML template

### Touch controls don't work

- Make sure the touch control overlay is being drawn and is handling `pygame.FINGERDOWN` / `pygame.FINGERUP` events
- Touch coordinates from pygame are normalized (0.0 - 1.0); multiply by screen dimensions to get pixel coordinates

### gh-pages branch not appearing

- Make sure the Actions workflow completed successfully (green checkmark)
- The `gh-pages` branch is created automatically by the deploy action on first successful run

---

## Project Structure

```
zelda_miloutte/
  main.py                  # Entry point (async for web)
  game.py                  # Game loop and state stack
  settings.py              # Constants (screen size, speeds, colors)
  input_handler.py         # Keyboard + touch input
  camera.py                # Camera with lerp follow + screen shake
  hud.py                   # Hearts, keys, boss health bar
  sounds.py                # Procedurally generated SFX and music
  particles.py             # Particle effects
  transition.py            # Fade-in/fade-out transitions
  save_manager.py          # Save/load game state
  quest_manager.py         # Quest tracking
  states/                  # Game state machine
    state.py               # Abstract base state
    gameplay_state.py       # Shared gameplay logic
    play_state.py           # Overworld state
    dungeon_state.py        # Dungeon state
    title_state.py          # Title screen
    cinematic_state.py      # Intro cinematic
    pause_state.py          # Pause menu
    gameover_state.py       # Game over screen
  entities/                # Game entities
    entity.py              # Base entity class
    player.py              # Player character
    enemy.py               # Basic enemy
    archer.py              # Ranged enemy
    boss.py                # Boss enemy
    item.py                # Pickups (hearts, keys)
    chest.py               # Treasure chests
    projectile.py          # Arrows and projectiles
    sign.py                # Readable signs
    npc.py                 # Non-player characters
  world/                   # World/map system
    tile.py                # Tile types and properties
    tilemap.py             # Tile map rendering and collision
    maps.py                # Map data (2D arrays + spawn configs)
  sprites/                 # Procedural pixel art
    pixel_art.py           # Core sprite generation (ASCII grid → Surface)
    player_sprites.py      # Player animations
    enemy_sprites.py       # Enemy animations
    boss_sprites.py        # Boss animations
    archer_sprites.py      # Archer animations
    item_sprites.py        # Item sprites
    chest_sprites.py       # Chest sprites
    sign_sprites.py        # Sign sprites
    npc_sprites.py         # NPC sprites
    tile_sprites.py        # Tile sprites
    hud_sprites.py         # HUD element sprites
    effects.py             # Visual effect sprites
  ui/                      # UI components
    textbox.py             # Sign/dialogue text display
    dialogue_box.py        # NPC dialogue system
    floating_text.py       # Floating damage/XP numbers
  data/                    # Game data
    quests.py              # Quest definitions
```
