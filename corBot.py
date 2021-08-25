import discord
from discord.ext import commands
import csv
import pandas as pd
from datetime import date
import math

fullCSV = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/owid-covid-latest.csv'

listOfCommands = '!daily: prints new cases, new deaths, and total cases worldwide \n!country [COUNTRY NAME]: prints new cases, new deaths, and total cases in the specified country, reproduction rate, vaccination status, and population'
client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    print("ready")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("!daily"):
        await message.channel.send(daily_stats())
    elif message.content.startswith("!help"):
        await message.channel.send('List of commands:\n' + listOfCommands)
    elif message.content.startswith("!country"):
        await message.channel.send(country_stats(message.content))

def daily_stats():
    df = pd.read_csv(fullCSV)
    totalCasesWorld = 0;
    newCasesWorld = 0;
    newDeathsWorld = 0;

    world = df["total_cases"]
    for x in world:
        if not math.isnan(x):
            totalCasesWorld += x
    world = df["new_cases"]
    for x in world:
        if not math.isnan(x):
            newCasesWorld += x

    world = df["new_deaths"]
    for x in world:
        if not math.isnan(x):
            newDeathsWorld += x
    res = '{}: \nNew Cases: {} \nNew Deaths: {} \nTotal Cases: {}'.format( date.today(), newCasesWorld, newDeathsWorld, totalCasesWorld)
    return res


def country_stats(country):
    country = country.split("!country ")
    country = country[1].capitalize()

    df = pd.read_csv(fullCSV)

    row = df.index[df['location']==country].tolist()
    if len(row) == 0:
        res = 'Stats for the country {} could not be found'.format(country)
        return res
    index = row[0]
    country_total = df.iat[index, 4]
    country_new = df.iat[index, 5]
    country_deaths = df.iat[index, 7]
    country_r = df.iat[index, 16]
    country_fullyvaccinated = df.iat[index, 36]
    country_pop = df.iat[index, 46]
    if not math.isnan(country_pop) and not math.isnan(country_fullyvaccinated):
        country_percentage = (country_fullyvaccinated/country_pop)*100
        res = '{}: \nTotal Cases: {} \nNew Cases Today: {} \nTotal Deaths: {} \nReproduction Rate: {} \nFully Vaccinated: {} \nPopulation: {} \nVaccination Rate: {:.2f}%'.format( date.today(), country_total, country_new, country_deaths,country_r,country_fullyvaccinated,country_pop, country_percentage)
        return res


    res = '{}: \nTotal Cases: {} \nNew Cases Today: {} \nTotal Deaths: {} \nReproduction Rate: {} \nFully Vaccinated: {} \nPopulation: {}'.format( date.today(), country_total, country_new, country_deaths,country_r,country_fullyvaccinated,country_pop)
    return res


#insert bot ID here
client.run()

