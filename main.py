import discord
from discord.ext import commands
import os
from ai import get_class
import random
import shutil
import hashlib

STORAGE_DIR = "storage"
os.makedirs(STORAGE_DIR, exist_ok=True)

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.reactions = True
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents)

SAVE_DIRECTORY = "saved_images"
os.makedirs(SAVE_DIRECTORY, exist_ok=True)

@bot.command(name='commands')
async def send_link(ctx):
    await ctx.send("""Command yang ada:
`$commands` : memperlihatkan semua command yang ada
`$info`: memberikan **informasi** tentang perubahan iklim
`$quiz`: memberikan **quiz** yang bisa dipelajari kembali setelah dijawab
`$meme`: memperlihatkan beberapa **meme** tentang perubahan iklim
`$inventory`: untuk melihat gambar apa saja yang sudah anda dapatkan
`$save`: digunakan untuk menyimpan gambar anda sendiri ke dalam bot
`$learn`: link **video** belajar tentang perubahan iklim, tapi ada kemungkin kejadian lucu terjadi ;)""")

pages = [
    "🌏 **Pengertian Perubahan Iklim**\nPerubahan iklim mengacu pada perubahan jangka panjang dalam suhu dan pola cuaca. Pergeseran ini terjadi secara alami, seperti melalui variasi siklus matahari. Namun sejak tahun 1800-an, aktivitas manusia telah menjadi penyebab utama perubahan iklim, terutama akibat pembakaran bahan bakar fosil seperti batu bara, minyak dan gas.",
    """🏭 **Penyebab Perubahan Iklim**
    \n1. Gas rumah kaca💨
    \nBeberapa gas yang ada di atmosfer bumi bertindak seperti kaca di rumah kaca, yaitu dengan memerangkap panas yang dihasilkan matahari dan menghentikannya supaya tidak bocor dan kembali ke angkasa.
    \n2. Peningkatan emisi ⛽
    \nPenyebab terjadinya perubahan iklim yang kedua berasal dari adanya peningkatan pada emisi yang dilakukan oleh manusia, di antaranya adalah pembakaran batu bara, gas, dan minyak yang bisa menghasilkan dioksida dan nitrogen dioksida. Penebangan hutan, pupuk yang mengandung nitrogen juga bisa menjadi penyebab perubahan iklim.
    \n3. Pemanasan global 🤒
    \nPenyebab perubahan iklim yang selanjutnya adalah adanya aktivitas pemanasan global. Pembangkit listrik dan instalasi industri menjadi penghasil utama CO2. Para ilmuwan iklim dunia berpikir bahwa aktivitas yang dilakukan manusia pasti menjadi penyebab utama dari pemanasan dan menyebabkan perubahan iklim.
    \n4. Kendaraan bermotor 🚗💨
    \nBensin juga termasuk ke dalam bahan bakar fosil. Di mana pembuangan gas pada kendaraan bermotor mengandung banyak sekali polusi gas kimia yang menjadi penyebab perubahan iklim global. Ini menjadi penyebab terjadinya perubahan iklim yang tidak terbantahkan.
    \n5. Tempat pembuangan sampah 🗑️
    \nKetika membuang makanan dan sampah taman ke tempat sampah, maka sampah tersebut akan dibawa dan terkubur di tempat pembuangan sampah. Hal ini yang menjadi penyebab perubahan iklim. Ketika sampah yang berada di paling bawah mengalami pembusukan, maka terbentuklah gas methane.""",
    """⛈️ **Dampak Perubahan Iklim**
    \n1. Peningkatan Suhu Bumi 🌡️
    \nPerubahan iklim dapat meningkatkan konsentrasi gas rumah kaca. Kondisi ini jika terus menerus terjadi, maka suhu permukaan global akan meningkat.
    \n2. Menyebabkan Badai Destruktif 🌪️
    \nDampak perubahan iklim lainnya yaitu menyebabkan badai destruktif menjadi lebih kuat dan sering di beberapa wilayah. Seiring dengan meningkatkan suhu, maka banyak suhu air menguap. Kondisi tersebut bisa menyebabkan curah hujan ekstrem dan banjir, sehingga menimbulkan badai destruktif.
    \n3. Mengakibatkan Kekeringan 🍂
    \nPerubahan iklim turut mengubah ketersediaan air yang dapat memicu kekeringan di berbagai wilayah. Pemanasan global juga bisa memperburuk kekeringan di wilayah yang telah mengalami kesulitan air.
    \n4. Menyebabkan Volume dan Suhu Laut Meningkat 🌊
    \nDampak perubahan iklim lainnya yaitu terjadi peningkatan volume dan suhu laut. Dalam beberapa tahun terakhir, suhu air laut meningkat lebih cepat di hampir seluruh kedalaman laut. Saat suhu air laut meningkat, maka volume air akan bertambah karena air mengalami pemuaian.""",
    """♻️ **Cara Mengatasi Perubahan Iklim**
    \n1. Menghemat energi. 🔋
    \nDengan menghemat energi, kita dapat mengurangi efek rumah kaca yang menyebabkan perubahan iklim.
    \n2. Berjalan kaki, bersepeda, atau naik kendaraan umum. 🚶
    \nIni akan mengurangi emisi gas rumah kaca dan membantu kesehatan serta kebugaran tubuh.
    \n3. Kurangi perjalanan menggunakan pesawat. ❌✈️
    \nSejumlah besar bahan bakar fosil digunakan untuk pesawat, sehingga menghasilkan emisi gas rumah kaca yang signifikan.
    \n4. Ubah sumber energi rumah. 🌬️➡️⚡
    \nJika memungkinkan, coba beralih ke sumber energi terbarukan, seperti angin atau matahari. Pasang panel surya di atap untuk menghasilkan energi bagi rumah.""",
    '📄 **Quiz time**\nsekarang kamu bisa mengerjakan quiz tentang perubahan iklim dengan menjalankan perintah $quiz'
]

class PageButton(discord.ui.Button):
    def __init__(self, page_number: int):
        super().__init__(label=f"{page_number+1}", style=discord.ButtonStyle.primary)
        self.page_number = page_number

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"Perubahan Iklim",
            description=pages[self.page_number],
            color=discord.Color.blurple()
        )
        await interaction.response.edit_message(embed=embed, view=self.view)

class PageView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=600)
        for i in range(len(pages)):
            self.add_item(PageButton(i))

@bot.command(name='info')
async def paginate(ctx):
    embed = discord.Embed(
        title="Perubahan Iklim",
        description=pages[0],
        color=discord.Color.blurple()
    )
    view = PageView()
    await ctx.send(embed=embed, view=view)

Quiz1 = {
    "🇦": discord.Embed(title="Salah!", description="Silahkan coba lagi."),
    "🇧": discord.Embed(title="Benar!", description="Anda sangat pintar."),
    "🇨": discord.Embed(title="Salah!", description="Silahkan coba lagi."),
    "📄": discord.Embed(title="📄Soal", description="""Di bawah ini yang bukan merupakan penyebab perubahan iklim adalah?
    \nA. Gas rumah kaca
    \nB. Makan makanan sehat
    \nC. Kendaraan bermotor""")
}


Quiz2 = {
    "🇦": discord.Embed(title="Benar!", description="Anda sangat pintar."),
    "🇧": discord.Embed(title="Salah!", description="Silahkan coba lagi."),
    "🇨": discord.Embed(title="Salah!", description="Silahkan coba lagi."),
    "📄": discord.Embed(title="📄Soal", description="""Apakah bepergian dengan sepeda merupakan cara mengatasi perubahan iklim?
    \nA. Ya
    \nB. Tidak
    \nC. Tidak tahu""")
}

Quiz3 = {
    "🇦": discord.Embed(title="Benar!", description="Anda sangat pintar."),
    "🇧": discord.Embed(title="Salah!", description="Silahkan coba lagi."),
    "🇨": discord.Embed(title="Tidak apa!", description="Silahkan belajar lagi."),
    "📄": discord.Embed(title="📄Soal", description="""Apa itu perubahan iklim?
    \nA. Perubahan jangka panjang dalam suhu dan pola cuaca.
    \nB. Tersebarluasnya pengaruh ilmu pengetahuan dan kebudayaan yang ada di setiap penjuru dunia ke penjuru dunia yang lain.
    \nC. Meningkatnya suhu atmosfer , laut, dan daratan.""")
}

Quiz4 = {
    "🇦": discord.Embed(title="Salah!", description="Silahkan coba lagi."),
    "🇧": discord.Embed(title="Salah!", description="Silahkan coba lagi."),
    "🇨": discord.Embed(title="Benar!", description="Anda sangat pintar\n"),
    "📄": discord.Embed(title="📄Soal", description="""Yang merupakan dampak perubahan iklim adalah?
    \nA. Tanah menjadi subur.
    \nB. Cuaca cerah sepanjang waktu.
    \nC. Suhu bumi meningkat.""")
}

Quiz5 = {
    "🇦": discord.Embed(title="Salah!", description="Silahkan coba lagi."),
    "🇧": discord.Embed(title="Salah!", description="Silahkan coba lagi."),
    "🇨": discord.Embed(title="Benar!", description="Anda sangat pintar."),
    "📄": discord.Embed(title="📄Soal", description="""Berikut ini yang merupakan penyebab perubahan iklim?
    \nA. Perdamaian global.
    \nB. Penghijauan global.
    \nC. Pemanasan global.""")
}

def hash_file(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def user_has_image(user_id, image_path):
    target_hash = hash_file(image_path)
    user_dir = f"user_images/{user_id}"
    if not os.path.exists(user_dir):
        return False
    for fname in os.listdir(user_dir):
        fpath = os.path.join(user_dir, fname)
        if hash_file(fpath) == target_hash:
            return True
    return False

@bot.command(name='save')
async def upload(ctx):
    if not ctx.message.attachments:
        await ctx.send("Mohon lampirkan gambar untuk diunggah.")
        return

    user_dir = f"user_images/{ctx.author.id}"
    os.makedirs(user_dir, exist_ok=True)

    for attachment in ctx.message.attachments:
        if attachment.filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            save_path = os.path.join(user_dir, attachment.filename)
            await attachment.save(save_path)
            await ctx.send(f"✅ Gambar '{attachment.filename}' berhasil disimpan.") 
        else:
            await ctx.send(f"'{attachment.filename}' bukan format gambar yang valid.")

@bot.command(name='quiz')
async def menu(ctx):
    paper_emoji = "📄"
    A = '🇦'
    B = '🇧'
    C = '🇨'

    pick = random.randint(1, 5)

    if pick == 1:
        quiz = Quiz1
        correct_emoji = B
        fallback_image = "benar1.jpeg"
    elif pick == 2:
        quiz = Quiz2
        correct_emoji = A
        fallback_image = "benar2.jpeg"
    elif pick == 3:
        quiz = Quiz3
        correct_emoji = A
        fallback_image = "benar3.jpeg"
    elif pick == 4:
        quiz = Quiz4
        correct_emoji = C
        fallback_image = "benar4.jpeg"
    elif pick == 5:
        quiz = Quiz5
        correct_emoji = C
        fallback_image = "benar5.jpg"

    emojis = list(quiz.keys())
    current_embed = quiz[paper_emoji]
    message = await ctx.send(embed=current_embed)

    for emoji in emojis:
        await message.add_reaction(emoji)

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in emojis and reaction.message.id == message.id

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=120.0, check=check)
            emoji_clicked = str(reaction.emoji)
            new_embed = quiz.get(emoji_clicked)

            if new_embed:
                if emoji_clicked == correct_emoji:
                    file = discord.File(fallback_image, filename=os.path.basename(fallback_image))
                    new_embed.set_image(url=f"attachment://{os.path.basename(fallback_image)}")
                    await message.edit(embed=new_embed, attachments=[file])

                    # Save to user's storage if not already there
                    user_dir = f"user_images/{user.id}"
                    os.makedirs(user_dir, exist_ok=True)
                    if not user_has_image(user.id, fallback_image):
                        base = os.path.basename(fallback_image)
                        new_name = f"{os.path.splitext(base)[0]}_{random.randint(1000,9999)}{os.path.splitext(base)[1]}"
                        save_path = os.path.join(user_dir, new_name)
                        shutil.copy(fallback_image, save_path)
                        await ctx.send(f"📥 Gambar berhasil disimpan sebagai `{new_name}`.")
                    else:
                        await ctx.send("⚠️ Gambar ini sudah ada di penyimpanan kamu.")
                else:
                    await message.edit(embed=new_embed)

            await message.remove_reaction(reaction.emoji, user)

        except Exception:
            break

@bot.command(name='inventory')
async def myimages(ctx):
    user_id = ctx.author.id
    user_dir = f"user_images/{user_id}"

    if not os.path.exists(user_dir) or not os.listdir(user_dir):
        await ctx.send("📂 Kamu belum menyimpan gambar apa pun.")
        return

    files = sorted(os.listdir(user_dir))
    per_page = 5
    total_pages = (len(files) + per_page - 1) // per_page
    current_page = 0

    number_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
    nav_emojis = ["⬅️", "➡️"]
    valid_emojis = number_emojis + nav_emojis

    def get_page_embed(page):
        start = page * per_page
        end = start + per_page
        chunk = files[start:end]
        lines = [f"{number_emojis[i]} {name}" for i, name in enumerate(chunk)]
        embed = discord.Embed(title=f"📁 Gambar kamu (Hal {page + 1}/{total_pages})", description="\n".join(lines))
        return embed, chunk

    embed, chunk = get_page_embed(current_page)
    message = await ctx.send(embed=embed)

    for emoji in valid_emojis[:len(chunk)] + nav_emojis:
        await message.add_reaction(emoji)

    def check(reaction, user):
        return (
            user == ctx.author
            and str(reaction.emoji) in valid_emojis
            and reaction.message.id == message.id
        )

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=60.0, check=check)
            emoji = str(reaction.emoji)
            await message.remove_reaction(emoji, user)

            if emoji in number_emojis:
                index = number_emojis.index(emoji)
                if index < len(chunk):
                    filename = chunk[index]
                    path = os.path.join(user_dir, filename)
                    file = discord.File(path, filename=filename)
                    await ctx.send(f"🖼️ Gambar kamu: `{filename}`", file=file)

            elif emoji == "➡️" and current_page < total_pages - 1:
                current_page += 1
                embed, chunk = get_page_embed(current_page)
                await message.edit(embed=embed)
                await message.clear_reactions()
                for emoji in valid_emojis[:len(chunk)] + nav_emojis:
                    await message.add_reaction(emoji)

            elif emoji == "⬅️" and current_page > 0:
                current_page -= 1
                embed, chunk = get_page_embed(current_page)
                await message.edit(embed=embed)
                await message.clear_reactions()
                for emoji in valid_emojis[:len(chunk)] + nav_emojis:
                    await message.add_reaction(emoji)

        except Exception:
            break

IMAGE_FOLDER = "images"     
USER_IMAGE_FOLDER = "user_images"      

@bot.command(name='meme')
async def meme(ctx):
    # Get all meme images
    images = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))]

    if len(images) < 1:
        await ctx.send("❌ Tidak ada gambar meme yang tersedia.")
        return

    selected_image = random.choice(images)
    source_path = os.path.join(IMAGE_FOLDER, selected_image)

    # Create user's personal folder
    user_id = str(ctx.author.id)
    user_folder = os.path.join(USER_IMAGE_FOLDER, user_id)
    os.makedirs(user_folder, exist_ok=True)

    destination_path = os.path.join(user_folder, selected_image)

    # Save image if not already collected
    if not os.path.exists(destination_path):
        shutil.copyfile(source_path, destination_path)
        status_msg = "📥 Gambar baru ditambahkan ke koleksimu!"
    else:
        status_msg = "✅ Gambar ini sudah ada di koleksimu."

    # Send the image to the user
    file = discord.File(source_path, filename=selected_image)
    await ctx.send(f"🖼️ `{selected_image}`\n{status_msg}", file=file)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')

link1 = "Jika anda mau belajar lebih lanjut tentang perubahan iklim, klik link berikut :) [video](https://youtu.be/J4Zwc6UzxAg)"
link2 = "Jika anda mau belajar lebih lanjut tentang perubahan iklim, klik link berikut: [video](https://youtu.be/kyqy6XiqWx4?si=Pkn5tYfp5plXXA9w)"

@bot.command(name='learn')
async def send_link(ctx):
    link=random.randint(1,3)
    if link == 1:
        message = await ctx.send(link1)
        await message.edit(suppress=True)
    else:
        message = await ctx.send(link2)
        await message.edit(suppress=True)

@bot.command(name="saveimage")
async def save_image(ctx):
    attachments = ctx.message.attachments

    if not attachments:
        await ctx.send("❌ Tidak ada gambar yang dilampirkan. Silakan lampirkan gambar dan jalankan `!saveimage`.")
        return

    for attachment in attachments:
        if attachment.content_type and attachment.content_type.startswith("image/"):
            save_path = os.path.join(SAVE_DIRECTORY, attachment.filename)
            await attachment.save(save_path)
            await ctx.send(f"✅ Gambar `{attachment.filename}` telah disimpan di `{save_path}`.")

            result = get_class(save_path)

            await ctx.send(f"Gamber yang anda kirim adalah `{result}`.")
        else:
            await ctx.send(f"⚠️ File `{attachment.filename}` bukan gambar dan tidak disimpan.")

bot.run("token")