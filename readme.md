# Discord Bot

This is a simple Discord bot base for you to build off of and expand into something big with ease

## Setup

1. Clone this repository to your local machine.
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Fill in the necessary data in `config.yml`:
   ```yaml
   token: YOUR_BOT_TOKEN
   Db: this isnt implemented yet but is very easy to do so your self. (I might add this with addition of other commands?)
   ```

## Usage

1. Make sure you've completed the setup steps above.
2. Run the bot by executing:
   ```
   python main.py
   ```
3. Your done!

## Features

- Free AI Image generator and TTS from elevenlabs
- Easy to build off of
- Organized
- Custom rate limit wraper for 'groups', limits how many times any such command in a group can be run in a duration (wrapper applied manually)

## Commands

- `/generate-image`: Generatea an AI image with any prompt, proxies arent needed for this command.
- `/generate-tts`: Generate TTS with Elevenlabs (proxies recommended for this to work well)

## Troubleshooting

If you encounter any issues, please check the following:

1. Ensure your `config.yml` file is correctly formatted and contains all necessary information.
2. Verify that your bot token is correct and has not expired.
3. Check that you have the required permissions in the Discord server.

## Contributing

- Make a pull request 🔥

## License

Open for all skids 💖

## Note
- Join https://discord.shard-ai.xyz to get many free AI models like elevenlabs, gpt, claude, and much more without having to pay and easier to maintain 🔥
