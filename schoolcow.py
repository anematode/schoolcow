import discord
from handlers import handle_message, handle_message_edit, handle_reaction, handle_reaction_remove


class SchoolCow(discord.Client):

    def __init__(self):
        discord.Client.__init__(self)

    async def on_message(self, message):
        await handle_message(self, message)

    async def on_message_edit(self, before, after):
        await handle_message_edit(self, before, after)

    async def on_reaction_add(self, reaction, user):
        await handle_reaction(self, reaction, user)

    async def on_reaction_remove(self, reaction, user):
        await handle_reaction_remove(self, reaction, user)


Cow = SchoolCow()


def run():
    Cow.run(open("secret_key.txt").read())


if __name__ == "__main__":
    print("Running SchoolCow")

    run()
