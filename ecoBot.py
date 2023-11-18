import discord
import random as r
from discord.ext import commands
from settings import settings
from dicts import events_dict, tips_dict

intents = discord.Intents.default()
intents.message_content = True
botPrefix = settings['prefix']
bot = commands.Bot(command_prefix=botPrefix, intents=intents)

@bot.event
async def on_ready():
    print(f'Вы вошли в систему как {bot.user}')

@bot.command()
async def tip(ctx):
    '''
    Выдает случайный эко-совет
    '''
    random_numbertip = r.randint(1,15)
    choosen_tip = tips_dict[f'Совет №{random_numbertip}']
    await ctx.send(f'Совет #{random_numbertip}\n{choosen_tip}')
@bot.command()
async def decomposition(ctx):
    '''
    Выдает период разложения различных отходов
    '''
    await ctx.send('Период разложения отходов:\n   Органические отходы(такие как кожура банана или огрызок яблока) - 2 месяца\n    Картон - 1 месяц\n    Бумага - 1.5 месяца\n    Окурок - 5 лет\n    Ткань - 40 лет\n    Пенопласт - 50 лет\n    Резина - 40 лет\n    Фанера - 1-3 года\n    Консервная банка - 50 лет\n    Пластик - 400 лет\n    Алюминий - 500 лет\n    Стекло - тысячи лет')
@bot.command()
async def events(ctx, city= commands.parameter(default='Москва',description="Фильтр событий по заданному городу"), date= commands.parameter(default=None,description="Фильтр событий по заданной дате. Формат: ДД.ММ.ГГГГ")):
    '''
    Выдает список экомероприятий
    '''
    if city.upper() in list(events_dict.keys()):
        if date != None:
            if date in list(events_dict[city.upper()].keys()):
                date_event = (f'    {events_dict[city.upper()][date]}\n')
                await ctx.send(f'Экомероприятия в городе **{city.upper()}** на дату **{date}**:\n{date_event}')
            else:
                await ctx.send(f'На дату **{date}** экомероприятий в городе **{city.upper()}** - *нет*')
        else:
            all_events = ''
            events_city_keys = list(events_dict[city.upper()].keys())
            for i in range(len(events_city_keys)):
                all_events += (f'   {events_city_keys[i]}: {events_dict[city.upper()][events_city_keys[i]]}\n')
            await ctx.send(f'Экомероприятия в городе **{city.upper()}**:\n{all_events}')
    else:
        await ctx.send(f'Экомероприятий в городе **{city.upper()}** - *нет*')
bot.run(settings["TOKEN"])