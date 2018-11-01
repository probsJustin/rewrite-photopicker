from cogs.util import pyson
from discord.ext import commands
from imgurpython import ImgurClient
from cogs.util.errorhandling import NotAuthorized
import random
import discord
import io


def is_admin():
    '''Checks if the message author is the owner or has admin perms'''
    def predicate(ctx):
        if ctx.author.id == ctx.message.guild.owner.id or ctx.author.guild_permissions.manage_guild:
            return True

        if ctx.author.id in pyson.Pyson(f'data/servers/{str(ctx.guild.id)}/config.json').data.get('config').get('admins'):
            return True

        else:
            raise NotAuthorized
    return commands.check(predicate)


class imgur:
    def __init__(self, bot):
        self.bot = bot
        self.clientID = bot.config.data.get('config').get('imgur_client_id')
        self.secretID = bot.config.data.get('config').get('imgur_client_secret')
        self.imgur_client = ImgurClient(self.clientID, self.secretID)

    @is_admin()
    @commands.command(aliases=['addalbum', 'aa'])
    async def album(self, ctx, link: str=None, *, album_name: str=None):
        '''addalbum [album link] [album name] - Adds an album, link, and name.
        ex; .addalbum https://imgur.com/gallery/MnIjj3n a phone
        and 'pickone a phone' would call this album.
        '''
        if not link or not album_name:
            await ctx.send('Please include a link to the album and a name for the album.')
            return

        possible_links = ['https://imgur.com/gallery/', 'https://imgur.com/a/'] #leaving this for additions later
        if not any(x in link for x in possible_links):
            await ctx.send('That doesnt look like a valid link.')

        else:
            album_name = album_name.lower()
            self.bot.serverconfig = pyson.Pyson(f'data/servers/{str(ctx.guild.id)}/config.json')
            if album_name not in self.bot.serverconfig.data.get('albums'):
                self.bot.serverconfig.data['albums'][album_name] = link
                self.bot.serverconfig.save()
                await ctx.send(f'"{album_name}" has been added!')
            else:
                await ctx.send(f'"{album_name}" already exists.')

    @is_admin()
    @commands.command(aliases=['delalbum', 'remalbum', 'da', 'ra'])
    async def deletealbum(self, ctx, *, album_name: str=None):
        '''deletealbum [album name] - Deletes an album, name.
        ex; .deletealbum a phone
        '''
        if not album_name:
            await ctx.send('Please provide an album name.')

        if album_name.lower() in self.bot.serverconfig.data.get('albums'):
            self.bot.serverconfig.data['albums'].pop(album_name, None)
            self.bot.serverconfig.save()
            await ctx.send(f'Removed album "{album_name}"')

        else:
            await ctx.send(f'Couldnt find an album the name of "{album_name}"')

    @commands.command(aliases=['p1', 'po', 'pick'])
    async def pickone(self, ctx, *, album_name: str=None):
        '''pickone (Optional album name) - picks a random image from the album.
        ex; .pickone a phone
        If only one album exists you do not provide an album name.
        '''
        if len(self.bot.serverconfig.data.get('albums')) is 0:
            await ctx.send('You should probably add an album first..')
            return

        if not album_name:
            if len(self.bot.serverconfig.data.get('albums')) >= 2:
                await ctx.send('Seems you forgot to provide an album name!')
                return

            elif len(self.bot.serverconfig.data.get('albums')) == 1: #will swap this to local storage soon.
                await ctx.message.add_reaction(discord.utils.get(self.bot.emojis, name='check'))
                tail = list(self.bot.serverconfig.data.get('albums').values())[0].split('/')[4]
                the_list = list(item.link for item in self.imgur_client.get_album_images(tail))
                async with self.bot.aiohttp.get(random.choice(the_list)) as resp:
                    link = await resp.read()
                    f = discord.File(io.BytesIO(link), filename="image.png")
                    e = discord.Embed(title="I Chose..", colour=discord.Colour(0x278d89), )
                    e.set_image(url=f'''attachment://image.png''')
                    await ctx.send(file=f, embed=e, content='You asked me to pick a picture...')

            elif not self.bot.serverconfig.data.get('albums'):
                await ctx.send('It doesnt seem that you have added an ablum.')

        if album_name in self.bot.serverconfig.data.get('albums'):
            await ctx.message.add_reaction(discord.utils.get(self.bot.emojis, name='check'))
            tail = self.bot.serverconfig.data.get('albums').get(album_name).split('/')[4]
            the_list = list(item.link for item in self.imgur_client.get_album_images(tail))
            async with self.bot.aiohttp.get(random.choice(the_list)) as resp:
                link = await resp.read()
                f = discord.File(io.BytesIO(link), filename="image.png")
                e = discord.Embed(title="I Chose..", colour=discord.Colour(0x278d89), )
                e.set_image(url=f'''attachment://image.png''')
                await ctx.send(file=f, embed=e, content='You asked me to pick a picture...')

        elif not album_name and len(self.bot.serverconfig.data.get('albums')) >= 2:
            await ctx.send(f'I couldnt find an album by the name of "{album_name}"')

    @commands.command(aliases=['al', 'list'])
    async def albumlist(self, ctx):
        '''albumlist - displays all currently added albums by name.
        '''
        if len(self.bot.serverconfig.data.get('albums')) is not 0:
            await ctx.send(f"The list of albums I see are: {', '.join(list(self.bot.serverconfig.data.get('albums')))}.")

        else:
            await ctx.send('It doesnt seem that you have added an ablum.')

    @is_admin()
    @commands.command(aliases=['adda', 'admin'])
    async def addadmin(self, ctx, member: discord.Member = None):
        '''addadmin [user name] - Adds an admin
        ex; .addadmin @ProbsJustin#0001
        You can attempt to use just a string name; eg ProbsJustin but recommend a mention.
        '''
        if not member:
            await ctx.send('You should probably include a member.')
            return
        else:
            if not member.id in self.bot.serverconfig.data.get('config').get('admins'):
                self.bot.serverconfig.data['config']['admins'].append(member.id)
                self.bot.serverconfig.save()
                await ctx.send(f'{member.mention} has been added as an admin.')
            else:
                await ctx.send('That user is already an admin!')

    @is_admin()
    @commands.command(aliases=['remadmin', 'deladmin', 'deleteadmin'])
    async def removeadmin(self, ctx, member: discord.Member = None):
        '''removeadmin [user name] - Remove an admin
        ex; .removeadmin @ProbsJustin#0001
        You can attempt to use just a string name; eg ProbsJustin but recommend a mention.
        '''
        if not member:
            await ctx.send('You should probably include a member.')
            return
        else:
            if member.id in self.bot.serverconfig.data.get('config').get('admins'):
                self.bot.serverconfig.data['config']['admins'].remove(member.id)
                self.bot.serverconfig.save()
                await ctx.send(f'{member.mention} has been removed as an admin.')
            else:
                await ctx.send('I couldnt find that user in the admin list.')

    @addadmin.error
    @removeadmin.error
    async def member_not_found_error(self, ctx, exception): #so this is a thing.
        if not isinstance(exception, NotAuthorized):
            await ctx.send('Member not found! Try mentioning them instead.')


def setup(bot):
    bot.add_cog(imgur(bot))
