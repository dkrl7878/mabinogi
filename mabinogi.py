import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import pytz

intents = discord.Intents.default()
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)
scheduler = AsyncIOScheduler()

# 설정값
CHANNEL_ID = 1368110243183198219  # 여기에 알림을 보낼 채널 ID 입력
ROLE_ID = 1369246211315339326     # 여기에 멘션할 역할 ID 입력
TIMEZONE = 'Asia/Seoul'          # 한국 시간대

# 알람을 보낼 시간대 (3시간 간격, 10분 전)
ALERT_HOURS = [2, 5, 8, 11, 14, 17, 20, 23]  # 실제 알림 전송 시간

@bot.event
async def on_ready():
    print(f"✅ 로그인 완료: {bot.user}")
    scheduler.start()

    for hour in ALERT_HOURS:
        scheduler.add_job(
            send_reminder,
            'cron',
            hour=hour,
            minute=50,
            timezone=pytz.timezone(TIMEZONE)
        )
    print("📆 알림 스케줄 등록 완료.")

async def send_reminder():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(f"<@&{ROLE_ID}> 결계 시작 10분 전 입니다.")
    else:
        print("❌ 채널을 찾을 수 없습니다.")

bot.run('')
