from discord.ext import commands
import docker
import subprocess
import json
from discord_config import TOKEN

bot = commands.Bot(command_prefix="$")

# docker client
docker_client = docker.from_env()

@bot.command(
    name='status',
    help='Prints docker ps, prints last N chars of ACC Docker log, status <n>'
)
async def status(ctx, log_char=500):
    cont_list=docker_client.containers.list()
    if len(cont_list)==0:
        await ctx.channel.send('No containers running')
        return
    log_char = -1*log_char
    logs = str([_ for _ in cont_list[0].logs()[log_char:].decode('utf8').splitlines() if _ != ''])
    response = str(len(cont_list))+' server(s) online. ->'+str(cont_list[0].image)+logs
    await ctx.channel.send(response)


@bot.command(
    name='start',
    help='Starts server'
)
async def start(ctx):
    if len(docker_client.containers.list())>0:
        response = 'Cannot start new docker container, one already running'
        await ctx.channel.send(response)
        return
    proc=subprocess.run(['docker', 'create', '-p', '0.0.0.0:9231:9231/udp', '-p','0.0.0.0:9232:9232/tcp', '-t', '-i', 'accserver', '/bin/bash', 'wine', '/root/acc/server/accServer.exe'], capture_output=True)
    proc_id = proc.stdout.decode()[:-1]
    subprocess.run(['docker', 'start', proc_id])
    await ctx.channel.send('Run via subprocess '+str(proc_id))
    #try:
        #created = docker_client.containers.create('accserver', ports={'9231/udp':('0.0.0.0',9231),'9232/tcp':('0.0.0.0',9232)})
        #docker_client.containers.run
        #await ctx.channel.send('Run server, please wait 2 minutes, use $status to check')
    #except docker.errors.ContainerError:
    #    await ctx.channel.send('Exception docker.errors.ContainerError')
    #except docker.errors.ImageNotFound:
    #    await ctx.channel.send('Exception docker.errors.ImageNotFound')
    #except docker.errors.APIError:
    #    await ctx.channel.send('Exception docker.errors.APIError')

@bot.command(
    name='stop',
    help='stops server'
)
async def stop(ctx):
    if len(docker_client.containers.list())==0:
        response = 'No docker containers running.'
        await ctx.channel.send(response)
        return
    c=0
    size=len(docker_client.containers.list())
    for cont in docker_client.containers.list():
        c+=1
        await ctx.channel.send('('+str(c)+'/'+str(size)+') Stopping container, please wait...')
        cont.stop()
        await ctx.channel.send('('+str(c)+'/'+str(size)+') Stopped container.')

def rebuild():
    proc=subprocess.run(['/bin/bash', '-c', '/home/ubuntu/AssettoCorsaCompetizioneDockerServer/build.sh'])

@bot.command(
    name='build',
    help='builds docker server'
)
async def build(ctx):
    await ctx.channel.send('Building server...')
    rebuild() #proc=subprocess.run(['/bin/bash', '-c', '/home/ubuntu/AssettoCorsaCompetizioneDockerServer/build.sh'])
    await ctx.channel.send('Server rebuilt.')


track_list = [
    "barcelona",
    "barcelona_2019",
    "brands_hatch",
    "brands_hatch_2019",
	"kyalami_2019",
	"laguna_seca_2019",
    "hungaroring",
    "hungaroring_2019",
    "misano",
    "misano_2019",
    "monza",
    "monza_2019",
	"mount_panorama_2019",
    "nurburgring",
    "nurburgring_2019",
    "paul_ricard",
    "paul_ricard_2019",
    "silverstone",
    "silverstone_2019",
    "spa",
    "spa_2019",
	"suzuka_2019",
    "zolder",
    "zolder_2019",
    "zandvoort",
    "zandvoort_2019",
]

@bot.command(
    name='changetrack',
    help='FORMAT changetrack <track_name>. Stops server, changes track, rebuilds server and starts new instance.'
)
async def changetrack(ctx, track_name=''):
    if track_name == '':
        await ctx.channel.send('No track given. FORMAT changetrack <track_name>.')
        return
    elif track_name not in track_list:
        await ctx.channel.send('Track not found in track list. See https://www.acc-wiki.info/wiki/Server_Configuration#ID_Lists')
        return
    # stopping server
    await stop(ctx)
    # change name of track
    event = json.load(open("/home/ubuntu/AssettoCorsaCompetizioneDockerServer/serverConfigs/event.json", "r"))
    event['track'] = track_name
    with open('/home/ubuntu/AssettoCorsaCompetizioneDockerServer/serverConfigs/event.json', 'w', encoding='utf-8') as f:
        json.dump(event, f, ensure_ascii=False, indent=4)
    await ctx.channel.send('Written track to event.json, rebuilding server...')
    await build(ctx)
    await start(ctx)
    await ctx.channel.send("Track changed. Please wait 2 minutes for server to connect to ACC.")


# discord bot client
bot.run(TOKEN)
