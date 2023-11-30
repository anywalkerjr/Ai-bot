import discord, requests, keras, os.path, tensorflow, PIL
import random as r
from discord.ext import commands
from settings import settings
from dicts import events_dict, tips_dict
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import model
from discord.utils import get



intents = discord.Intents.default()
intents.message_content = True
botPrefix = settings['prefix']
bot = commands.Bot(command_prefix=botPrefix, intents=intents)
path = 'images'
images_count = len([f for f in os.listdir(path)
                if os.path.isfile(os.path.join(path, f))])

@bot.event
async def on_ready():
    print(f'Вы вошли в систему как {bot.user}')

@bot.command()
async def совет(ctx):
    '''
    Выдает случайный эко-совет
    '''
    random_numbertip = r.randint(1,15)
    choosen_tip = tips_dict[f'Совет №{random_numbertip}']
    await ctx.send(f'Совет #{random_numbertip}\n{choosen_tip}')
@bot.command()
async def разложение(ctx):
    '''
    Выдает период разложения различных отходов
    '''
    await ctx.send('Период разложения отходов:\n   Органические отходы(такие как кожура банана или огрызок яблока) - 2 месяца\n    Картон - 1 месяц\n    Бумага - 1.5 месяца\n    Окурок - 5 лет\n    Ткань - 40 лет\n    Пенопласт - 50 лет\n    Резина - 40 лет\n    Фанера - 1-3 года\n    Консервная банка - 50 лет\n    Пластик - 400 лет\n    Алюминий - 500 лет\n    Стекло - тысячи лет')
@bot.command()
async def эвенты(ctx, city= commands.parameter(default='Москва',description="Фильтр событий по заданному городу"), date= commands.parameter(default=None,description="Фильтр событий по заданной дате. Формат: ДД.ММ.ГГГГ")):
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
@bot.command()
async def гриб(ctx):
    if len(ctx.message.attachments) > 0:
            attachment = ctx.message.attachments[-1]
    else:
        ctx.reply(f'{ctx.author.mention}, Вы забыли прикрепить картинку!')
    if attachment.filename.endswith(".jpg") or attachment.filename.endswith(".jpeg") or attachment.filename.endswith(".png") or attachment.filename.endswith(".webp") or attachment.filename.endswith(".gif"):
            await attachment.save(f'images/{images_count}_mushroom_{attachment.filename}.png')
            await ctx.send(f'{ctx.author.mention}, подождите 10-30 секунд!')
            detected = model.detect_image(f"images/{images_count}_mushroom_{attachment.filename}.png", 'keras_model.h5', 'labels.txt', path)
            desription = model.detect_mushrooms(detected)
            await ctx.reply(f' · Я думаю, что это гриб {detected["mushroom_name"].lower()}(Точность: {detected["score"]*100}%). \n **Съедобность**: {desription["Съедобность"]}\n **Описание**: {desription["Описание"]}')

# @bot.command()
# async def квиз(ctx):
#     member = ctx.message.author
#     role = get(member.server.roles, name="Эко-отличник")
#    await ctx.reply(f'{ctx.author.mention}, Вы решили пройти квиз по экологии. Если вы ответите на все вопросы правильно, то получите роль {role}')
#    for answers in range(0,10):
#        await ctx.reply()
    

bot.run(settings["TOKEN"])