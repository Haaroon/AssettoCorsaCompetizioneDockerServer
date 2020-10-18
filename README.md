# AssettoCorsaCompetizioneDockerServer
Dockerfile to run a Assetto Corsa Competizione server

## Requires
* Assetto Corsa Competitzione server files, download them 
from steam, zip the archive and call it acc.zip, then place in this folder

* Rename `serverConfigsExample` to `serverConfigs` and edit the config files as necesary

## Discord bot

This software comes with a discord bot that can be used to 
remotely control the server. 
Create a new discord application, invite the bot to the server
with permissions to read and send messages, add the token to the 
`discord_configExample.py` then rename this file to `discord_config.py`. 
Then pip install discord.py and docker into your python3 env, 
then run `python3 discord_bot_run.py`. 

Server commands

* $status <n> -> Prints docker ps, prints last N chars of ACC Docker log, status <n>
* $start -> Starts server, runs a server, only runs one instance
* $stop  -> stops all docker containers running/servers running
* $build -> rebuilds the server with no-cache
* $changetrack <trackname> -> Changes track on server, FORMAT changetrack <track_name>. Stops server, changes track, rebuilds server and starts new instance.


