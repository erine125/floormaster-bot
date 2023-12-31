import discord
from discord.ext import commands
import random
from datetime import timedelta
from asyncio import sleep
import datetime

description = '''this is the FloormasterBot'''
bot = commands.Bot(command_prefix='?', description=description)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("FloormasterBot is online! Check #organization-database for bot commands!"))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


class Player:
    def __init__(self, user):
        self.user = user
        self.username = user.name
        self.userid = user.discriminator
        self.gameRole = None
        self.votes = 0
    def setGameRole(self, gameRole):
        self.gameRole = gameRole
    def getGameRole(self):
        return self.gameRole
    def voteFor(self):
        self.votes += 1
    def getVotes(self):
        return self.votes
    def setVotes(self, num):
        self.votes = num

@bot.command()
async def getHelp(ctx):
    server = ctx.guild
    for member in server.members:
        for role in member.roles:
            if role.name == "god":
                god = role


    msg = "**?getHelp** - lists commands\n\
**?start** - prints welcome message and pings participants\n\
**?assignRoles** - randomizes roles and sends DMs to participants with their roles\n\
**?showPlayers** - prints out all the current players and their discord codes!\n\
**?revealRoles** - prints out who is keymaster, sage, and sacrifice. obviously, DO NOT call this during a game\n\
**?vote <userid>** - send in DM to the bot to vote for a player (enter their discord code without the hashtag)\n\
**?showVotes** - prints out current number of votes per person\n\
**?resetVotes** - only use in case people accidentally vote more than once or there are issues. resets all vote numbers to 0\n\
**?finalVote** - moves us into the final vote and prints out list of candidates\n\
Shoot a message to {0.mention} if you have questions about the bot!".format(god)
    await ctx.send(msg)

@bot.command()
async def start(ctx):
    for member in ctx.guild.members:
        for role in member.roles:
            if role.name == "participant":
                participant_role = role
    msg = ""
    msg += "{0.mention}\n".format(participant_role)
    msg += "**Welcome to the Main Game!**\n"
    msg += "Please read the rules channel!\n"
    msg += "Type __?getHelp__ to access list of bot commands\n"
    msg += "Type __?assignRoles__ when you are ready to start!"
    await ctx.send(msg)

@bot.command()
async def checkRole(ctx):
    try:
        for player in players:
            if player.getGameRole()== "keymaster":
                keymaster = player
            elif player.getGameRole() == "sage":
                sage = player
            elif player.getGameRole() == "sacrifice":
                sacrifice = player
        if ctx.author == keymaster.user:
            await ctx.send("Your role: **keymaster**")
        elif ctx.author == sage.user:
            await cttx.send("Your role: **sage**")
        elif ctx.author == sacrifice.user:
            await ctx.send("Your role: **sacrifice**")
        else:
            await ctx.send("Your role: **commoner**")

    except:
        await ctx.send("Error - Roles not yet assigned")

@bot.command()
async def revealRoles(ctx):
    try:
        msg = ""
        for member in players:
            if member.getGameRole() == "keymaster":
                msg += "**keymaster:** {}\n".format(member.user.name)
            elif member.getGameRole() == "sage":
                msg += "**sage:** {}\n".format(member.user.name)
            elif member.getGameRole() == "sacrifice":
                msg += "**sarifice:** {}\n".format(member.user.name)
        await ctx.send(msg)

    except:
        await ctx.send("Roles have not been assigned yet!")

@bot.command()
async def resetVotes(ctx):
    try:
        for player in players:
            player.setVotes(0)
        await ctx.send("Votes have been reset for all participants")
        return
    except:
        await ctx.send("Error - Roles have not been assigned yet")
        return


@bot.command()
async def vote(ctx, userid):



    try:
        voted = None
        for player in players:
            if player.user.discriminator == userid:
                player.voteFor()
                voted = player.user
    except:
        await ctx.send("Error - roles have not bee assigned yet")
        return

    try:
        for candidate in candidates:
            if candidate.user.discriminator == userid:
                candidate.voteFor()
                voted = candidate.user
    except:
        pass

    if voted==None:
        await ctx.send("Not a valid user ID of a player you can vote for")
        return

    await ctx.send("You have successfully voted for " + str(voted))

@bot.command()
async def finalVote(ctx):
    for player in players:
        player.setVotes(0)

    global candidates
    candidates = []
    server = ctx.guild
    for member in server.members:
        for role in member.roles:
            if role.name == "candidate":
                candidate = Player(member)
                candidates.append(candidate)

    msg = ""
    for candidate in candidates:
        msg += str(candidate.user.name) + "\n"
    await ctx.send("**Candidates**\n"+msg)


@bot.command()
async def showVotes(ctx):

    try:
        msg = "**Final vote!**\n"
        random.shuffle(candidates)
        for member in candidates:
            msg += str(member.user) + " has " + str(member.getVotes()) + " votes \n"
        await ctx.send(msg)
    except:
        msg = "**Preliminary vote!**\n"
        random.shuffle(players)

        for member in players:
            msg += str(member.user) + " has " + str(member.getVotes()) + " votes \n"
        await ctx.send(msg)


@bot.command()
async def showPlayers(ctx):
    try:
        msg = "**Current Players**\n"
        for player in players:
            if player.user.nick != None:
                msg += "{0} — {1}\n".format(str(player.user), player.user.nick)
            else:
                msg += "{0} — {1}\n".format(str(player.user), player.user.name)
        await ctx.send(msg)
    except:
        await ctx.send("Error - game has not started")



@bot.command()
async def assignRoles(ctx):
    global participants
    participants = []
    server = ctx.guild
    for member in server.members:
        for role in member.roles:
            if role.name == "participant":
                participant_role = role
                player = Player(member)
                participants.append(player)

    if len(participants) == 0:
        await ctx.send("not enough participants")
        return

    global players
    players = []

    keymaster = random.choice(participants)
    keymaster.setGameRole("keymaster")
    participants.remove(keymaster)
    players.append(keymaster)


    if len(participants) == 0:
        await ctx.send("not enough participants")
        return

    sage = random.choice(participants)
    sage.setGameRole("sage")
    participants.remove(sage)
    players.append(sage)



    if len(participants) == 0:
        await ctx.send("not enough participants")
        return

    sacrifice = random.choice(participants)
    sacrifice.setGameRole("sacrifice")
    participants.remove(sacrifice)
    players.append(sacrifice)

    commoners = participants
    for player in commoners:
        player.setGameRole("commoner")
        players.append(player)


async def timer(td:timedelta):
    minutes, seconds = divmod(int(td.total_seconds()), 60)
    hours, minutes = divmod(minutes, 60)
    days , hours = divmod(hours, 24)
    res = f"{minutes:>02}:{seconds:>02}"
    if hours or days:
        res = f"{hours:>02}:" + res
    if days:
        res =  f"{td.days} days, " + res
    return res

@bot.command()
async def countdown(ctx, seconds: int):
    td = timedelta(seconds=seconds)
    while True:
        await bot.say(time_repr(td))
        if td.total_seconds() > 30:
            td -= timedelta(seconds=30)
            await sleep(30)
        elif td.total_seconds > 10:
            td -= timedelta(seconds=10)
            await sleep(10)
        elif td.total_seconds > 1:
            td -= timedelta(seconds=1)
            await sleep(1)
        else:
            break

@bot.command()
async def quit(ctx):
    await ctx.send("Thanks for playing!")
    exit()

class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


