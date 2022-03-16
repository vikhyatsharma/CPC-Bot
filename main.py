import discord
from bot import BOT
import os
import time

client = discord.Client()
bot = BOT()

async def my_background_task():
    await client.wait_until_ready() # ensures cache is loaded
    channel = client.get_channel(id=817263418985152515)
    message = []
    while not client.is_closed():
      message = bot.list_new_contests()
      if len(message)!= 0:
        for i in range(len(message)):
          embed = message[i]
          await channel.send(embed=embed)
      time.sleep(3600)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    client.loop.create_task(my_background_task()) 

client.run("ODE3MjY0NTg2NDAyMTY4ODQy.YEG-9Q.S_pAUJmTrj5SPakDJ27c8U3NFxI")