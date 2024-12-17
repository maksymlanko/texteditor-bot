import discord
from discord.ext import commands
import subprocess
import os

# Get the token from the environment
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if not TOKEN:
    raise ValueError("⚠️ Bot token not found. Set the DISCORD_BOT_TOKEN environment variable.")

# Enable intents
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent

# Create bot instance with intents
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignore messages from the bot itself

    if "sus" in message.content.lower():
        await message.channel.send("very sus!")

    await bot.process_commands(message)

# Command: Append message to a file
@bot.command()
async def append(ctx, *, user_message: str):
    """
    Appends a user's message to a file called 'output.txt'.
    Usage: !append your message here
    """
    try:
        with open("output.txt", "a") as file:
            file.write(user_message + "\n")
        await ctx.send("✅ Message appended to file!")
    except Exception as e:
        await ctx.send(f"❌ An error occurred: {e}")

# Command: Run 'output.txt' as a Python script and print the result
@bot.command()
async def runfile(ctx):
    """
    Runs the 'output.txt' file as a Python script and prints the output.
    Usage: !runfile
    """
    try:
        # Run 'python output.txt' and capture the output
        result = subprocess.run(
            ["python", "output.txt"], capture_output=True, text=True, timeout=5
        )

        # Send the output (stdout or stderr) back to Discord
        output = result.stdout if result.stdout else result.stderr
        if not output:
            output = "✅ Script ran successfully, but there was no output."

        # Send response
        await ctx.send(f"**Output:**\n```\n{output}\n```")
    except subprocess.TimeoutExpired:
        await ctx.send("❌ Script execution timed out.")
    except Exception as e:
        await ctx.send(f"❌ An error occurred: {e}")

# Command: Delete file
@bot.command()
async def deletefile(ctx):
    """
    Cleans the contents of 'output.txt'
    Usage: !deletefile
    """
    try:
        with open("output.txt", "w") as file:
            file.truncate(0)  # Clear the file by truncating it to 0 bytes
        await ctx.send("🧹 `output.txt` has been cleared.")
    except Exception as e:
        await ctx.send(f"❌ An error occurred while clearing the file: {e}")

# Command: Open and print file
@bot.command()
async def printfile(ctx):
    """
    Prints the contents of the file
    Usage: !printfile
    """
    try:
        # Try to read the file
        with open("output.txt", "r") as file:
            contents = file.read().strip()
        
        # Send the contents of the file
        if contents:
            await ctx.send(f"**File Contents:**\n```\n{contents}\n```")
        else:
            await ctx.send("📂 `output.txt` is currently empty.")
    
    except FileNotFoundError:
        await ctx.send("⚠️ `output.txt` not found.")
    
    except Exception as e:
        await ctx.send(f"❌ An error occurred while reading the file: {e}")


bot.run(TOKEN)

