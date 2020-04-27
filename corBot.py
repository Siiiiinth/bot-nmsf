import discord
from discord.ext import commands
import csv
import pandas as pd
from datetime import date

#sID: 225690515323092993

newCases = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/ecdc/new_cases.csv'
newDeaths = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/ecdc/new_deaths.csv'
totalCases = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/ecdc/total_cases.csv'


listOfCountries = 'Austria, Belgium, Brazil, Canada, China, France, Germany, India, Italy, Japan, Russia, Spain, Sweden, Thailand, United States, United Kingdom'

listOfCommands = '!start: prints new cases, new deaths, and total cases worldwide \n!countries: prints all available countries \n!country [COUNTRY NAME]: prints new cases, new deaths, and total cases in the specified country'
client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    print("ready")

@client.event
async def on_message(message):

    #id = client.get_guild(225690515323092993)
    newCasesParsed = parse_csv(newCases)
    newDeathsParsed = parse_csv(newDeaths)
    totalCasesParsed = parse_csv(totalCases)
    res = '     {}: \nNew Cases: {} \nNew Deaths: {} \nTotal Cases: {}'.format( date.today(), newCasesParsed, newDeathsParsed, totalCasesParsed)

    if message.content == "!start":
        await message.channel.send(res)
    elif message.content == "!help":
        await message.channel.send('List of commands:\n' + listOfCommands)
    elif message.content == "!countries":
        await message.channel.send(listOfCountries)



def parse_csv(link):
    file = pd.read_csv(link)
    parsedData = file.tail(1)
    parsedData = list(set(parsedData['World']))
    parsedData = parsedData[0]
    return parsedData

client.run('NzA0MjU0NjQ2NjIwOTEzNzM0.XqaeRw.XyhEebTWDVMkIv0RycghS6N3vk8')
