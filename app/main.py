import discord
import configparser
import redis
import requests


config = configparser.ConfigParser()
config.read('bot.ini')
token = config['Discord']['Token']
redishost = config['DEFAULT']['RedisHost']
redisport = config['DEFAULT']['RedisPort']
redispassword = config['DEFAULT']['RedisPassword']

redisconn = redis.Redis(
    host=redishost,
    port=redisport,
    password=redispassword)


class Bot:
    command_table = {}

    def __init__(self, token):
        self.client = discord.Client()
        self.token = token


def command(coroutine):
    Bot.command_table[coroutine.__name__.strip(' ')] = coroutine


class Asuka(Bot):
    def __init__(self, token):
        super().__init__(token)

    @command
    async def quit(self, message, args):
        await self.client.send_message(discord.Object('496185128171864065'),
                                       'I am needed elsewhere! Farewell!'.format(message))
        await self.client.close()

    @command
    async def verify(self, message, args):
        redisconn.hmset(message.channel)
    async def test(self, message, args):
        fromEmail = config['Mailgun']['from']
        subjectEmail = config['Mailgun']['subject']
        apiEmail = config['Mailgun']['API']
        urlEmail = config['Mailgun']['url']
        try:
            payload = {'from': fromEmail, 'to': args, 'subject': subjectEmail, 'text': 'This is a sample message'}
            header = {'api': apiEmail}
            send = requests.post(urlEmail, payload, headers=header)
            print(send.status_code)
            print(args)
        except:
            await self.client.send_message(message.channel, 'Message send Fail.')


asuka = Asuka(token)


@asuka.client.event
async def on_message(message):
    if message.author == asuka.client.user:
        return
    if message.content.startswith('.'):
        try:
            command, *args = message.content.lstrip('.').split()

            await Bot.command_table[command](asuka, message, args)
        except (ValueError, KeyError):
            await asuka.client.send_message(message.channel, 'Unknown command!')


@asuka.client.event
async def on_member_join(member):
    default_channel = config['YPH']['verify_chan']
    await asuka.client.send_message(discord.Object(default_channel),
                                    'Welcome, <@' + member.id + '>!')
    await asuka.client.send_message(discord.Object(default_channel),
                                    'Please run `.verify <STUDENT EMAIL>` to verify your account.')
    await asuka.client.send_message(discord.Object(default_channel),
                                    'You will receive an email with further instructions!')
    await asuka.client.send_message(discord.Object(default_channel),
                                    'You will be unable to speak until your account is verified.')
    await asuka.client.send_message(discord.Object(default_channel),
                                    'Accounts not verified within 30 minutes are automatically removed from the server.')


@asuka.client.event
async def on_ready():
    print('Logged in as')
    print(asuka.client.user.name)
    print(asuka.client.user.id)
    print('------')
    await asuka.client.send_message(discord.Object('496185128171864065'), 'I have returned!')


asuka.client.run(asuka.token)
