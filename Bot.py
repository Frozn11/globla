import discord
from discord.ext import commands
from setting import TOKEN,appid
import requests
import math

intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

            
class SimpleView(discord.ui.View):
    foo : bool = None
    weatherNowbool : bool = None

    async def send(self, ctx):
        self.message = await ctx.send(view=self)
        await self.update_message(self.data[:self.sep])

    async def disable_all_items(self):
            for item in self.children:
                item.disabled = True
            await self.message.edit(view=self)
    async def on_timeout(self) -> None:
            await self.message.channel.send("TimeOut")
            await self.disable_all_items()
    
    @discord.ui.button(label="Погода сейчас", 
                    style=discord.ButtonStyle.success)
    async def weathernow(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.weatherNowbool = True
        # msg = await interaction.response.send_message("https://cdn.discordapp.com/emojis/1138172643867111595.gif?size=96&quality=lossless")
        # await msg.delete()

        await weatherNow()
        await interaction.response.send_message(f"температура: {datanow['main']['temp']}° \n \t \t \t погода: {datanow['weather'][0]['description']} {word} \n \t \t \t макс.температура: {datanow['main']['temp_min']}° \n \t \t \t мини.температура: {datanow['main']['temp_max']}°")
        self.foo = True
        self.stop()
        
    @discord.ui.button(label="Погоды на 5 дней", 
                    style=discord.ButtonStyle.blurple)
    async def weatherfor5days(self, interaction: discord.Interaction, button: discord.ui.Button):
        # msg = await interaction.response.send_message("https://cdn.discordapp.com/emojis/1138172643867111595.gif?size=96&quality=lossless")    
        self.weatherNowbool = False
        global city
        city = s_city
        city_id = 0
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
            params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
        datanow = res.json()
        cities = ["{} ({})".format(d['name'], d['sys']['country'])
        for d in datanow['list']]
        print("city:", cities)
        try:
            city_id = datanow['list'][0]['id']
            city_id = city_id
            print("success")
        except:
            city_id = 524901
            print("fail")

        print('city_id=', city_id)    
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                        params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        dataweather = res.json()
        global data 
        data = []

        for i in dataweather['list']:
            data.append(f"дата/время: {i['dt_txt']} \n \t \t \t температура: {'{0:+3.0f}'.format(i['main']['temp'])}° \n \t \t \t погода: {i['weather'][0]['description']}")  
        
    
        await interaction.response.send_message("success")    
        
        self.foo = True
        self.stop()

class Pagination_View(discord.ui.View):
    current_page : int = 1
    sep : int = 5
    async def send(self, ctx):
        self.message = await ctx.send(view=self)
        await self.update_message(self.data[:self.sep])

    def create_embed(self, data):
        embed = discord.Embed(title=f"Погода на 5 дней: страница {self.current_page} / {math.ceil(len(self.data) / self.sep)}")
        for item in data:
            embed.add_field(name=item, value=item, inline=False)
        return embed
    
    async def update_message(self,data):
        self.update_buttons()
        await self.message.edit(embed=self.create_embed(data), view=self)

    def update_buttons(self):
        if self.current_page == 1:
            self.first_page_button.disabled = True
            self.prev_button.disabled = True
            self.first_page_button.style = discord.ButtonStyle.gray
            self.prev_button.style = discord.ButtonStyle.gray
        else:
            self.first_page_button.disabled = False
            self.prev_button.disabled = False
            self.first_page_button.style = discord.ButtonStyle.green
            self.prev_button.style = discord.ButtonStyle.primary

        if self.current_page == int(len(self.data) / self.sep) + 1:
            self.next_button.disabled = True
            self.last_page_button.disabled = True
            self.last_page_button.style = discord.ButtonStyle.gray
            self.next_button.style = discord.ButtonStyle.gray
        else:
            self.next_button.disabled = False
            self.last_page_button.disabled = False
            self.last_page_button.style = discord.ButtonStyle.green
            self.next_button.style = discord.ButtonStyle.primary

    def get_current_page_data(self):
        until_item = self.current_page * self.sep
        from_item = until_item - self.sep
        if not self.current_page == 1:
            from_item = 0
            until_item = self.sep
        if self.current_page == int(len(self.data) / self.sep) + 1:
            from_item = self.current_page * self.sep - self.sep
            until_item = len(self.data)
        return self.data[from_item:until_item]

            

    @discord.ui.button(label="|<",
                       style=discord.ButtonStyle.green)
    async def first_page_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page = 1

        await self.update_message(self.get_current_page_data())

    @discord.ui.button(label="<",
                       style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page -= 1
        await self.update_message(self.get_current_page_data())

    @discord.ui.button(label=">",
                       style=discord.ButtonStyle.primary)
    async def next_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page += 1
        await self.update_message(self.get_current_page_data())

    @discord.ui.button(label=">|",
                       style=discord.ButtonStyle.green)
    async def last_page_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page = math.ceil(len(self.data) / self.sep)
        await self.update_message(self.get_current_page_data())


        
async def weatherNow():
    global datanow 
    global emojes
    global word
    emojes = {
    "пасмурно": [":cloud:"],
    "ясно": [":sunny:"],
    "облачно с прояснениями": [":white_sun_cloud: "],
    "дождь": [":cloud_rain:"],
    "переменная облачность": [":white_sun_small_cloud: "]
    }
    city_id = 0
    res = requests.get("http://api.openweathermap.org/data/2.5/find",
            params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
    datanow = res.json()
    cities = ["{} ({})".format(d['name'], d['sys']['country'])
    for d in datanow['list']]
    print("city:", cities)
    try:
            city_id = datanow['list'][0]['id']
            city_id = city_id
            print("success")
    except:
        city_id = 524901
        print("fail")
    res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                    params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
    datanow = res.json()
    # print(data)
    word = datanow["weather"][0]['description']
    word = emojes.get(word, [])
    word =  "".join(word)
    if not word:
        print("no")
    print(s_city)




@bot.command()
async def weather(ctx, s_city2):
    global s_city
    s_city = s_city2
    view = SimpleView(timeout=15)
#       button = discord.ui.Button(label="Clck me")
#       view.add_item(button)
    message = await ctx.send(view=view)
    view.message = message
    await view.wait()
    await view.disable_all_items()
    if view.weatherNowbool is False:
        pagination_view = Pagination_View()
        pagination_view.data = data
        await pagination_view.send(ctx)

    if view.foo is None:
        
            print("timeOut")

    elif view.foo is True:
            print("ok")

    else:
            print("cancell")


@weather.error
async def info_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send('sorry you need to enter city name')
        
bot.run(TOKEN)