import discord


def ALL(user):
    assert isinstance(user, discord.Member)

    return True


def has_role(user, name):
    return name in (_.name.lower() for _ in user.roles)


def ADMIN(user):
    assert isinstance(user, discord.Member)

    return has_role(user, "admin")


def MOD(user):
    return ADMIN(user) or has_role(user, "mod")


def IS(user):
    assert isinstance(user, discord.Member)

    return lambda x: x == user


def ISNOT(user):
    is_f = IS(user)

    return lambda x: not is_f(x)
