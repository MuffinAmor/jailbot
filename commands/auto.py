import os
import sys

import discord
from discord.ext import commands

from lib.create import create_user, create_server, delete_server
from lib.edit import edit_user_roles
from lib.request import request_user_jail, request_jail_role

bot = commands.Bot(command_prefix='p!')

botcolor = 0x40c444

os.chdir(r'/home/rex/data/WW/Vici')


class auto(commands.Cog):
    def __init__(self, bot, ):
        self.bot = bot

    ####################################################################################################################
    @commands.Cog.listener()
    async def on_message(self, message):
        if "discord.gg" in message.content or "discordapp.com/invite" in message.content:
            if not message.author.guild_permissions.administrator:
                if not "InviteChannel" in message.channel.topic:
                    try:
                        await message.delete()
                        embed2 = discord.Embed(
                            description='Invites sind **NICHT** erlaubt! \n Invite wurde '
                                        'gesendet von {}.'.format(message.author.mention), color=botcolor)
                        await message.channel.send(embed=embed2)
                    except:
                        pass

    @commands.Cog.listener()
    async def on_ready(self):
        for i in self.bot.guilds:
            server_id = str(i.id)
            create_server(server_id)
            for _ in i.members:
                user_id = str(_.id)
                create_user(server_id, user_id)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.channel.send(error)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        create_server(str(guild.id))
        server_id = str(guild.id)
        create_server(server_id)
        for _ in guild.members:
            user_id = str(_.id)
            create_user(server_id, user_id)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        delete_server(str(guild.id))

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        try:
            if not before.bot or not after.bot:
                if len(before.roles) != len(after.roles):
                    server_id = str(after.guild.id)
                    user_id = str(after.id)
                    jail_role_id = request_jail_role(server_id)
                    jail_role = after.guild.get_role(int(jail_role_id))
                    user_jailed = request_user_jail(server_id, user_id)
                    user_roles = list(role for role in after.roles)
                    if user_jailed == 'edit':
                        return
                    elif not user_jailed:
                        role_list = []
                        for i in after.roles:
                            if not i.name == "@everyone":
                                role_list.append(i.id)
                        edit_user_roles(server_id, user_id, role_list)
                    elif user_jailed:
                        if len(user_roles) <= 1 and jail_role in user_roles:
                            return
                        else:
                            for i in after.roles:
                                if not i.name == "@everyone" and not i == jail_role:
                                    try:
                                        await after.remove_roles(i)
                                    except PermissionError:
                                        pass
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not member.bot:
            server_id = str(member.guild.id)
            user_id = str(member.id)
            user_jailed = request_user_jail(server_id, user_id)
            jail_role_id = request_jail_role(server_id)
            jail_role = member.guild.get_role(int(jail_role_id))
            if user_jailed:
                for i in member.roles:
                    if not i.name == "@everyone":
                        try:
                            await member.remove_roles(i)
                        except PermissionError:
                            pass
                try:
                    await member.add_roles(jail_role)
                except PermissionError:
                    pass



def setup(bot):
    bot.add_cog(auto(bot))
