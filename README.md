# Sky Jumper

Sky Jumper is an exciting platformer game where players aim to jump higher and higher while collecting coins and unlocking achievements. The game features various platforms and an engaging store where players can use collected coins to buy upgrades. It's my first ever Python project.

## Game Overview

In Sky Jumper, players control a character that must jump from platform to platform, avoiding falling off the screen while collecting coins and unlocking achievements. As the game progresses, the platforms increase in speed, adding to the challenge. Players can unlock new player skins through achievements and aim to achieve the highest score, which is automatically saved to an HTML file.

## Features

- **Infinite Jumping**: The main objective is to keep jumping higher without falling.
- **Coin Collection**: Collect coins scattered across platforms to use in the in-game store.
- **Achievements**: Unlock achievements by reaching specific scores.
- **Player Skins**: Unlock new player skins by achieving certain milestones.
- **In-Game Store**: Spend your collected coins on jump boosts and extra lives.
- **High Scores**: Keep track of your best scores and aim to beat them. Scores are automatically saved to an HTML file.
- **Dynamic Camera**: The camera follows the player as they jump higher, making the gameplay more immersive.
- **Sound Effects**: Enjoy engaging sound effects for jumping, collecting coins, confirming purchases, and more.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/softchad/sky-jumper.git
   ```
2. **Navigate to the project directory**:
   ```bash
   cd sky-jumper
   ```
3. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   ```
4. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
5. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## How to Play

1. **Start the game**:
   ```bash
   python Main.py
   ```
2. **Main Menu**:
   - Use the arrow keys to navigate through the menu options.
   - Press `Enter` to select an option.
3. **Gameplay**:
   - Use the left and right arrow keys to move the character.
   - Press the spacebar to jump.
   - Collect coins and avoid falling off the screen.
   - Reach higher scores to unlock achievements and new player skins.
4. **Store**:
   - After a game over, you can enter the store to buy jump boosts and extra lives with your collected coins.
   - Use the up and down arrow keys to navigate through store options and `Enter` to confirm purchases.
5. **Settings**:
   - Adjust music and sound effects settings from the menu.

## Game Controls

- **Left Arrow**: Move left
- **Right Arrow**: Move right
- **Spacebar**: Jump
- **Up Arrow**: Use jump boost (if available)
- **Enter**: Confirm selection in menus
- **Escape**: Return to the previous menu or quit

## Achievements

- **Score 100 Points**: Unlock the first achievement.
- **Score 200 Points**: Unlock the second achievement and change player skin color.
- **Score 300 Points**: And so on up to 1500 points.

## Store Items

- **Jump Boost (5 Coins)**: Provides an extra boost for higher jumps.
- **Extra Life (10 Coins)**: Grants an extra life, allowing you to continue playing after falling off the screen.

## Saving and Loading

The game automatically saves your achievements and player data, including coins, jump boosts, and extra lives. High scores are saved in an HTML file.

## Credits

- Game developed by Vytautas Petronis.
- Supervised by Marius Gžegoževskis.
- Special thanks to Vilniaus Kolegija for the support.

Enjoy playing Sky Jumper and aim for the highest score!