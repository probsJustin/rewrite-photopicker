# Rewrite Photopicker

This is a rewrite version of my Async branch [photopicker](https://github.com/SobieskiCodes/photopicker)
Written to handle asynchronous compatible with Aiohttp requests, SQL storage, and local image caching.


## Command Changes

* Setup has been removed completely and is now done automagically.
* Adding admins is now done with mentions eg; .addadmin @ProbsJustin#0001
* removeadmin has been added
* Adding albums no longer gives a prompt, and the command has been reworked


### Commands
[]Indicates required ()Indicates Options *Is an available alias ~Requires manage guild perms or added as an admin
# Owner Commands - Not available in public bot
```
load [cog name] - Loads a cog you've uploaded, case sensitive.
unload [cog name] - Unloads a cog you have enabled, case sensitive.
reload [cog name] - Reloads a cog you've changed thats active, case sensitive.
echo (message) - Replies back in channel provided text.
vme - Displays info about the bot, version, server count, member count, uptime.
sts [message] - Changes the presence of the bot
ui [message] - Updates the <info> command text
```
# Guild Owner Commands
```
setprefix [prefix] *sp - Set the prefix for the guild, if no prefix is provided it will spit the current prefix (works with mention)
invite *inv - Send the invite link to the channel
```
# General Commands
```
album [link] [name] ~ *addalbum, aa - Add an album ex; album https://imgur.com/gallery/MnIjj3n a phone
deletealbum [name] ~ *delalbum,remalbum,da,ra - Delete an album ex; delalbum a phone
addadmin [name/mention] ~ *adda,admin - Adds an admin to the bot, can be a case sensitive name or mention
removeadmin [name/mention] ~ *remadmin,deladmin,deleteadmin - Removes and admin, same as addadmin
pickone [album] *p1,po,pick - Pick a random image from the album, if only one album it will not require an album name
albumlist *al,list - Lists all albums in the server
info - Displays custom text set by owner of the bot
```

### Requirements

```
python3.6+
imgurpython
```

And a json file under /data/config name 'startup.json'

```
{
    "config": {
        "discord_token": "Discord token here",
        "imgur_client_id": "client id here",
        "imgur_client_secret": "client secret here",
        "info": "what you want the info command to say here \n breaks are supported"
    }
}
```

**The bot needs to be started BEFORE you invite it to a server - it creates the files it needs on server join.

## Built With

* [Discord.py Rewrite](https://github.com/Rapptz/discord.py/tree/rewrite) - a modern, easy to use, feature-rich, and async ready API wrapper for Discord.

## Authors

* **Justin Sobieski** - [Sobieski.Codes](https://sobieski.codes)

## License

This project is licensed under the The Unlicense - see the [LICENSE.md](LICENSE) file for details

## Acknowledgments

* Special thanks to [stroupbslayen](https://github.com/stroupbslayen) for the snippets and constant answers for stupid questions.

