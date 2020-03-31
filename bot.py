import discord
import requests
import json
import os
#import datetime

####################################
#with open('config.json') as f:
#  data = json.load(f)
#
#TOKEN = str(data['token'])
####################################
#Uncomment above section if using the config.json for the token

TOKEN = str(os.environ.get('TOKEN'))
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    print('Currently on: ' + str(len(list(client.guilds))) + " Guilds")
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Type '$cupdate' to get updates!"))

@client.event
async def on_message(message):
    state = str(message.content[9:])

    if message.author == client.user:
        return

    if message.content.startswith('$cupdate'):
        allData = get_data("ALL", "")

        if state != "":
            usData = get_data("STATE", state)
        else:
            usData = get_data("USA", "")

        if usData == "error":
            embed = discord.Embed(colour=discord.Colour(0xd0021b))

            embed.set_footer(text="Contact ManZ_#1234 if this error persists", icon_url="https://upload.wikimedia.org/wikipedia/commons/8/82/SARS-CoV-2_without_background.png")
            embed.add_field(name="Whoops!", value="State either does not exist or was spelt wrong!")

            await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(title="COVID-19 Stats", colour=discord.Colour(0xd0021b), url="https://www.worldometers.info/coronavirus/", description="this is the most up to date data relating to COVID-19\n\n")

            embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/8/82/SARS-CoV-2_without_background.png")
            if message.author.id == 167383539250102272:
                embed.set_footer(text="Bot created by the one who used the command 🤔")
            else:
                embed.set_footer(text="Bot created by ManZ_#1234")

            embed.add_field(name="**__Worldwide__**", value="Cases: " + str(allData['cases']) + "\n\nDeaths: " + str(allData['deaths']) + "\n\nRecovered: "  + str(allData['recovered']), inline=True)
            
            if state != "":
                embed.add_field(name="**__"+usData['state']+"__**", value="Cases: " + str(usData['cases']) + " (**Today: " + str(usData['todayCases']) + "**)\n\nDeaths: " + str(usData['deaths']) + " (**Today: " + str(usData['todayDeaths']) + "**)", inline=True)
            else:
                embed.add_field(name="**__USA__**", value="Cases: " + str(usData['cases']) + " (**Today: " + str(usData['todayCases']) + "**)\n\nDeaths: " + str(usData['deaths']) + " (**Today: " + str(usData['todayDeaths']) + "**)\n\nRecovered: " + str(usData['recovered']), inline=True)

            await message.channel.send(embed=embed)

def get_data(type, state):
    if type == "USA":
        covidApi = "https://corona.lmao.ninja/countries/usa" 
    if type == "ALL":
        covidApi = "https://corona.lmao.ninja/all" 
    if type == "STATE":
        covidApi = "https://corona.lmao.ninja/states"
        data = requests.get(covidApi)
        states = data.json()
        for i in states:
            if str(i['state']).lower() == state.lower():
                return i
        return "error"

    else:
        data = requests.get(covidApi)
        return data.json()

client.run(TOKEN)

#https://corona.lmao.ninja/countries/usa <-- Give usa data
#https://corona.lmao.ninja/all <--Gives all data
#https://corona.lmao.ninja/states <--State info

#{"cases":219265,"deaths":8968,"recovered":85745,"updated":1584592035456}
#{"country":"USA","cases":9458,"todayCases":199,"deaths":155,"todayDeaths":5,"recovered":108,"active":9195,"critical":64,"casesPerOneMillion":29}

