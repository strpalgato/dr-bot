import discord
from discord.ext import commands
from collections import defaultdict
import asyncio
import json
import os

class AntiSpam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spam_tracker = defaultdict(list)
        self.mute_time = 240  # Tiempo en segundos para silenciar al usuario

        # Cargar las URLs de gifs desde el archivo JSON
        with open(os.path.join("data", "media.json"), "r") as f:
            media_data = json.load(f)
            self.gifs = media_data.get("gifs", {})
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("AntiSpam cargado correctamente.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return  # Ignorar mensajes de bots

        user_id = message.author.id
        timestamp = message.created_at.timestamp()

        # Verificar si el usuario tiene el rol que indica silencio
        if any(role.id == 1210341291821371403 for role in message.author.roles):
            await message.delete()  # Eliminar el mensaje
            return  # Salir del método sin procesar más

        # Verificar si el usuario ha enviado mensajes recientemente
        if len(self.spam_tracker[user_id]) >= 5:
            oldest_msg = self.spam_tracker[user_id][0]
            if timestamp - oldest_msg < 5:  # Si envió más de 5 mensajes en menos de 5 segundos
                # Silenciar al usuario
                await message.author.add_roles(message.guild.get_role(1210341291821371403))
                channel = message.guild.get_channel(1210343520582508634)
                # Enviar el mensaje inicial con la cuenta regresiva
                initial_message = await channel.send(f"{message.author.mention} ha sido silenciado por spam. Volverá <t:{int(timestamp + self.mute_time)}:R>")
                # Obtener la URL del gif desde el archivo JSON
                gif_url = self.gifs.get("gif1")
                await channel.send(gif_url)
                # Iniciar temporizador para levantar el silencio después del tiempo especificado
                await asyncio.sleep(self.mute_time)
                # Modificar el mensaje para eliminar el timestamp
                await initial_message.edit(content=f"{message.author.mention} fue silenciado por spam. *Volvió a los 4 minutos*  :white_check_mark:")   
                # Levantar el silencio
                await message.author.remove_roles(message.guild.get_role(1210341291821371403))
                # Limpiar la lista de mensajes del usuario
                self.spam_tracker[user_id] = []

        # Agregar el mensaje actual a la lista de mensajes del usuario
        self.spam_tracker[user_id].append(timestamp)

        # Mantener solo los últimos 5 mensajes del usuario en el registro
        if len(self.spam_tracker[user_id]) > 5:
            self.spam_tracker[user_id] = self.spam_tracker[user_id][-5:]

async def setup(bot):
    await bot.add_cog(AntiSpam(bot))
