from discord.ext import commands, tasks
import requests, discord
import asyncio
import random, os

# Danh sách các loại ảnh (sfw)
sfw_categories = ["waifu", "neko", "trap", "blowjob"]

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Kênh gửi ảnh tự động
CHANNEL_ID = [1170009154648293388, 1294120124818653228] # Thay thế bằng ID kênh mong muốn

# --- Kênh cho phép cho command ---
ALLOWED_CHANNEL_IDS = CHANNEL_ID # Thay thế bằng ID kênh mong muốn

# --- Kiểm tra kênh cho command---
def is_allowed_channel():
    """Decorator kiểm tra kênh cho phép."""
    async def predicate(ctx):
        return ctx.channel.id in ALLOWED_CHANNEL_IDS
    return commands.check(predicate)


@tasks.loop(seconds=10)  # Chạy mỗi 10 giây
async def send_waifu_image():
    try:
        # Chọn ngẫu nhiên một loại ảnh
        category = random.choice(sfw_categories)

        # Gọi API để lấy URL ảnh
        response = requests.get(f"https://api.waifu.pics/nsfw/{category}")
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        image_url = response.json()["url"]

        # Lấy kênh từ ID
        channel = bot.get_channel(CHANNEL_ID)
        if channel is None:
            print(f"Không tìm thấy kênh có ID {CHANNEL_ID}")
            return

        # Gửi ảnh
        await channel.send(image_url)

    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gọi API: {e}")
    except Exception as e:
        print(f"Lỗi khác: {e}")


@bot.command(name="send_waifu")
@is_allowed_channel()
async def send_waifu_command(ctx):
    try:
        # Chọn ngẫu nhiên một loại ảnh
        category = random.choice(sfw_categories)

        # Gọi API để lấy URL ảnh
        response = requests.get(f"https://api.waifu.pics/nsfw/{category}")
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        image_url = response.json()["url"]

        # Gửi ảnh
        await ctx.send(image_url)

    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gọi API: {e}")
        await ctx.send("Lỗi khi lấy ảnh.")
    except Exception as e:
        print(f"Lỗi khác: {e}")
        await ctx.send("Đã xảy ra lỗi.")



@bot.event
async def on_ready():
    print(f"{bot.user} đã kết nối!")
    send_waifu_image.start()  # Khởi động task

bot.run(os.getenv('HAITEN'))