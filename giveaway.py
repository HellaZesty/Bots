import nextcord
from nextcord.ext import commands
import random
import datetime
import asyncio

intents = nextcord.Intents.all()
client = nextcord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def giveaway(ctx, prize: str, giveaway_channel_id: int, deadline: str):
    # Parse the deadline string into a datetime object
    deadline = datetime.datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S")

    # Get the channel where the giveaway will be set
    giveaway_channel = bot.get_channel(giveaway_channel_id)

    # Create the embed for the giveaway
    embed = nextcord.Embed(title=f'{prize} giveaway', description='React with 🎉 to enter the giveaway!')

    # Set the footer of the embed to show the deadline for the giveaway
    embed.set_footer(text=f'End: {deadline.strftime("%B %d, %Y at %I:%M %p")}')

    # Send the embed in the giveaway channel
    message = await giveaway_channel.send(embed=embed)

    # Add the reaction to the message
    await message.add_reaction('🎉')

    # Wait for the deadline to arrive
    await asyncio.sleep((deadline - datetime.datetime.now()).total_seconds())

    # Fetch the updated message from the giveaway channel
    message = await giveaway_channel.fetch_message(message.id)
    reactions = message.reactions
    for reaction in reactions:
        if reaction.emoji == '🎉':
            # Get the users who reacted with 🎉
            users = await reaction.users().flatten()
            # Exclude the bot from the list of users
            users = [user for user in users if not user.bot]
            if users:
                # Choose a random user from the list
                winner = random.choice(users)
                # Send the winner announcement in the giveaway channel
                await giveaway_channel.send(f'The winner is {winner.mention}! Congratulations!')
            else:
                await giveaway_channel.send('There are no eligible users on this message.')
            break
    else:
        await giveaway_channel.send('There are no reactions on this message.')

bot.run('[Token]')