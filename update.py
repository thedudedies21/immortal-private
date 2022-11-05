import sqlite3
import time
import sys
import requests as request
import config
import discord
import asyncio
from discord.ui import Button, View
import random

rew = []


con = sqlite3.Connection("player.db")
cur = con.cursor()



async def Update(i):
    cur2 = con.cursor()
    cur2.execute("SELECT * FROM smo WHERE vid = ?", (i, ))
    q = cur2.fetchone()
    x = request.post(f"https://api.simple-mmo.com/v1/player/info/{q[1]}", json = config.api_key)
    data = x.json()
    nexp = data['exp']
    nlvl = data['level']
    nsteps = data['steps']
    nmotto = data['motto']
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
    av = data['avatar']
    gold = data['gold']
    olvl = q[3]
    output = []
    cur2.execute("UPDATE smo SET level = ?, exp = ?, steps = ?, motto = ?, npc_kills = ?, user_kills = ?, dex = ?, def = ?, str = ?, bdex = ?, bdef = ?, bstr = ?, max_hp = ?, boss_kills = ?, avatar = ?, gold = ? WHERE vid = ?", (nlvl, nexp, nsteps, nmotto, npc, userk, dex, defense, strength, bdex, bdef, bstr, maxhp, boss, av, gold, i))
    print(f"updated user {q[0]}")
    con.commit()
    if nlvl >= 200 and olvl < 200:
        output.append(q[0])
        output.append(1)
        output.append(q[2])
        await asyncio.sleep(3)
        return output
    elif nlvl >= 500 and olvl < 500:
        output.append(q[0])
        output.append(2)
        output.append(q[2])
        await asyncio.sleep(3)
        return output
    elif nlvl >=1000 and olvl < 1000:
        output.append(q[0])
        output.append(3)
        output.append(q[2])
        await asyncio.sleep(3)
        return output
    elif nlvl >=2000 and olvl < 2000:
        output.append(q[0])
        output.append(4)
        output.append(q[2])
        await asyncio.sleep(3)
        return output
    elif nlvl >=5000 and olvl < 5000:
        output.append(q[0])
        output.append(5)
        output.append(q[2])
        await asyncio.sleep(3)
        return output
    elif nlvl >=10000 and olvl < 10000:
        output.append(q[0])
        output.append(6)
        output.append(q[2])
        await asyncio.sleep(3)
        return output
    elif nlvl >=20000 and olvl < 20000:
        output.append(q[0])
        output.append(7)
        output.append(q[2])
        await asyncio.sleep(3)
        return output
    elif nlvl >=50000 and olvl < 50000:
        output.append(q[0])
        output.append(8)
        output.append(q[2])
        await asyncio.sleep(3)
        return output
    else:
        output.append(q[0])
        output.append(0)
        output.append(q[2])
        await asyncio.sleep(2)
        return output



