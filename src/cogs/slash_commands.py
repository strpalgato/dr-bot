import discord
from discord import app_commands
from discord.ext import commands

class slash_commands(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print("Comandos slash cargados correctamente.")
  
  @app_commands.command(name="serverip", description="Obtén la IP del servidor")
  async def serverip(self, interaction: discord.Interaction):
    await interaction.response.send_message("La IP del servidor es **server.boukencraft.com**", ephemeral=True)
  
  @app_commands.command(name="clear", description="Borra mensajes del canal")
  async def clear(self, interaction: discord.Interaction, amount: int):
    
    try:
        if amount <= 0:
          await interaction.response.send_message("Por favor, introduce un número positivo mayor que 0.", ephemeral=True)
          return  # Sale de la función si la cantidad es 0 o negativa

        if amount > 1:
          await interaction.response.send_message(f"Se han borrado {amount} mensajes.", ephemeral=True)

        else:
          await interaction.response.send_message(f"Se ha borrado {amount} mensaje.", ephemeral=True)

        await interaction.channel.purge(limit=amount
                                        )
    except discord.NotFound:
        print("La interacción ya no existe.")
  
async def setup(client: commands.Bot) -> None:
  await client.add_cog(slash_commands(client))

