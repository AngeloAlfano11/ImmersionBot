# ImmersionBot
_**Telegram Bot for immersion in roleplay by chat**_

This project was created to enhance immersion during chat-based roleplay, using a Telegram bot that represents the player's OC (original character). Its main function is to delete the text messages sent by the player and re-send them as if they were from the bot itself, giving the impression that the OC is speaking. Replying to a message creates a link to the message being replied to.

## Bot's tools
- Using the command `/CHARACTER`, followed by some text, the bot deletes the message sent by the user and re-sends it as its own. CHARACTER is the name of the OC set in the Usage Instructions.
- Using the command `/edit`, followed by some text and in reply to a message sent by the bot, the bot edits that message with the new text provided.
- Using the command `/delete` in reply to a message sent by the bot, the bot deletes the message it is replying to.
- Using `/switchRandomizer CHARACTER`, the bot activates the randomizer function: until it is deactivated by running the same command again, all messages sent by the bot will have their text randomized. CHARACTER is the name of the OC set in the Usage Instructions.

## Usage Instructions
1. Download `BotImmersion.py` and install all of the libraries requied to run;
2. Create a bot using [BotFather](https://telegram.me/BotFather), giving it the name of your OC. Once it's created, you’ll be provided with an HTTP API token. Insert that string into the `TOKEN` variable.
(Note: the number before the colon is the BotId, which must be added to the BOTS_ID list.)
3. Retrieve the user's user_id and insert it into the `USER_ID` variable. I plan to publish the code for another bot that can do this with a simple command.
4. Retrieve the chat ID where the bot will send messages and insert it into the `ON_ROLECHAT` variable. I also plan to publish the code for the previously mentioned bot to handle this.
5. In the `BOTS_ID` variable, add an entry composed of: BotId (the number mentioned in step 2), UsernamePlayer (the player’s name. this can be anything you want) and IdPlayer (the USER_ID of the player)
6. Save the code and rename it as you like. Run it from the terminal using the command `python "BotName".py`

### Side notes
This version of the code has some issues with editing messages that have been replied to, and overall the code is not very well-written, as it was developed quickly without much oversight.
Additionally, the `BOTS_ID` variable must be kept up-to-date and consistent across all bot instances, as it is used to mention the player when replying to a message sent by the bot
