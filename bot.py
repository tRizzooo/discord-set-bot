import discord
from discord.ext import commands
import os

# ========= CONFIGURAÇÕES =========
TOKEN = os.getenv("DISCORD_TOKEN")  # token vem do Railway
CANAL_ID = 1455358323623989300       # ID do canal permitido
CARGO_NOME = "Membro"               # nome exato do cargo

# ========= INTENTS =========
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ========= BOT ONLINE =========
@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

# ========= MODAL =========
class SetModal(discord.ui.Modal, title="Configurar Perfil"):
    nome = discord.ui.TextInput(
        label="Nome na cidade",
        placeholder="Ex: João Silva",
        required=True
    )

    passaporte = discord.ui.TextInput(
        label="Passaporte",
        placeholder="Ex: 12345",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user

        novo_nome = f"#{self.passaporte.value} | {self.nome.value}"

        try:
            await member.edit(nick=novo_nome)

            cargo = discord.utils.get(guild.roles, name=CARGO_NOME)
            if cargo:
                await member.add_roles(cargo)

            await interaction.response.send_message(
                "✅ Perfil configurado com sucesso!",
                ephemeral=True
            )

        except Exception as e:
            await interaction.response.send_message(
                f"❌ Erro ao configurar perfil: {e}",
                ephemeral=True
            )

# ========= VIEW COM BOTÃO =========
class SetView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Fazer Set",
        style=discord.ButtonStyle.green
    )
    async def set_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.channel.id != CANAL_ID:
            await interaction.response.send_message(
                "❌ Use este botão no canal correto.",
                ephemeral=True
            )
            return

        await interaction.response.send_modal(SetModal())

# ========= COMANDO =========
@bot.command()
async def set(ctx):
    if ctx.channel.id != CANAL_ID:
        await ctx.send(f"❌ Use este comando no canal <#{CANAL_ID}>.")
        return

    await ctx.send(
        "Clique no botão abaixo para configurar seu perfil:",
        view=SetView()
    )

# ========= INICIAR BOT =========
bot.run(TOKEN)
