import discord
from discord.ext import commands
import csv
import pandas as pd
from datetime import date


newCases = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/ecdc/new_cases.csv'
newDeaths = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/ecdc/new_deaths.csv'
totalCases = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/ecdc/total_cases.csv'


listOfCountries = 'Austria, Belgium, Brazil, Canada, China, France, Germany, India, Italy, Japan, Russia, Spain, Sweden, Thailand, United States, United Kingdom'

listOfCommands = '!daily: prints new cases, new deaths, and total cases worldwide \n!countries: prints all available countries \n!country [COUNTRY NAME]: prints new cases, new deaths, and total cases in the specified country'
client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    print("ready")

@client.event
async def on_message(message):
    #if message.author == client.user:
        #return
    #id = client.get_guild(225690515323092993)
    newCasesParsed = parse_csv(newCases, 'World')
    newDeathsParsed = parse_csv(newDeaths, 'World')
    totalCasesParsed = parse_csv(totalCases, 'World')
    res = '     {}: \nNew Cases: {} \nNew Deaths: {} \nTotal Cases: {}'.format( date.today(), newCasesParsed, newDeathsParsed, totalCasesParsed)

    if message.content.startswith("!daily"):
        await message.channel.send(res)
    elif message.content.startswith("!help"):
        await message.channel.send('List of commands:\n' + listOfCommands)
    elif message.content.startswith("!countries"):
        await message.channel.send(listOfCountries)
    elif message.content.startswith("!country"):
        await message.channel.send(countryStat(message.content))

def parse_csv(link, col):
    file = pd.read_csv(link)
    parsedData = file.tail(1)
    parsedData = list(set(parsedData[col]))
    parsedData = parsedData[0]
    return parsedData

def countryStat(country):
    country = country.split("!country ")
    country = country[1].capitalize()
    if country == 'United states' or country == 'Usa':
        country = 'United States'

    if country == 'United kingdom' or country == 'Uk':
        country = 'United Kingdom'
    newCasesCountry = parse_csv(newCases, country)
    newDeathsCountry = parse_csv(newDeaths, country)
    totalCasesCountry = parse_csv(totalCases, country)
    countryStats = '       {}: \nNew Cases: {} \nNewDeaths {} \nTotal Cases: {}'.format(country, newCasesCountry, newDeathsCountry, totalCasesCountry)
    return countryStats

#insert bot ID in brackets
client.run()
