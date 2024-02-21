import discord
from discord.ext import commands
from setting import TOKEN
import utils
import requests



intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


class SimpleView(discord.ui.View):
       
        @discord.ui.button(label="обичнойе",
                        tyle=discord.ButtonStyle.success)
        async def hello(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.send_message("World")


@bot.command()
async def button(ctx):
      view = SimpleView()
      button = discord.ui.Button(label="click me")
      view.add_item(button)
      await ctx.send(view=view)

@bot.command(pass_context=True ,no_pm=True) 
async def weather(ctx, s_city):
        msg = await ctx.send("https://cdn.discordapp.com/emojis/1138172643867111595.gif?size=96&quality=lossless")
        emojes = {
              "пасмурно": [":cloud:"],
              "ясно": [":sunny:"],
              "облачно с прояснениями": [":white_sun_cloud:"],
              "дождь": [":cloud_rain:"]

        }
        appid = "4874417f6b948d6308647178a019be2d"
        city_id = 0
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
        data = res.json()
        cities = ["{} ({})".format(d['name'], d['sys']['country'])
        for d in data['list']]
        print("city:", cities)
        try:
                city_id = data['list'][0]['id']
                city_id = city_id
                print("secsei")
        except:
               city_id = 524901
               print("fail")
        print('city_id=', city_id)
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                         params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        
        data = res.json()
        # print(data)
        word = data["weather"][0]['description']
        word = emojes.get(word, [])
        word =  "".join(word)
        if not word:
              print("no")
        
        await msg.delete()
        await ctx.send(f"температура: {data['main']['temp']}° \n \t \t \t погода: {data['weather'][0]['description']} {word} \n \t \t \t макс.температура: {data['main']['temp_min']}° \n \t \t \t мини.температура: {data['main']['temp_max']}°")
        print("conditions:", data['weather'][0]['description'])
        print("temp:", data['main']['temp'])
        print("temp_min:", data['main']['temp_min'])
        print("temp_max:", data['main']['temp_max'])



# @weather.error
# async def info_error(ctx, error):
#     if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
#         await ctx.send('sorry you need to enter city name')
        
bot.run(TOKEN)