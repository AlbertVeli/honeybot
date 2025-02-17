This is a simple discord chatbot that uses the discord API to interact with users. The bot is able to respond to a few commands and it is easy to implement new commands.

Here are instructions from ChatGPT about how to create a discord bot and get the token:

# Creating a Discord Bot Token

To run your bot, you need a **bot token** from Discord:

## Create a New Application
1. Open [Discord Developer Portal](https://discord.com/developers/applications) in your browser.
2. Click **"New Application"** (top-right corner).
3. Give your application a name (e.g., `"MyDiscordBot"`) and click **"Create"**.

## Create a Bot
1. In the left sidebar, go to **"Bot"**.
2. Click **"Add Bot"**, then confirm by clicking **"Yes, do it!"**.
3. (Optional) Customize your bot’s name and avatar.

## Get the Bot Token
1. In the **"Bot"** settings, click **"Reset Token"** (or **"Copy"** if it’s already visible).
2. Save the token securely. **Never share it publicly!**
3. Store this token in a `.env` file for security (see Step 7).

## Enable Message Content Intent
1. In the **"Bot"** settings, scroll down to **"Privileged Gateway Intents"**.
2. Enable **"Message Content Intent"** (this allows the bot to read messages in Discord).
3. Click **"Save Changes"** at the bottom.

## Set OAuth2 Permissions
1. In the left sidebar, go to **"OAuth2" > "URL Generator"**.
2. Under **Scopes**, select:
   - `bot`
   - `applications.commands`
3. Under **Bot Permissions**, select:
   - **Read Messages** (View Channel)
   - **Send Messages**
   - **Read Message History**
   - **Use Slash Commands** (optional)
4. Copy the generated **OAuth2 URL**.

## Invite the Bot to Your Server
1. Open the copied OAuth2 URL in your browser.
2. Select the server where you want to add the bot.
3. Click **"Authorize"** and complete the CAPTCHA.

## Securely Store Your Bot Token
1. **Never hardcode your token in your script!** Instead, create a `.env` file and store the token there.


Setting Orange, the 45th day of Chaos in the YOLD 3191

Albert Veli
