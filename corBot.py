import discord
import csv
import pandas as pd
from datetime import date

#sID: 225690515323092993

newCases = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/ecdc/new_cases.csv'
newDeaths = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/ecdc/new_deaths.csv'
totalCases = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/ecdc/total_cases.csv'

client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    print("ready")

@client.event
async def on_message(message):

    id = client.get_guild(225690515323092993)
    newCasesParsed = parse_csv(newCases)
    newDeathsParsed = parse_csv(newDeaths)
    totalCasesParsed = parse_csv(totalCases)
    res = '     {}: \nNew Cases: {} \nNew Deaths: {} \nTotal Cases: {}'.format( date.today(), newCasesParsed, newDeathsParsed, totalCasesParsed)


    if message.content.find("!start") != -1:
        await message.channel.send(res)


def parse_csv(link):
    file = pd.read_csv(link)
    parsedData = file.tail(1)
    parsedData = list(set(parsedData['World']))
    parsedData = parsedData[0]
    return parsedData


client.run('NzA0MjU0NjQ2NjIwOTEzNzM0.XqaeRw.XyhEebTWDVMkIv0RycghS6N3vk8')
