import discord
import os
import asyncio
import yt_dlp
import apikeys as APPKEYS
from discord.ext import commands
from dotenv import load_dotenv
import urllib.parse, urllib.request, re
from discord import AudioSource as aus

load_dotenv()

intents = discord.Intents.all()
intents.members = True
intents.message_content = True

load_dotenv()
TOKEN = APPKEYS.SPOTTER
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)

meep = []
song = []
queues = {}
voice_clients = {}
youtube_base_url = 'https://www.youtube.com/'
youtube_results_url = youtube_base_url + 'results?'
youtube_watch_url = youtube_base_url + 'watch?v='
yt_dl_options = {"format": "bestaudio/best"}
ytdl = yt_dlp.YoutubeDL(yt_dl_options)
number_songs = 0

ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn -filter:a "volume=0.25"'}

@client.event
async def on_ready():
    print("Ready Status: Ok")

async def play_next(ctx):

    if queues[ctx.guild.id] != []:
        link = queues[ctx.guild.id].pop(0)
        await play(ctx, link=link)
    if meep != []:
        link = meep.pop(0)
        await play(ctx, link=link)

# Creating a command for the bot to play audio

@client.command(name="play")
async def play(ctx, *, link):
        try:
            voice_client = await ctx.author.voice.channel.connect()
            voice_clients[voice_client.guild.id] = voice_client
        except Exception as e:
            print(e)

        try:

            if youtube_base_url not in link:
                query_string = urllib.parse.urlencode({
                    'search_query': link
                })

                content = urllib.request.urlopen(
                    youtube_results_url + query_string
                )

                search_results = re.findall(r'/watch\?v=(.{11})', content.read().decode())

                link = youtube_watch_url + search_results[0]

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(link, download=False))

            song = data['url']
            player = discord.FFmpegOpusAudio(song, **ffmpeg_options)

            voice_clients[ctx.guild.id].play(player, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), client.loop))

            print(song)
        except Exception as e:
            print(e)

#Testing command to implement playlist reproduction to spotter

@client.command(name="playp")
async def playp(ctx, *, link):
        
        #Calling global variables for other commands to manage the same data
        
        global meep
        global song

        #Connecting to the voice channel and retrieving the required data (link)
        try:
            voice_client = await ctx.author.voice.channel.connect()
            voice_clients[voice_client.guild.id] = voice_client
        except Exception as e:
            print(e)

        #Filtering to determine the data collected (video tittle, video link or playlist link)
        try:
            if youtube_base_url not in link:

                #Searching video by tittle name and retrieving it's link
                query_string = urllib.parse.urlencode({
                    'search_query': link
                })
                content = urllib.request.urlopen(
                    youtube_results_url + query_string
                )
                search_results = re.findall(r'/watch\?v=(.{11})', content.read().decode())
                link = youtube_watch_url + search_results[0]

            elif "list" in link:

                #Attempting to obtain a list of url links to each individual video inside the playlist
                meep = ytdl._playlist_infodict.__get__.__str__()
                print(meep)
            else:

                #Playing the determined link
                loop = asyncio.get_event_loop()
                data = await loop.run_in_executor(None, lambda: ytdl.extract_info(link, download=False))

                song = data['url']
            player = discord.FFmpegOpusAudio(song, **ffmpeg_options)
            voice_clients[ctx.guild.id].play(player, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), client.loop))

        except Exception as e:
            print(e)

#Creating a command for pausing audio

@client.command(pass_context = True)
async def pause(ctx):

    #Obtaining current song being played

    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)

    #Verifying if a song is being played

    if (ctx.voice_client):
        if (voice.is_playing()):
            try:
                voice_clients[ctx.guild.id].pause()
            except Exception as e:
                print(e)
        else: 
            await ctx.send("There is no audio playing at the moment.")
    else:
        await ctx.send("Spotter is not in any voice chat at the moment.")

#Creating a command for resuming the audio after a pause.

@client.command(pass_context = True)
async def resume(ctx):

    #Obtaining current song being played

    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)

    #Verifying audio status

    if (ctx.voice_client):
        if (voice.is_paused()):
            try:
                voice_clients[ctx.guild.id].resume()
            except Exception as e:
                print(e)
        else: 
            await ctx.send("There is no audio paused at the moment.")
    else:
        await ctx.send("Spotter is not in any voice chat at the moment.")

#Creating a command for stopping the bot completely

@client.command(name="stop")
async def stop(ctx):
    try:
        voice_clients[ctx.guild.id].stop()
        await voice_clients[ctx.guild.id].disconnect()
        del voice_clients[ctx.guild.id]
    except Exception as e:
        print(e)
    
#Creating a command for Queue's

@client.command(name="queue")
async def queue(ctx, *, url):

    if ctx.guild.id not in queues:
        queues[ctx.guild.id] = []
    queues[ctx.guild.id].append(url)
    await ctx.send("Added to queue!")

#Creating a command for skipping a song in the Queue

@client.command(name="skip")
async def skip(ctx):

    if queues[ctx.guild.id] != []:
        voice_clients[ctx.guild.id].pause()
        link = queues[ctx.guild.id].pop(0)
        await play(ctx, link=link)
    else:
        ctx.send("There are no songs in the queue.")

#Creating a command to print the list currently in queue

@client.command(name="queuelist")
async def queuelist(ctx):

    number_songs = len(queues[ctx.guild.id])

    if number_songs == 0:
        await ctx.send("There are currently no songs in queue.")
    else:
        for n in range(number_songs): 
            songlink = str(queues[ctx.guild.id][n])
            nt = str(n+1)
            await ctx.send(nt+". "+songlink)

client.run(APPKEYS.SPOTTER)
