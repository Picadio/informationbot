import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
import psycopg2
import os
db_url = str(os.environ.get("DATABASE_URL"))
db_url=db_url.replace("postgres://", "")
x=db_url.split(":")
db_user=x[0]
db_password=x[1].split("@")[0]
db_host=x[1].split("@")[1]
db_name=x[2].split("/")[1]
Bot = commands.Bot(command_prefix='.')
@Bot.event
async def on_ready():
    print("Bot is online")
@Bot.command(pass_context=True)
async def info(ctx, user:discord.Member):
    conn = psycopg2.connect(dbname=db_name, user=db_user, 
                       password=db_password, host=db_host)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM info')
    row = cursor.fetchone()
    q=bool(0)
    while row is not None:
        if user.id in row:
            q=bool(1)
            break
        row = cursor.fetchone()
    if q==0:
        cursor.execute('''INSERT INTO info (id,likee,dislike,des,vpl,vx,va) VALUES ({0},0, 0, 'None', '❌', '❌', '❌')'''.format(user.id) )
        conn.commit()
    cursor.close()
    conn.close()

    emb=discord.Embed( colour= 0x39d0d6)
    emb.set_author(icon_url =user.avatar_url, name=user.name)
    emb.add_field(name="Like 👍", value=row[1])
    emb.add_field(name="Dislike 👎", value=row[2])
    pol = 0
    print(user.roles)
    role = get(ctx.guild.roles, name="Доступ")
    await user.add_roles(role)
    if get(user.roles, name="Парень"):
        emb.add_field(name="Пол 🚻", value="♂")
    elif get(user.roles, name="Девушка"):
        emb.add_field(name="Пол 🚻", value="♀")
    else:
        emb.add_field(name="Пол 🚻", value=None)
        
        

    emb.add_field(name="Присоединился 📅", value=user.joined_at.strftime("%d.%m.%Y @ %H:%M:%S %p"))

    emb.add_field(name="О себе", value=row[3], inline=False)

    if row[4] == "✅" and row[5] == "✅" and row[6] == "✅":
        emb.add_field(name="Full Verification", value="✅", inline=False)
    else:
        emb.add_field(name="Full Verification", value="❌", inline=False)
    
    emb.add_field(name="Игроки", value=row[4])
    emb.add_field(name="Хелпер", value=row[5])
    emb.add_field(name="Админ", value=row[6])
    emb.set_thumbnail(url=user.avatar_url)


    emb.set_footer(text="Вызвано: {}".format(ctx.message.author.name),icon_url=ctx.message.author.avatar_url)
    await ctx.message.channel.send(embed=emb)

       
    

@Bot.command(pass_context=True)
async def set_description(ctx, s):
    conn = psycopg2.connect(dbname=db_name, user=db_user, 
                       password=db_password, host=db_host)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM info')
    row = cursor.fetchone()

    q=bool(0)
    while row is not None:
        if ctx.message.author.id in row:
            q=bool(1)
            break
        row = cursor.fetchone()
    if q==0:
        cursor.execute('''INSERT INTO info (id,likee,dislike,des,vpl,vx,va) VALUES ({0},0, 0, "None", "❌", "❌", "❌")'''.format(ctx.message.author.id) )
        conn.commit()  
    cursor.close()
    conn.close()

    conn = sqlite3.connect("mybase.sqlite")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM info')

    
    cursor.execute('''UPDATE info SET des=? WHERE id=?''',(s,ctx.message.author.id))
    conn.commit()
    await ctx.message.channel.send("Описание было успешно изменено")     
       
    cursor.close()
    conn.close()
    
@Bot.command(pass_context=True)
async def like(ctx, user:discord.Member):
    conn = psycopg2.connect(dbname=db_name, user=db_user, 
                       password=db_password, host=db_host)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM info')
    row = cursor.fetchone()

    q=bool(0)
    while row is not None:
        if user.id in row:
            q=bool(1)
            break
        row = cursor.fetchone()
    if q==0:
        cursor.execute('''INSERT INTO info (id,likee,dislike,des,vpl,vx,va) VALUES ({0},0, 0, "None", "❌", "❌", "❌")'''.format(user.id) )
        conn.commit()  
    cursor.close()
    conn.close()
    conn = sqlite3.connect("mybase.sqlite")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM info')
    
    
    a=row[1]+1
    if a>=20:
        cursor.execute('''UPDATE info SET vpl=? WHERE id=?''',("✅",user.id))
    cursor.execute('''UPDATE info SET likee={0} WHERE id={1}'''.format(a,user.id))
    conn.commit()
    await ctx.message.channel.send("Вы поставили Like "+user.name)       
       
    cursor.close()
    conn.close()

@Bot.command(pass_context=True)
async def dislike(ctx, user:discord.Member):
    conn = psycopg2.connect(dbname=db_name, user=db_user, 
                       password=db_password, host=db_host)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM info')
    row = cursor.fetchone()

    q=bool(0)
    while row is not None:
        if user.id in row:
            q=bool(1)
            break
        row = cursor.fetchone()
    if q==0:
        cursor.execute('''INSERT INTO info (id,likee,dislike,des,vpl,vx,va) VALUES ({0},0, 0, "None", "❌", "❌", "❌")'''.format(user.id) )
        conn.commit()
    cursor.close()
    conn.close()
    conn = sqlite3.connect("mybase.sqlite")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM info')
   
    a=row[2]+1
    cursor.execute('''UPDATE info SET dislike={0} WHERE id={1}'''.format(a,user.id))
    conn.commit()
    await ctx.message.channel.send("Вы поставили Dislike "+user.name)         
    
    cursor.close()
    conn.close()

@Bot.command(pass_context=True)
async def crtable(ctx):
    
   
    conn = psycopg2.connect(dbname=db_name, user=db_user, 
                       password=db_password, host=db_host)
    
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE info (id bigint, likee integer, dislike integer, des text, vpl bool, vx bool, va bool)''')
    print("Sucessful")
    cursor.close()
    conn.close()

Bot.run(str(os.environ.get("Token")))
