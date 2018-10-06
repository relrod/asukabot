import discord

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
        await self.client.send_message(discord.Object('496185128171864065'), 'I am needed elsewhere! Farewell!'.format(message))
        await self.client.close()


asuka = Asuka('NDk2MTg2MTgxNDk5NzQ4MzU0.DpM_oA.jGbBvZkSa_NW3pfBAm5Yb0_Ctzs')

@asuka.client.event
async def on_message(message):
    if message.author == asuka.client.user:
        return
    if message.content.startswith('.'):
        try:
            command, *args = message.content.lstrip('.').split()

            await Bot.command_table[command](asuka, message, args)
        except (ValueError, KeyError):
            await asuka.client.send_message(discord.Object('496185128171864065'), 'Unknown command!')

@asuka.client.event
async def on_member_join(member):
    await asuka.client.send_message(discord.Object('375064753208426499'), 'Welcome, <@' + member.id + '>! I have sent you instructions on how to verify your account!')
    await asuka.client.send_message(discord.Object('375064753208426499'), 'You will be unable to speak until your account is verified. Accounts not verified within 30 minutes are automatically removed from the server.')

@asuka.client.event
async def on_ready():
    print('Logged in as')
    print(asuka.client.user.name)
    print(asuka.client.user.id)
    print('------')
    await asuka.client.send_message(discord.Object('496185128171864065'), 'I have returned!')

asuka.client.run(asuka.token)