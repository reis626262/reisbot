from telethon import TelegramClient, events
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

# Ortam değişkenlerinden API bilgilerini al
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
phone_number = os.getenv("PHONE_NUMBER")

# Hedef grup (mesajların iletileceği yer)
hedef_grup = 'canavarozel'  # kullanıcı adıysa get_entity ile çözülmeli

# Mesajları dinlenecek gruplar
kaynak_gruplar = [
    -5083491813,
    'bgitkazandirir',
    'odeon_sosyal',
    'megasosyal',
    'holigantg',
    'artemisresmi',
    'nakitresmi',
    'sekaresmi',
    'mavi_sosyal',
    'havanabetcom',
    'dogrusun7'
]

# Filtre kelimeleri
filtre_kelimeler = [
    'özel oran', 'Özel Oran', 'Özel oran', 'maksimum',
    'Özel Oranlara', 'ÖZEL ORAN', 'MEGA ORAN'
]

client = TelegramClient('baran_session', api_id, api_hash)

@client.on(events.NewMessage(chats=kaynak_gruplar))
async def mesaj_yakala(event):
    mesaj = event.message.message
    if any(kelime.lower() in mesaj.lower() for kelime in filtre_kelimeler):
        hedef = await client.get_entity(hedef_grup)

        if event.message.media:
            # Medya varsa → dosya ile birlikte gönder
            await client.send_file(hedef, event.message.media, caption=mesaj)
        else:
            # Sadece metin varsa → markdown ile gönder
            await client.send_message(hedef, mesaj, parse_mode='markdown')

async def main():
    await client.connect()
    if not await client.is_user_authorized():
        print("Oturum geçersiz, yeniden giriş gerekli.")
        return
    print("Bot çalışıyor...")
    await client.run_until_disconnected()

client.loop.run_until_complete(main())

