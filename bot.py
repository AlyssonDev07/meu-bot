import discord
from discord.ext import commands
from discord import app_commands
import random
import unicodedata
import os
import asyncio

TOKEN = os.getenv("TOKEN")

CANAL_ENTRADA = 1500239261952245980
CANAL_SAIDA = 1500239349583974531

# Calls Bate-Papo
CANAL_CRIAR_CALL_BATEPAPO = 1500237380068573204
CATEGORIA_BATEPAPO = 1500237318148325376

# Standoff
CANAL_CRIAR_CALL_STANDOFF = 1500313730012024962
CANAL_CHAT_STANDOFF = 1500315002760859789
CATEGORIA_STANDOFF = 1500301722965381120

# Free Fire
CANAL_CRIAR_CALL_FF = 1500308286107549747
CANAL_CHAT_FF = 1500317425055567933
CATEGORIA_FF = 1500301895753928845

# Brawl Stars
CANAL_CRIAR_CALL_BS = 1500319590062882877
CANAL_CHAT_BS = 1500319493849612379
CATEGORIA_BS = 1500301934383333397

# Entretenimento
CANAL_AKINATOR = 1500321612560465970
CANAL_QUIZ = 1500322868125503518
CANAL_VTM = 1500322957673893959
CANAL_ADIVINHA = 1500322978683031572

GUILD_ID = 1499953983601639578

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

calls_temporarias = {}

PATENTES_STANDOFF = [
    "🥉 Bronze", "🥈 Silver", "🥇 Gold", "🔥 Phoenix",
    "🎯 Ranger", "🏆 Champion", "👑 Master", "⭐ Elite", "🌍 The Legend",
]
PATENTES_FF = [
    "🥉 Bronze", "🥈 Prata", "🥇 Ouro",
    "💎 Platina", "💠 Diamante", "👑 Mestre", "🏆 Desafiante",
]
PATENTES_BS = [
    "🥉 Bronze", "🥈 Prata", "🥇 Ouro",
    "💠 Diamante", "🔮 Mítico", "🌟 Lendário", "👑 Mestres",
]

QUIZ = {
    "🌍 Mundo": [
        {"p": "Qual é a capital do Brasil?", "r": ["Brasília", "São Paulo", "Rio de Janeiro", "Salvador"], "c": "Brasília"},
        {"p": "Qual é o maior oceano do mundo?", "r": ["Atlântico", "Índico", "Ártico", "Pacífico"], "c": "Pacífico"},
        {"p": "Qual país tem mais habitantes?", "r": ["Índia", "China", "EUA", "Brasil"], "c": "Índia"},
        {"p": "Qual é o maior país do mundo?", "r": ["Canadá", "China", "Rússia", "EUA"], "c": "Rússia"},
        {"p": "Em qual continente fica o Egito?", "r": ["Ásia", "Europa", "África", "Oceania"], "c": "África"},
    ],
    "👤 Pessoas": [
        {"p": "Quem inventou o telefone?", "r": ["Edison", "Tesla", "Bell", "Newton"], "c": "Bell"},
        {"p": "Quem foi o primeiro homem na Lua?", "r": ["Buzz Aldrin", "Neil Armstrong", "Yuri Gagarin", "John Glenn"], "c": "Neil Armstrong"},
        {"p": "Quem pintou a Monalisa?", "r": ["Picasso", "Van Gogh", "Da Vinci", "Michelangelo"], "c": "Da Vinci"},
        {"p": "Quem criou o WhatsApp?", "r": ["Zuckerberg", "Jan Koum", "Elon Musk", "Bill Gates"], "c": "Jan Koum"},
        {"p": "Quem foi Albert Einstein?", "r": ["Filósofo", "Médico", "Físico", "Químico"], "c": "Físico"},
    ],
    "🎮 Jogos": [
        {"p": "Qual patente é a mais alta no Free Fire?", "r": ["Diamante", "Mestre", "Desafiante", "Platina"], "c": "Desafiante"},
        {"p": "Qual patente é a mais alta no Standoff 2?", "r": ["Master", "Elite", "The Legend", "Champion"], "c": "The Legend"},
        {"p": "Qual patente é a mais alta no Brawl Stars?", "r": ["Lendário", "Mítico", "Mestres", "Diamante"], "c": "Mestres"},
        {"p": "Quantos jogadores tem uma partida padrão de Free Fire?", "r": ["50", "75", "100", "150"], "c": "50"},
        {"p": "Qual é o nome do mapa principal do Standoff 2?", "r": ["Dust", "Agency", "Arena", "Corridor"], "c": "Agency"},
    ],
    "🎨 Temas": [
        {"p": "Qual filme ganhou o Oscar de melhor filme em 2020?", "r": ["1917", "Coringa", "Parasita", "Ford vs Ferrari"], "c": "Parasita"},
        {"p": "Qual série foi a mais assistida na Netflix em 2023?", "r": ["Stranger Things", "Wednesday", "The Crown", "Squid Game"], "c": "Wednesday"},
        {"p": "Qual cor é formada misturando azul e amarelo?", "r": ["Roxo", "Laranja", "Verde", "Marrom"], "c": "Verde"},
        {"p": "Quantas cores tem o arco-íris?", "r": ["5", "6", "7", "8"], "c": "7"},
        {"p": "Qual instrumento tem 88 teclas?", "r": ["Violão", "Piano", "Órgão", "Teclado"], "c": "Piano"},
    ],
}

VTM = [
    {"p": "A Muralha da China pode ser vista do espaço.", "c": False},
    {"p": "Os golfinhos dormem com um olho aberto.", "c": True},
    {"p": "O coração humano bate cerca de 100 mil vezes por dia.", "c": True},
    {"p": "A água ferve a 100°C no nível do mar.", "c": True},
    {"p": "Os humanos usam apenas 10% do cérebro.", "c": False},
    {"p": "O Sol é uma estrela.", "c": True},
    {"p": "Morcegos são cegos.", "c": False},
    {"p": "O ouro é o metal mais pesado do mundo.", "c": False},
]

ADIVINHA = [
    {"dica": "Sou um herói da Marvel. Tenho escudo e sou americano.", "r": "Capitão América"},
    {"dica": "Sou uma princesa que tem cabelo comprido e fica numa torre.", "r": "Rapunzel"},
    {"dica": "Sou um plomeiro italiano que pula em cogumelos.", "r": "Mario"},
    {"dica": "Sou um detetive famoso que mora na Baker Street.", "r": "Sherlock Holmes"},
    {"dica": "Sou um rei leão que fugiu do seu reino quando era filhote.", "r": "Simba"},
    {"dica": "Sou um ninja laranja que quer ser Hokage.", "r": "Naruto"},
    {"dica": "Sou uma sereia que quer ter pernas e viver na terra.", "r": "Ariel"},
]

def normalizar(texto):
    texto = texto.lower().strip()
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    return texto

# ========== VIEWS ==========

class ContinuarPararView(discord.ui.View):
    def __init__(self, member, modo, tema=None):
        super().__init__(timeout=30)
        self.member = member
        self.modo = modo
        self.tema = tema

    @discord.ui.button(label="🔄 Jogar novamente", style=discord.ButtonStyle.success)
    async def jogar_novamente(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.member.id:
            await interaction.response.send_message("Não é sua vez!", ephemeral=True)
            return
        if self.modo == "quiz":
            pergunta = random.choice(QUIZ[self.tema])
            opcoes = pergunta["r"][:]
            random.shuffle(opcoes)
            embed = discord.Embed(title=f"❓ Quiz - {self.tema}", description=pergunta["p"], color=discord.Color.blurple())
            await interaction.response.edit_message(embed=embed, view=QuizRespostaView(self.member, pergunta["c"], opcoes, self.tema))
        elif self.modo == "vtm":
            pergunta = random.choice(VTM)
            embed = discord.Embed(title="🤔 Verdade ou Mito?", description=pergunta["p"], color=discord.Color.gold())
            await interaction.response.edit_message(embed=embed, view=VTMView(self.member, pergunta["c"]))
        elif self.modo == "adivinha":
            personagem = random.choice(ADIVINHA)
            embed = discord.Embed(title="🎭 Quem sou eu?", description=f"**Dica:** {personagem['dica']}", color=discord.Color.purple())
            embed.set_footer(text="Digite sua resposta no chat!")
            await interaction.response.edit_message(embed=embed, view=None)
            def check(m):
                return m.author.id == self.member.id and m.channel.id == CANAL_ADIVINHA
            try:
                msg = await bot.wait_for("message", check=check, timeout=30)
                if normalizar(msg.content) == normalizar(personagem["r"]):
                    result_embed = discord.Embed(title="✅ Correto! 🎉", description=f"Era **{personagem['r']}**!", color=discord.Color.green())
                else:
                    result_embed = discord.Embed(title="❌ Errado!", description=f"A resposta era **{personagem['r']}**!", color=discord.Color.red())
                await msg.reply(embed=result_embed, view=ContinuarPararView(self.member, "adivinha"))
            except:
                await interaction.followup.send(f"⏰ Tempo esgotado! A resposta era **{personagem['r']}**!", view=ContinuarPararView(self.member, "adivinha"))

    @discord.ui.button(label="⛔ Parar", style=discord.ButtonStyle.danger)
    async def parar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.member.id:
            await interaction.response.send_message("Não é sua vez!", ephemeral=True)
            return
        embed = discord.Embed(title="👋 Até mais!", description="Jogo encerrado!", color=discord.Color.greyple())
        await interaction.response.edit_message(embed=embed, view=None)

class QuizTemaView(discord.ui.View):
    def __init__(self, member):
        super().__init__(timeout=30)
        self.member = member
        for tema in QUIZ.keys():
            btn = discord.ui.Button(label=tema, style=discord.ButtonStyle.primary)
            btn.callback = self.make_callback(tema)
            self.add_item(btn)

    def make_callback(self, tema):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.member.id:
                await interaction.response.send_message("Não é sua vez!", ephemeral=True)
                return
            pergunta = random.choice(QUIZ[tema])
            opcoes = pergunta["r"][:]
            random.shuffle(opcoes)
            embed = discord.Embed(title=f"❓ Quiz - {tema}", description=pergunta["p"], color=discord.Color.blurple())
            await interaction.response.edit_message(embed=embed, view=QuizRespostaView(interaction.user, pergunta["c"], opcoes, tema))
        return callback

class QuizRespostaView(discord.ui.View):
    def __init__(self, member, correta, opcoes, tema):
        super().__init__(timeout=20)
        self.member = member
        self.correta = correta
        self.tema = tema
        for opcao in opcoes:
            btn = discord.ui.Button(label=opcao, style=discord.ButtonStyle.secondary)
            btn.callback = self.make_callback(opcao)
            self.add_item(btn)

    def make_callback(self, opcao):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.member.id:
                await interaction.response.send_message("Não é sua vez!", ephemeral=True)
                return
            if opcao == self.correta:
                embed = discord.Embed(title="✅ Correto! 🎉", description=f"A resposta era **{self.correta}**!", color=discord.Color.green())
            else:
                embed = discord.Embed(title="❌ Errado!", description=f"A resposta certa era **{self.correta}**!", color=discord.Color.red())
            await interaction.response.edit_message(embed=embed, view=ContinuarPararView(self.member, "quiz", self.tema))
        return callback

class VTMView(discord.ui.View):
    def __init__(self, member, correto):
        super().__init__(timeout=20)
        self.member = member
        self.correto = correto

    @discord.ui.button(label="✅ Verdade", style=discord.ButtonStyle.success)
    async def verdade(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.member.id:
            await interaction.response.send_message("Não é sua vez!", ephemeral=True)
            return
        if self.correto:
            embed = discord.Embed(title="✅ Correto! 🎉", description="Era **Verdade**!", color=discord.Color.green())
        else:
            embed = discord.Embed(title="❌ Errado!", description="Era **Mito**!", color=discord.Color.red())
        await interaction.response.edit_message(embed=embed, view=ContinuarPararView(self.member, "vtm"))

    @discord.ui.button(label="❌ Mito", style=discord.ButtonStyle.danger)
    async def mito(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.member.id:
            await interaction.response.send_message("Não é sua vez!", ephemeral=True)
            return
        if not self.correto:
            embed = discord.Embed(title="✅ Correto! 🎉", description="Era **Mito**!", color=discord.Color.green())
        else:
            embed = discord.Embed(title="❌ Errado!", description="Era **Verdade**!", color=discord.Color.red())
        await interaction.response.edit_message(embed=embed, view=ContinuarPararView(self.member, "vtm"))

class ModoStandoffView(discord.ui.View):
    def __init__(self, member):
        super().__init__(timeout=30)
        self.member = member

    @discord.ui.button(label="🤝 Aliados", style=discord.ButtonStyle.primary)
    async def aliados(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.member.id:
            await interaction.response.send_message("Essa seleção não é sua!", ephemeral=True)
            return
        await interaction.message.delete()
        canal = interaction.channel
        embed = discord.Embed(title="🎮 Criar Call - Standoff 2", description=f"{self.member.mention}, escolha a patente:", color=discord.Color.blurple())
        await canal.send(embed=embed, view=PatenteView(self.member, PATENTES_STANDOFF, CATEGORIA_STANDOFF, "aliados"))

    @discord.ui.button(label="🏆 Competitivo", style=discord.ButtonStyle.primary)
    async def competitivo(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.member.id:
            await interaction.response.send_message("Essa seleção não é sua!", ephemeral=True)
            return
        await interaction.message.delete()
        canal = interaction.channel
        embed = discord.Embed(title="🎮 Criar Call - Standoff 2", description=f"{self.member.mention}, escolha a patente:", color=discord.Color.blurple())
        await canal.send(embed=embed, view=PatenteView(self.member, PATENTES_STANDOFF, CATEGORIA_STANDOFF, "competitivo"))

class ModoFFView(discord.ui.View):
    def __init__(self, member):
        super().__init__(timeout=30)
        self.member = member

    @discord.ui.button(label="👥 Duo", style=discord.ButtonStyle.primary)
    async def duo(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.member.id:
            await interaction.response.send_message("Essa seleção não é sua!", ephemeral=True)
            return
        await interaction.message.delete()
        canal = interaction.channel
        embed = discord.Embed(title="🔥 Criar Call - Free Fire", description=f"{self.member.mention}, escolha a patente:", color=discord.Color.orange())
        await canal.send(embed=embed, view=PatenteView(self.member, PATENTES_FF, CATEGORIA_FF, "duo"))

    @discord.ui.button(label="🪖 Squad", style=discord.ButtonStyle.primary)
    async def squad(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.member.id:
            await interaction.response.send_message("Essa seleção não é sua!", ephemeral=True)
            return
        await interaction.message.delete()
        canal = interaction.channel
        embed = discord.Embed(title="🔥 Criar Call - Free Fire", description=f"{self.member.mention}, escolha a patente:", color=discord.Color.orange())
        await canal.send(embed=embed, view=PatenteView(self.member, PATENTES_FF, CATEGORIA_FF, "squad"))

class ModoBSView(discord.ui.View):
    def __init__(self, member):
        super().__init__(timeout=30)
        self.member = member

    @discord.ui.button(label="🏆 Push de Troféus", style=discord.ButtonStyle.primary)
    async def trofeus(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.member.id:
            await interaction.response.send_message("Essa seleção não é sua!", ephemeral=True)
            return
        await interaction.message.delete()
        canal = interaction.channel
        embed = discord.Embed(title="⚔️ Criar Call - Brawl Stars", description=f"{self.member.mention}, escolha a faixa de troféus:", color=0xff6b6b)
        await canal.send(embed=embed, view=TrofeusBSView(self.member))

    @discord.ui.button(label="⚔️ Ranked", style=discord.ButtonStyle.primary)
    async def ranked(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.member.id:
            await interaction.response.send_message("Essa seleção não é sua!", ephemeral=True)
            return
        await interaction.message.delete()
        canal = interaction.channel
        embed = discord.Embed(title="⚔️ Criar Call - Brawl Stars", description=f"{self.member.mention}, escolha a patente:", color=0xff6b6b)
        await canal.send(embed=embed, view=PatenteView(self.member, PATENTES_BS, CATEGORIA_BS, "ranked"))

class TrofeusBSView(discord.ui.View):
    def __init__(self, member):
        super().__init__(timeout=30)
        self.member = member
        faixas = ["0 - 5k", "5k - 10k", "10k - 20k", "20k - 50k", "50k - 100k"]
        for faixa in faixas:
            btn = discord.ui.Button(label=f"🏆 {faixa}", style=discord.ButtonStyle.secondary)
            btn.callback = self.make_callback(faixa)
            self.add_item(btn)

    def make_callback(self, faixa):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.member.id:
                await interaction.response.send_message("Essa seleção não é sua!", ephemeral=True)
                return
            await interaction.response.defer()
            categoria = bot.get_channel(CATEGORIA_BS)
            chave = "trofeus" + faixa
            numero = sum(1 for c in calls_temporarias.values() if c == chave) + 1
            nova_call = await interaction.guild.create_voice_channel(
                name=f"🏆 {faixa} - Call {numero:02d}",
                category=categoria,
                user_limit=3
            )
            calls_temporarias[nova_call.id] = chave
            await self.member.move_to(nova_call)
            await interaction.message.delete()
        return callback

class PatenteView(discord.ui.View):
    def __init__(self, member, patentes, categoria_id, modo=None):
        super().__init__(timeout=30)
        self.member = member
        self.categoria_id = categoria_id
        self.modo = modo
        for patente in patentes:
            btn = discord.ui.Button(label=patente, style=discord.ButtonStyle.primary)
            btn.callback = self.make_callback(patente)
            self.add_item(btn)

    def make_callback(self, patente):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.member.id:
                await interaction.response.send_message("Essa seleção não é sua!", ephemeral=True)
                return
            await interaction.response.defer()
            categoria = bot.get_channel(self.categoria_id)
            if not categoria:
                await interaction.followup.send("Categoria não encontrada!", ephemeral=True)
                return

            if self.modo == "aliados":
                user_limit = 2
                chave = patente + "aliados"
                numero = sum(1 for c in calls_temporarias.values() if c == chave) + 1
                nome = f"🤝 Aliados - {patente} - Call {numero:02d}"
            elif self.modo == "competitivo":
                user_limit = 5
                chave = patente + "competitivo"
                numero = sum(1 for c in calls_temporarias.values() if c == chave) + 1
                nome = f"🏆 Competitivo - {patente} - Call {numero:02d}"
            elif self.modo == "duo":
                user_limit = 2
                chave = patente + "duo"
                numero = sum(1 for c in calls_temporarias.values() if c == chave) + 1
                nome = f"👥 Duo - {patente} - Call {numero:02d}"
            elif self.modo == "squad":
                user_limit = 4
                chave = patente + "squad"
                numero = sum(1 for c in calls_temporarias.values() if c == chave) + 1
                nome = f"🪖 Squad - {patente} - Call {numero:02d}"
            elif self.modo == "ranked":
                user_limit = 3
                chave = patente + "ranked"
                numero = sum(1 for c in calls_temporarias.values() if c == chave) + 1
                nome = f"⚔️ Ranked - {patente} - Call {numero:02d}"
            else:
                user_limit = 0
                chave = patente
                numero = sum(1 for c in calls_temporarias.values() if c == chave) + 1
                nome = f"{patente} - Call {numero:02d}"

            nova_call = await interaction.guild.create_voice_channel(
                name=nome,
                category=categoria,
                user_limit=user_limit
            )
            calls_temporarias[nova_call.id] = chave
            await self.member.move_to(nova_call)
            await interaction.message.delete()
        return callback

# ========== EVENTOS ==========

@bot.event
async def on_ready():
    print(f"Bot {bot.user} está online!")
    guild = discord.Object(id=GUILD_ID)
    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)
    print("Slash commands sincronizados!")

@bot.event
async def on_member_join(member):
    canal = bot.get_channel(CANAL_ENTRADA)
    if canal:
        embed = discord.Embed(
            title="👋 Bem-vindo(a)!",
            description=f"Olá {member.mention}, seja bem-vindo(a) ao **{member.guild.name}**! 🎉",
            color=0x9b59b6
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"Membro #{member.guild.member_count}")
        await canal.send(embed=embed)

@bot.event
async def on_member_remove(member):
    canal = bot.get_channel(CANAL_SAIDA)
    if canal:
        embed = discord.Embed(
            title="😢 Saiu do servidor",
            description=f"**{member.name}** saiu do servidor. Até mais!",
            color=discord.Color.red()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        await canal.send(embed=embed)

@bot.event
async def on_voice_state_update(member, before, after):
    # Call simples Bate-Papo
    if after.channel and after.channel.id == CANAL_CRIAR_CALL_BATEPAPO:
        categoria = bot.get_channel(CATEGORIA_BATEPAPO)
        numero = sum(1 for c in calls_temporarias.values() if c == "batepapo") + 1
        nova_call = await member.guild.create_voice_channel(
            name=f"Call {numero:02d}",
            category=categoria
        )
        calls_temporarias[nova_call.id] = "batepapo"
        await member.move_to(nova_call)

    # Standoff
    if after.channel and after.channel.id == CANAL_CRIAR_CALL_STANDOFF:
        canal_texto = bot.get_channel(CANAL_CHAT_STANDOFF)
        embed = discord.Embed(title="🎮 Criar Call - Standoff 2", description=f"{member.mention}, escolha o modo:", color=discord.Color.blurple())
        await canal_texto.send(embed=embed, view=ModoStandoffView(member))

    # Free Fire
    if after.channel and after.channel.id == CANAL_CRIAR_CALL_FF:
        canal_texto = bot.get_channel(CANAL_CHAT_FF)
        embed = discord.Embed(title="🔥 Criar Call - Free Fire", description=f"{member.mention}, escolha o modo:", color=discord.Color.orange())
        await canal_texto.send(embed=embed, view=ModoFFView(member))

    # Brawl Stars
    if after.channel and after.channel.id == CANAL_CRIAR_CALL_BS:
        canal_texto = bot.get_channel(CANAL_CHAT_BS)
        embed = discord.Embed(title="⚔️ Criar Call - Brawl Stars", description=f"{member.mention}, escolha o modo:", color=0xff6b6b)
        await canal_texto.send(embed=embed, view=ModoBSView(member))

    # Deletar call vazia
    if before.channel and before.channel.id in calls_temporarias:
        canal = before.channel
        if len(canal.members) == 0:
            if canal.id in calls_temporarias:
                del calls_temporarias[canal.id]
            try:
                await canal.delete()
            except:
                pass

# ========== SLASH COMMANDS ==========

@bot.tree.command(name="aki", description="Jogar Akinator!", guild=discord.Object(id=GUILD_ID))
async def aki(interaction: discord.Interaction):
    if interaction.channel_id != CANAL_AKINATOR:
        await interaction.response.send_message(f"❌ Use esse comando no canal <#{CANAL_AKINATOR}>!", ephemeral=True)
        return
    embed = discord.Embed(title="🧞 Akinator", description="Clique no botão abaixo para jogar!", color=0x9b59b6)
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="🎮 Jogar Akinator", url="https://en.akinator.com", style=discord.ButtonStyle.link))
    await interaction.response.send_message(embed=embed, view=view)

@bot.tree.command(name="quiz", description="Jogar Quiz!", guild=discord.Object(id=GUILD_ID))
async def quiz(interaction: discord.Interaction):
    if interaction.channel_id != CANAL_QUIZ:
        await interaction.response.send_message(f"❌ Use esse comando no canal <#{CANAL_QUIZ}>!", ephemeral=True)
        return
    embed = discord.Embed(title="🎯 Quiz", description="Escolha o tema:", color=discord.Color.blurple())
    await interaction.response.send_message(embed=embed, view=QuizTemaView(interaction.user))

@bot.tree.command(name="vtm", description="Verdade ou Mito!", guild=discord.Object(id=GUILD_ID))
async def vtm(interaction: discord.Interaction):
    if interaction.channel_id != CANAL_VTM:
        await interaction.response.send_message(f"❌ Use esse comando no canal <#{CANAL_VTM}>!", ephemeral=True)
        return
    pergunta = random.choice(VTM)
    embed = discord.Embed(title="🤔 Verdade ou Mito?", description=pergunta["p"], color=discord.Color.gold())
    await interaction.response.send_message(embed=embed, view=VTMView(interaction.user, pergunta["c"]))

@bot.tree.command(name="adivinha", description="Adivinhe o personagem!", guild=discord.Object(id=GUILD_ID))
async def adivinha(interaction: discord.Interaction):
    if interaction.channel_id != CANAL_ADIVINHA:
        await interaction.response.send_message(f"❌ Use esse comando no canal <#{CANAL_ADIVINHA}>!", ephemeral=True)
        return
    personagem = random.choice(ADIVINHA)
    embed = discord.Embed(title="🎭 Quem sou eu?", description=f"**Dica:** {personagem['dica']}", color=discord.Color.purple())
    embed.set_footer(text="Digite sua resposta no chat!")
    await interaction.response.send_message(embed=embed)

    def check(m):
        return m.author.id == interaction.user.id and m.channel.id == CANAL_ADIVINHA

    try:
        msg = await bot.wait_for("message", check=check, timeout=30)
        if normalizar(msg.content) == normalizar(personagem["r"]):
            result_embed = discord.Embed(title="✅ Correto! 🎉", description=f"Era **{personagem['r']}**!", color=discord.Color.green())
        else:
            result_embed = discord.Embed(title="❌ Errado!", description=f"A resposta era **{personagem['r']}**!", color=discord.Color.red())
        await msg.reply(embed=result_embed, view=ContinuarPararView(interaction.user, "adivinha"))
    except:
        await interaction.followup.send(f"⏰ Tempo esgotado! A resposta era **{personagem['r']}**!", view=ContinuarPararView(interaction.user, "adivinha"))

CANAL_REGRAS = 1500227927076241448

@bot.tree.command(name="limpar", description="Apagar todas as mensagens do canal!", guild=discord.Object(id=GUILD_ID))
@app_commands.checks.has_permissions(manage_messages=True)
async def limpar(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    deleted = await interaction.channel.purge(limit=1000)
    await interaction.followup.send(f"🗑️ {len(deleted)} mensagens apagadas!", ephemeral=True)

@bot.tree.command(name="regras", description="Enviar regras do servidor!", guild=discord.Object(id=GUILD_ID))
async def regras(interaction: discord.Interaction):
    if interaction.channel_id != CANAL_REGRAS:
        await interaction.response.send_message(f"❌ Use esse comando no canal <#{CANAL_REGRAS}>!", ephemeral=True)
        return

    embed = discord.Embed(
        title="📜 Regras do Servidor",
        color=0x9b59b6
    )
    embed.add_field(name="1️⃣ Respeite todos os membros", value="Sem xingamentos ou provocações desnecessárias.", inline=False)
    embed.add_field(name="2️⃣ Proibido spam e flood", value="Sem mensagens repetidas ou desnecessárias.", inline=False)
    embed.add_field(name="3️⃣ Sem conteúdo impróprio", value="Nada de conteúdo +18 ou perturbador.", inline=False)
    embed.add_field(name="4️⃣ Sem divulgação", value="Proibido divulgar outros servidores ou links suspeitos.", inline=False)
    embed.add_field(name="5️⃣ Use os canais corretamente", value="Cada canal tem sua função, respeite isso.", inline=False)
    embed.add_field(name="6️⃣ Não mencione a Staff sem necessidade", value="Só mencione a Staff em casos realmente necessários.", inline=False)
    embed.add_field(name="7️⃣ Sem preconceito", value="Nada de racismo, discriminação ou qualquer tipo de preconceito.", inline=False)
    embed.add_field(name="8️⃣ Respeito nas calls", value="Sem ruídos excessivos ou comportamento perturbador nas calls.", inline=False)
    embed.add_field(name="9️⃣ Sem trapaças", value="Cheats ou trapaças nos jogos resultam em banimento.", inline=False)
    embed.add_field(name="🔟 A Staff tem a palavra final", value="Em qualquer situação, a decisão da Staff é definitiva.", inline=False)
    embed.set_footer(text="⚠️ O descumprimento pode resultar em advertência, mute ou banimento!")

    await interaction.response.send_message(embed=embed)

bot.run(TOKEN)
