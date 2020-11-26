import os

import discord
from discord.ext import commands

from lib.edit import edit_user_jail, edit_jail_log, edit_jail_role
from lib.request import request_jail_role, request_jail_log, request_user_jail, request_user_roles

bot = commands.Bot(command_prefix='p!')

botcolor = 0x40c444

os.chdir(r'/home/rex/data/WW/Vici')

bot.remove_command('help')


class JailCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ####################################################################################################################
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_knast(self, ctx, member: discord.Member = None):
        if not ctx.author.bot:
            if not member:
                await ctx.send("Bitte Nutzer angeben.")
            else:
                server_id = str(ctx.guild.id)
                user_id = str(member.id)
                is_in_jail = request_user_jail(server_id, user_id)
                if not is_in_jail:
                    jail_log_id = request_jail_log(server_id)
                    jail_log = self.bot.get_channel(int(jail_log_id))
                    jail_role_id = request_jail_role(server_id)
                    jail_role = ctx.guild.get_role(int(jail_role_id))
                    if jail_role:
                        edit_user_jail(server_id, user_id, True)
                        try:
                            await member.add_roles(jail_role)
                        except PermissionError:
                            await ctx.send("Mit fehlen Rechte.")
                        else:
                            await ctx.send("Nutzer wurde erfolgreich eingesperrt.")
                            if jail_log:
                                await jail_log.send("Nutzer {} wurde von {} eingesperrt.".format(member, ctx.author))
                    else:
                        await ctx.send("Es wurde noch keine Knast Rolle festgelegt.")
                else:
                    await ctx.send("Nutzer ist bereits eingesperrt.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def remove_knast(self, ctx, member: discord.Member = None):
        if not ctx.author.bot:
            if not member:
                await ctx.send("Bitte Nutzer angeben.")
            else:
                server_id = str(ctx.guild.id)
                user_id = str(member.id)
                is_in_jail = request_user_jail(server_id, user_id)
                if is_in_jail:
                    jail_log_id = request_jail_log(server_id)
                    jail_log = self.bot.get_channel(int(jail_log_id))
                    user_roles = request_user_roles(server_id, user_id)
                    jail_role_id = request_jail_role(server_id)
                    jail_role = ctx.guild.get_role(int(jail_role_id))
                    if jail_role:
                        edit_user_jail(server_id, user_id, 'edit')
                        if jail_role in member.roles:
                            try:
                                await member.remove_roles(jail_role)
                            except PermissionError:
                                await ctx.send("Mit fehlen Rechte.")
                    for i in user_roles:
                        role = ctx.guild.get_role(int(i))
                        if role:
                            try:
                                await member.add_roles(role)
                            except PermissionError:
                                await ctx.send("Mit fehlen Rechte.")
                    edit_user_jail(server_id, user_id, False)
                    await ctx.send("Der Nutzer wurde aus dem Knast entlassen")
                    if jail_log:
                        await jail_log.send("Nutzer {} wurde von {} entlassen.".format(member, ctx.author))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_role(self, ctx, role: discord.Role = None):
        if not ctx.author.bot:
            if not role:
                await ctx.send("Bitte Rolle angeben.")
            else:
                server_id = str(ctx.guild.id)
                edit_jail_role(server_id, role.id)
                await ctx.send("Die Knastrolle wurde erfolgreich eingestellt.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_log(self, ctx, channel: discord.TextChannel = None):
        if not ctx.author.bot:
            if not channel:
                await ctx.send("Bitte Channel angeben.")
            else:
                server_id = str(ctx.guild.id)
                edit_jail_log(server_id, channel.id)
                await ctx.send("Der Knastlog wurde erfolgreich eingestellt.")



########################################################################################################################
def setup(bot):
    bot.add_cog(JailCommands(bot))
