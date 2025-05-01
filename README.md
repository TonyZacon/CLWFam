CLWFam/GroupAssistantBot

Introduction

This repository contains the source code for a Telegram bot that helps manage group interactions and provide useful commands for administrators and members.

Features

Welcomes new members with a personalized message.

Provides group-related information like rules and member list.

Allows administrators to manage group settings.

Offers a variety of commands to enhance group interaction.


Structure

bot.py: Main file to run the bot.

handlers/: Contains modules to handle commands and new members.

commands.py: Handles commands like /start, /help, /info, etc.

members.py: Displays information about group members.

welcome.py: Handles new member welcome messages.


utils/: Contains utility functions for handling group data and settings.

database.py: Manages saving and loading group data from a JSON file.


requirements.txt: Dependencies for the project.


Setup Instructions

1. Clone the repository:

git clone https://github.com/CLWFam/GroupAssistantBot.git
cd GroupAssistantBot


2. Install dependencies:

pip install -r requirements.txt


3. Configure the bot with your Telegram token and admin IDs.


4. Run the bot:

python bot.py



Contribution

Feel free to open issues or pull requests for any features or improvements you would like to contribute!

License

This project is licensed under the MIT License.

