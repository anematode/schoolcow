import discord
import perms
import asyncio
import tex.render

RET_SP = 0
RET_CP = 1

class CowRestrictedFunction:
    def __init__(self, function, perm=perms.ALL):
        self.function = function
        self.perm = perm

    async def call(self, *args, **kwargs):  # returns false if it should be ignored, true if it should be the end and not propagate, and
        if not kwargs["user"] or self.perm(kwargs["user"]):  # call is allowed
            return await self.function(*args)
        return RET_CP


def sort_priority(arr):
    arr.sort(key=lambda x: x[1])


def add_message_handler(func, priority=0):
    message_handlers.append([func, priority])

    sort_priority(message_handlers)


def remove_message_handler(func):
    for i, handler in message_handlers:
        if handler[0] == func:
            del message_handlers[i]
            return


message_handlers = []
message_edit_handlers = []
reaction_handlers = []
reaction_add_handlers = []


async def handle_message(cow, msg):
    assert isinstance(cow, discord.Client)
    assert isinstance(msg, discord.Message)

    for handler_c in message_handlers:
        handler = handler_c[0]

        res = await handler.call(cow, msg, user=msg.author)

        if res == RET_CP:
            continue
        elif res == RET_SP:
            break


async def handle_message_edit(cow, before, after):
    assert isinstance(cow, discord.Client)
    assert isinstance(before, discord.Message)
    assert isinstance(after, discord.Message)


async def handle_reaction(cow, reaction, user):
    assert isinstance(cow, discord.Client)
    assert isinstance(reaction, discord.Reaction)
    assert isinstance(user, discord.User)


async def handle_reaction_remove(cow, reaction, user):
    assert isinstance(cow, discord.Client)
    assert isinstance(reaction, discord.Reaction)
    assert isinstance(user, discord.User)


Points = {

}


async def award(cow, msg):

    assert isinstance(cow, discord.Client)
    assert isinstance(msg, discord.Message)

    content = msg.content

    if content.startswith("school award"):
        mentions = msg.mentions

        if len(mentions) > 0:
            user = mentions[0]

            if user == msg.author:
                return

            if user in Points:
                Points[user] += 1
            else:
                Points[user] = 1

            await cow.send_message(msg.channel, "Awarded 1 point to " + user.mention + ".")


async def remove(cow, msg):

    assert isinstance(cow, discord.Client)
    assert isinstance(msg, discord.Message)

    content = msg.content

    if content.startswith("school rem"):
        mentions = msg.mentions

        if len(mentions) > 0:
            user = mentions[0]

            if user == msg.author:
                return

            if user in Points:
                Points[user] -= 1
            else:
                Points[user] = -1

            await cow.send_message(msg.channel, "Removed 1 point from " + user.mention + ".")


async def get(cow, msg):
    assert isinstance(cow, discord.Client)
    assert isinstance(msg, discord.Message)

    content = msg.content

    if content.startswith("school get"):
        mentions = msg.mentions

        if len(mentions) > 0:
            user = mentions[0]

            if user == msg.author:
                return

            point_count = (Points[user] if user in Points else 0)

            await cow.send_message(msg.channel, user.mention + " has " + str(point_count) + " point" +
                                   ("" if point_count == 1 else "s"))



async def render_tex(cow, msg):
    assert isinstance(cow, discord.Client)
    assert isinstance(msg, discord.Message)

    content = msg.content

    if content.startswith("school render"):
        user = msg.author
        tex_content = content[13:]

        render = await tex.render.render_tex_all(tex_content)

        try:
            if render.failed:
                message = await cow.send_message(msg.channel, """Render failed! Error log: ```{log}```""".format(log=render.reason))
            else:
                message = await cow.send_file(msg.channel, render.img_path())
        finally:
            render.close()


add_message_handler(CowRestrictedFunction(award))
add_message_handler(CowRestrictedFunction(remove))
add_message_handler(CowRestrictedFunction(get))
add_message_handler(CowRestrictedFunction(render_tex))