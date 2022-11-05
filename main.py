import asyncio
import requests as request
import discord
from discord.ext import commands, tasks
from discord.ui import Button, View
from discord.commands import option
from discord import utils
import config
import sqlite3
import random
import string
import update

#this is the constant used as the connection to the database file named "player.db"
con = sqlite3.connect("player.db")

#Define the loop to run the auto updater



#create the database to be written to if it doesnt already exist
cur = con.cursor()


cur.execute("""
    CREATE TABLE IF NOT EXISTS smo(
        discord INTEGER NOT NULL UNIQUE,
        id INTEGER NOT NULL UNIQUE,
        name STRING NOT NULL,
        level INTEGER NOT NULL,
        avatar STRING NOT NULL,
        exp INTEGER NOT NULL,
        steps INTEGER NOT NULL,
        gold INTEGER NOT NULL,
        connection_key STRING NOT NULL,
        motto STRING NOT NULL,
        vid INTEGER NOT NULL UNIQUE,
        profile_number INTEGER NOT NULL,
        npc_kills INTEGER NOT NULL,
        user_kills INTEGER NOT NULL,
        dex INTEGER NOT NULL,
        def INTEGER NOT NULL,
        str INTEGER NOT NULL, 
        bdex INTEGER NOT NULL,
        bdef INTEGER NOT NULL,
        bstr INTEGER NOT NULL,
        max_hp INTEGER NOT NULL,
        boss_kills INTEGER NOT NULL
    )
    """)
con.commit()


intents = discord.Intents.default()
intents.members = True 

#this is my constant to have anything to deal with this bot. It is possible to have more then 1 bot in this file all run on different tokens using this method
bot = discord.Bot(debug_guild=[config.debugServer, config.debugGuild], intents=intents)





@tasks.loop(hours = 2)
async def thrloop():
    cur.execute("SELECT * FROM smo")
    h = cur.fetchall()
    top = len(h) + 1
    out = await asyncio.gather(*[update.Update(i) for i in range(1, top, 1)])
    print(out)
    embed = discord.Embed(title='User Level Updates!', colour=0xf9c605)
    channel = bot.get_guild(config.debugGuild).get_channel(1006804282567315527)
    guild = bot.get_guild(config.debugGuild)
    for q in out:
        user = q[0]
        status = q[1]
        name = q[2]
        member = guild.get_member(user)
        if status == 0:
            pass
        elif status == 1:
            role = guild.get_role(config.role200)
            await member.add_roles(role)
            embed.add_field(name=f"{name}", value="Has reached level 200", inline=False)
        elif status == 2:
            role = guild.get_role(config.role500)
            await member.add_roles(role)
            embed.add_field(name=f"{name}", value="Has reached level 500", inline=False)
        elif status == 3:
            role = guild.get_role(config.role1000)
            await member.add_roles(role)
            embed.add_field(name=f"{name}", value="Has reached level 1000", inline=False)
        elif status == 4:
            role = guild.get_role(config.role2000)
            await member.add_roles(role)
            embed.add_field(name=f"{name}", value="Has reached level 2000", inline=False)
        elif status == 5:
            role = guild.get_role(config.role5000)
            await member.add_roles(role)
            embed.add_field(name=f"{name}", value="Has reached level 5000", inline=False)
        elif status == 6:
            role = guild.get_role(config.role10000)
            await member.add_roles(role)
            embed.add_field(name=f"{name}", value="Has reached level 10000", inline=False)
        elif status == 7:
            role = guild.get_role(config.role20000)
            await member.add_roles(role)
            embed.add_field(name=f"{name}", value="Has reached level 20000", inline=False)
        elif status == 8:
            role = guild.get_role(config.role50000)
            await member.add_roles(role)
            embed.add_field(name=f"{name}", value="Has reached level 50000", inline=False)
    if len(embed.fields) == 0:
        embed.add_field(name='Better Luck Next Time', value='No one has reached a new level advancement', inline=False)
    await channel.send(embed=embed)

            
    
    

#This is the first part of the bot, the on_ready event. This is required in cases where you want assurance to connection or to start events when the bot is loaded up
@bot.event
async def on_ready():
    thrloop.start()
    print("Logged into discord Munchy")


#this is my first command. 
@bot.command(description="Ping the bot")
async def ping(ctx):
    await ctx.respond(f"The bots latency is {bot.latency}")

@bot.command(desciption="Link your discord to Simple-MMO")
async def verify(ctx, id: discord.Option(int)):
    x = request.post(f'https://api.simple-mmo.com/v1/player/info/{id}', json = config.api_key)
    data = x.json()
    cur2 = con.cursor()
    cur.execute("SELECT * FROM smo WHERE discord = ?", (ctx.author.id, ))
    q = cur.fetchone()
    cur2.execute("SELECT * FROM smo")
    z = cur2.fetchall()
    if q == None:
        user = ctx.author.id
        smoid = id
        key = ''.join(random.choices(string.ascii_lowercase, k=10))
        smoname = data['name']
        smolvl = data['level']
        smoav = data['avatar']
        smoxp = data['exp']
        smosteps = data['steps']
        gold = data['gold']
        smotto = data['motto']
        pn = data['profile_number']
        npc = data['npc_kills']
        userk = data['user_kills']
        dex = data['dex']
        strength = data['str']
        defense = data['def']
        bdex = data['bonus_dex']
        bstr = data['bonus_str']
        bdef = data['bonus_def']
        maxhp = data['max_hp']
        boss = data['boss_kills']
        dcvid = len(z) + 1
        cur.execute("INSERT INTO smo VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (user, smoid, smoname, smolvl, smoav, smoxp, smosteps, gold, key, smotto, dcvid, pn, npc, userk, dex, defense, strength, bdex, bdef, bstr, maxhp, boss,  ))
        con.commit()
        await ctx.respond(f"Please change your motto on simpleMMO to `{key}` and rerun the command to verify", ephemeral=True)
    else:
        if q[8] == 1:
            await ctx.respond("You have already verified!", ephemeral=True)
        elif q[8] == data['motto']:
            cur.execute("UPDATE smo SET connection_key = 1 WHERE vid = ?", (q[10], ))
            con.commit()
            if q[3] >= 200 and q[3] < 500:
                role = ctx.guild.get_role(config.role200)
                await ctx.guild.get_member(ctx.author.id).add_roles(role)
            elif q[3] >= 500 and q[3] < 1000:
                role = ctx.guild.get_role(config.role500)
                await ctx.guild.get_member(ctx.author.id).add_roles(role)
            elif q[3] >= 1000 and q[3] < 2000:
                role = ctx.guild.get_role(config.role1000)
                await ctx.guild.get_member(ctx.author.id).add_roles(role)
            elif q[3] >= 2000 and q[3] < 5000:
                role = ctx.guild.get_role(config.role2000)
                await ctx.guild.get_member(ctx.author.id).add_roles(role)
            elif q[3] >= 5000 and q[3 < 10000]:
                role = ctx.guild.get_role(config.role5000)
                await ctx.guild.get_member(ctx.author.id).add_roles(role)
            elif q[3] >= 10000 and q[3] < 20000:
                role = ctx.guild.get_role(config.role10000)
                await ctx.guild.get_member(ctx.author.id).add_roles(role)
            elif q[3] >= 20000 and q[3] < 50000:
                role = ctx.guild.get_role(config.role20000)
                await ctx.guild.get_member(ctx.author.id).add_roles(role)
            elif q[3] >= 50000:
                role = ctx.guild.get_role(config.role50000)
                await ctx.guild.get_member(ctx.author.id).add_roles(role)
            else:
                pass
            await ctx.respond("You have Successfully Verified!")
        else:
            await ctx.respond(f"You need to update you SimpleMMO motto to {q[8]} in order to complete verification", ephemeral=True)

@bot.command(description="A simpleMMO profile command")
async def profile(ctx, id: discord.Option(int) = None):
    if id is not None:
        x = request.post(f'https://api.simple-mmo.com/v1/player/info/{id}', json = config.api_key)
        data = x.json()
        name = data['name']
        level = data['level']
        img = data['avatar']
        motto = data['motto']
        embed = discord.Embed(title=f"{name}'s Profile", description="A very powerful player indeed!", color=0xffd700)
        embed.add_field(name="level", value=level, inline=False)
        embed.add_field(name="motto", value=motto, inline=False)
        embed.set_thumbnail(url=f"https://web.simple-mmo.com{img}")
        embed.set_footer(text=str(id))
        await ctx.respond(embed=embed)
    else:
        cur = con.cursor()
        cur.execute("SELECT * FROM smo WHERE discord = ?", (ctx.author.id, ))
        q = cur.fetchone()
        button = Button(label='Stats', style=discord.ButtonStyle.green)
        view = View()
        view.add_item(button)
        async def button_callback(interaction):
            embed2 = discord.Embed(title=f"{q[2]}'s Stat profile", colour=0xf9c605)
            embed2.add_field(name='HP:', value=f"{q[20]}", inline=False)
            embed2.add_field(name='Dex:', value=f"{q[14]}", inline=False)
            embed2.add_field(name='Def:', value=f"{q[15]}", inline=False)
            embed2.add_field(name='Str:', value=f"{q[16]}", inline=False)
            embed2.add_field(name='Bonus Dex:', value=f"{q[17]}", inline=False)
            embed2.add_field(name='Bonus Def:', value=f"{q[18]}", inline=False)
            embed2.add_field(name='Bonus Str:', value=f"{q[19]}", inline=False)
            embed2.add_field(name='NPC Kills:', value=f"{q[12]}", inline=False)
            embed2.add_field(name='User Kills:', value=f"{q[13]}", inline=False)
            embed2.add_field(name='Boss Kills:', value=f"{q[21]}", inline=False)
            embed2.set_thumbnail(url=f"https://web.simple-mmo.com{img}")
            embed2.set_footer(text=f"SMO ID:{q[1]}, Verification ID:{uvid}")
            await interaction.response.send_message(embed=embed2)
        button.callback = button_callback
        if q is None:
            await ctx.respond("Please verify or input a valid ID to continue")
        else:
            name = q[2]
            discid = q[0]
            level = q[3]
            img = q[4]
            motto = q[9]
            dcbal = q[7]
            uvid = q[10]
            embed = discord.Embed(title=f"{name}'s Profile", description="A very powerful player indeed!", color=0xffd700)
            embed.add_field(name="level:", value=level, inline=False)
            embed.add_field(name="motto:", value=motto, inline=False)
            embed.add_field(name="Gold:", value=dcbal)
            embed.add_field(name="discord ID", value=discid, inline=False)
            embed.set_thumbnail(url=f"https://web.simple-mmo.com{img}")
            embed.set_footer(text=f"SMO ID:{q[1]}, Verification ID:{uvid}")
            await ctx.respond(embed=embed, view=view)

@bot.command(description="A tool for munchy")
async def test(ctx):
    if ctx.author.id != config.admin:
        await ctx.respond('You do not have permission to do this')
    else:
        await bot.user.edit(username="Immortal Gatekeeper")
    

@bot.command(description='Update the database')
async def updates(ctx):
    if ctx.author.id != config.admin:
        await ctx.respond("You do not have permission to run this command")
    else:
        update.Update()
        await ctx.respond("done")


@bot.user_command()
async def Profile(ctx, user):
    cur.execute("SELECT * FROM smo WHERE discord = ?", (user.id, ))
    q = cur.fetchone()
    button = Button(label='Stats', style=discord.ButtonStyle.green)
    view = View()
    view.add_item(button)
    async def button_callback(interaction):
        embed2 = discord.Embed(title=f"{q[2]}'s Stat profile", colour=0xf9c605)
        embed2.add_field(name='HP:', value=f"{q[20]}", inline=False)
        embed2.add_field(name='Dex:', value=f"{q[14]}", inline=False)
        embed2.add_field(name='Def:', value=f"{q[15]}", inline=False)
        embed2.add_field(name='Str:', value=f"{q[16]}", inline=False)
        embed2.add_field(name='Bonus Dex:', value=f"{q[17]}", inline=False)
        embed2.add_field(name='Bonus Def:', value=f"{q[18]}", inline=False)
        embed2.add_field(name='Bonus Str:', value=f"{q[19]}", inline=False)
        embed2.add_field(name='NPC Kills:', value=f"{q[12]}", inline=False)
        embed2.add_field(name='User Kills:', value=f"{q[13]}", inline=False)
        embed2.add_field(name='Boss Kills:', value=f"{q[21]}", inline=False)
        embed2.set_thumbnail(url=f"https://web.simple-mmo.com{img}")
        embed2.set_footer(text=f"SMO ID:{q[1]}, Verification ID:{uvid}")
        await interaction.response.send_message(embed=embed2)
    button.callback = button_callback
    if q is None:
        await ctx.respond('This user has not verified :frown:', ephemeral=True)
    else:
        name = q[2]
        discid = q[0]
        level = q[3]
        img = q[4]
        motto = q[9]
        dcbal = q[7]
        uvid = q[10]
        embed = discord.Embed(title=f"{name}'s Profile", description="A very powerful player indeed!", color=0xffd700)
        embed.add_field(name="level:", value=level, inline=False)
        embed.add_field(name="motto:", value=motto, inline=False)
        embed.add_field(name="Coins:", value=dcbal)
        embed.add_field(name="discord ID", value=discid, inline=False)
        embed.set_thumbnail(url=f"https://web.simple-mmo.com{img}")
        embed.set_footer(text=f"SMO ID:{q[1]}, Verification ID:{uvid}")
        await ctx.respond(embed=embed, view=view)

@bot.command(description='A help command for bot commands')
async def help(ctx):
    embed = discord.Embed(title='Simple Help', colour=0xf9c605)
    embed.add_field(name='help', value='This embed!', inline=False)
    embed.add_field(name='verify[id]', value='Run verify to connect your account to SMO, ID is the id of your account')
    embed.add_field(name='profile[Optional: ID]', value='Run profile to view the profile of another user in SMO. if you input the optional ID, it is referencing a SMO id, and will display that account info', inline=False)
    await ctx.respond(embed=embed)

@bot.slash_command(description='a 2nd test command')
@option("color", str, description='pick a color for this one', autocomplete=utils.basic_autocomplete(["red", "blue", "orange", "pink"]))
async def slash_example(ctx, color:str):
    await ctx.respond(f"you have chose the color {color} {ctx.author.name}")





bot.run(config.token)