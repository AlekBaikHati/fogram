import nest_asyncio  # Tambahkan ini
nest_asyncio.apply()  # Terapkan nest_asyncio

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import logging
import asyncio
import os
import tempfile

# Konfigurasi bot
API_TOKEN = ''

# Daftar ID atau username channel target dalam format horizontal
TARGET = []  # Kosongkan variabel ini

# Contoh pengisian variabel TARGET
# TARGET = ['-1002244853686']  # Contoh untuk satu ID
# TARGET = ['-1002373313541', '-1002254821058']  # Contoh untuk banyak ID

# Daftar ID atau username admin yang diizinkan
ADMIN = []  # Kosongkan variabel ini

# Contoh pengisian variabel ADMIN
# ADMIN = ['wiburich']  # Contoh untuk satu admin
# ADMIN = ['wiburich', 'Ghsd77', 'username3']  # Contoh untuk banyak admin

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Tambahkan handler untuk log
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Set logging level for httpx to WARNING to suppress 200 OK messages
httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.WARNING)

# Variabel status untuk mode operasi dan mode penerusan
mode_auto = False  # Default ke mode auto
mode_remof = False # Default ke mode penanda

# Tambahkan variabel untuk menyimpan konten terakhir
last_status_message_content = ""

# Fungsi untuk memeriksa otorisasi
def is_authorized(user):
    return user.username in ADMIN or str(user.id) in ADMIN

# Fungsi untuk memulai bot dengan pesan sambutan
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("REPO", url="https://github.com/AlekBaikHati/forward-bot-telegram")],
        [InlineKeyboardButton("FATHER", url="https://t.me/Zerozerozoro")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        'Selamat datang di F̶̢̉͝O̷̧̡̙̹̥̱̹͈̯͗̌R̸̡̰̯̥͙̘̩̀̅̊̇̈́̕W̶͕̬̻͎̜͑́͋A̴̦̘͎̾̊̉̋̄͊̏Ṙ̸̢̫̥̦̦̌̊̂D̸͉̾̆̄̕ ̷͕̗͇̿̽̂̍͠͝B̴͍̪̮͕͒̐́̄͂͜͠͝͝͠͝Ở̶̳̿̑̕T̵̳̭͉̄̓̾̓̄̀̀̄ͅ ̴̡͓̥̬͂̊͆͌̉̈́̓͠͝T̴̟̦̟͕͆͂͒́̊͝É̸̢̺͉͎̩̮̪̂̑͐͐̊̌͊͆̅L̴̨̯͍̞̞̩̞̯̀̈̋͋́͐̚̕Ȩ̸̢̺̲͉̰͚̭͔͒̀͝G̶̢̧̢̻̜̮̳̝̞̱̈́̑̅̑̍̍̽̓R̶̫͍͇̯̔̆̕Ą̷̰̭͚͔̖͉͙̇͒̏̐̋͗̀͠M̷̧͔͚̠͉͔͈̝̗͇̈̃̓̎̚! Gunakan /settings untuk mengatur mode.',
        reply_markup=reply_markup
    )

# Fungsi untuk mengatur mode bot
async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_authorized(update.effective_user):
        await update.message.reply_text('Anda tidak diizinkan untuk menggunakan bot ini.')
        return

    # Kirim pesan baru untuk memilih mode dengan foto
    photo_url = "https://ibb.co.com/4gKR86LC"  # URL gambar yang ingin Anda sertakan
    await update.message.reply_photo(
        photo=photo_url,
        caption='F̶̢̉͝O̷̧̡̙̹̥̱̹͈̯͗̌R̸̡̰̯̥͙̘̩̀̅̊̇̈́̕W̶͕̬̻͎̜͑́͋A̴̦̘͎̾̊̉̋̄͊̏Ṙ̸̢̫̥̦̦̌̊̂D̸͉̾̆̄̕ ̷͕̗͇̿̽̂̍͠͝B̴͍̪̮͕͒̐́̄͂͜͠͝͝͠͝Ở̶̳̿̑̕T̵̳̭͉̄̓̾̓̄̀̀̄ͅ ̴̡͓̥̬͂̊͆͌̉̈́̓͠͝T̴̟̦̟͕͆͂͒́̊͝É̸̢̺͉͎̩̮̪̂̑͐͐̊̌͊͆̅L̴̨̯͍̞̞̩̞̯̀̈̋͋́͐̚̕Ȩ̸̢̺̲͉̰͚̭͔͒̀͝G̶̢̧̢̻̜̮̳̝̞̱̈́̑̅̑̍̍̽̓R̶̫͍͇̯̔̆̕Ą̷̰̭͚͔̖͉͙̇͒̏̐̋͗̀͠M̷̧͔͚̠͉͔͈̝̗͇̈̃̓̎̚\n\n' + await get_active_mode_text(),
        reply_markup=await create_mode_keyboard()
    )

# Fungsi untuk mendapatkan teks mode aktif
async def get_active_mode_text() -> str:
    active_mode = []
    if mode_auto:
        active_mode.append("✅ AUTO")
    else:
        active_mode.append("✅ MANUAL")

    if mode_remof:
        active_mode.append("✅ REMOVE TAG")
    else:
        active_mode.append("✅ WITH TAG")

    return "Active Mode:\n" + "\n".join(active_mode)

# Fungsi untuk membuat keyboard mode
async def create_mode_keyboard() -> InlineKeyboardMarkup:
    # Tentukan emoji penanda
    auto_emoji = "📌" if mode_auto else ""
    manual_emoji = "📌" if not mode_auto else ""
    penanda_emoji = "📌" if not mode_remof else ""
    remov_emoji = "📌" if mode_remof else ""

    # Buat tombol inline
    keyboard = [
        [InlineKeyboardButton(f"{auto_emoji}AUTO", callback_data='set_auto'),
         InlineKeyboardButton(f"{manual_emoji}MANUAL", callback_data='set_manual')],
        [InlineKeyboardButton(f"{penanda_emoji}WITH TAG", callback_data='set_penanda'),
         InlineKeyboardButton(f"{remov_emoji}REMOVE TAG", callback_data='set_remov')],
        [InlineKeyboardButton("TUTUP", callback_data='close')]
    ]
    return InlineKeyboardMarkup(keyboard)

# Fungsi untuk menangani pesan
async def forward_post(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_authorized(update.effective_user):
        await update.message.reply_text('Anda tidak diizinkan untuk menggunakan bot ini.')
        return

    message = update.message or update.channel_post  # Tangani pesan dari user atau channel
    if not message:
        return

    if mode_auto:
        await forward_post_auto(update, context)  # Panggil fungsi untuk mode auto
    else:
        await forward_post_manual(update, context)  # Panggil fungsi untuk mode manual

# Fungsi untuk menangani pesan dalam mode auto
async def forward_post_auto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message or update.channel_post  # Tangani pesan dari user atau channel
    if not message:
        return

    action = "pengcopyan" if mode_remof else "penerusan"
    status_message = await message.reply_text(f'Memulai {action} pesan...', reply_to_message_id=message.message_id)
    error_channels = []
    success_channels = []
    total_channels = len(TARGET)

    # Tampilkan loading sederhana untuk 0%
    await status_message.edit_text(f"{action.capitalize()} pesan: 0%")
    last_status_message_content = f"{action.capitalize()} pesan: 0%"

    for index, target in enumerate(TARGET):
        try:
            if mode_remof:
                await context.bot.copy_message(chat_id=target, from_chat_id=message.chat_id, message_id=message.message_id)
            else:
                await context.bot.forward_message(chat_id=target, from_chat_id=message.chat_id, message_id=message.message_id)
            success_channels.append(target)
        except Exception as e:
            logger.error(f'Gagal meneruskan pesan ke {target}: {e}')
            error_channels.append(target)

        # Update progress setiap 10%
        progress = int((index + 1) / total_channels * 100)
        progress_bar = '█' * (progress // 10) + '▒' * (10 - (progress // 10))  # Membuat bar progres
        new_content = f"{action.capitalize()} pesan: {progress_bar} {progress}%"
        if new_content != last_status_message_content:  # Periksa apakah konten baru berbeda
            await status_message.edit_text(new_content)
            last_status_message_content = new_content  # Update konten terakhir

    # Pastikan persentase ditampilkan sebagai 100% jika sudah selesai
    final_content = f"{action.capitalize()} pesan: 100%"
    if final_content != last_status_message_content:  # Periksa apakah konten baru berbeda
        await status_message.edit_text(final_content)
        last_status_message_content = final_content  # Update konten terakhir

    # Summary of forwarding
    summary_message = f"{action.capitalize()} pesan selesai.\n"
    if success_channels:
        summary_message += f"Berhasil {action} ke: {', '.join(success_channels)}\n"
    if error_channels:
        summary_message += f"Gagal {action} ke: {', '.join(error_channels)}"

    await status_message.edit_text(summary_message)

# Fungsi untuk menangani pesan dalam mode manual
async def forward_post_manual(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message or update.channel_post  # Tangani pesan dari user atau channel
    if not message:
        return

    # Mode manual, tampilkan tombol konfirmasi
    keyboard = [
        [InlineKeyboardButton("Ya", callback_data=f'confirm_forward:{message.message_id}'),
         InlineKeyboardButton("Tidak", callback_data='cancel_forward')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await message.reply_text('Apakah Anda ingin meneruskan pesan ini?', reply_markup=reply_markup, reply_to_message_id=message.message_id)

# Fungsi untuk menangani tombol konfirmasi
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global mode_auto, mode_remof
    query = update.callback_query
    data = query.data

    # Menjawab callback query dengan alert jika mode sudah aktif
    if data == 'set_auto':
        if mode_auto:
            await query.answer(text="Mode AUTO sudah aktif.✨", show_alert=True)
        else:
            mode_auto = True
            mode_remof = False  # Pastikan mode REMOV dinonaktifkan saat beralih ke AUTO
            await query.answer(text="Mode diubah ke AUTO.✨", show_alert=True)
            new_text = 'F̶̢̉͝O̷̧̡̙̹̥̱̹͈̯͗̌R̸̡̰̯̥͙̘̩̀̅̊̇̈́̕W̶͕̬̻͎̜͑́͋A̴̦̘͎̾̊̉̋̄͊̏Ṙ̸̢̫̥̦̦̌̊̂D̸͉̾̆̄̕ ̷͕̗͇̿̽̂̍͠͝B̴͍̪̮͕͒̐́̄͂͜͠͝͝͠͝Ở̶̳̿̑̕T̵̳̭͉̄̓̾̓̄̀̀̄ͅ ̴̡͓̥̬͂̊͆͌̉̈́̓͠͝T̴̟̦̟͕͆͂͒́̊͝É̸̢̺͉͎̩̮̪̂̑͐͐̊̌͊͆̅L̴̨̯͍̞̞̩̞̯̀̈̋͋́͐̚̕Ȩ̸̢̺̲͉̰͚̭͔͒̀͝G̶̢̧̢̻̜̮̳̝̞̱̈́̑̅̑̍̍̽̓R̶̫͍͇̯̔̆̕Ą̷̰̭͚͔̖͉͙̇͒̏̐̋͗̀͠M̷̧͔͚̠͉͔͈̝̗͇̈̃̓̎̚\n\n' + await get_active_mode_text()
            await query.message.edit_caption(new_text, reply_markup=await create_mode_keyboard())
    elif data == 'set_manual':
        if not mode_auto:
            await query.answer(text="Mode MANUAL sudah aktif.✨", show_alert=True)
        else:
            mode_auto = False  # Ubah ke mode manual
            await query.answer(text="Mode diubah ke MANUAL.✨", show_alert=True)
            new_text = 'F̶̢̉͝O̷̧̡̙̹̥̱̹͈̯͗̌R̸̡̰̯̥͙̘̩̀̅̊̇̈́̕W̶͕̬̻͎̜͑́͋A̴̦̘͎̾̊̉̋̄͊̏Ṙ̸̢̫̥̦̦̌̊̂D̸͉̾̆̄̕ ̷͕̗͇̿̽̂̍͠͝B̴͍̪̮͕͒̐́̄͂͜͠͝͝͠͝Ở̶̳̿̑̕T̵̳̭͉̄̓̾̓̄̀̀̄ͅ ̴̡͓̥̬͂̊͆͌̉̈́̓͠͝T̴̟̦̟͕͆͂͒́̊͝É̸̢̺͉͎̩̮̪̂̑͐͐̊̌͊͆̅L̴̨̯͍̞̞̩̞̯̀̈̋͋́͐̚̕Ȩ̸̢̺̲͉̰͚̭͔͒̀͝G̶̢̧̢̻̜̮̳̝̞̱̈́̑̅̑̍̍̽̓R̶̫͍͇̯̔̆̕Ą̷̰̭͚͔̖͉͙̇͒̏̐̋͗̀͠M̷̧͔͚̠͉͔͈̝̗͇̈̃̓̎̚\n\n' + await get_active_mode_text()
            await query.message.edit_caption(new_text, reply_markup=await create_mode_keyboard())
    elif data == 'set_penanda':
        if not mode_remof:
            await query.answer(text="Mode WITH TAG sudah aktif.✨", show_alert=True)
        else:
            mode_remof = False  # Ubah ke mode penanda
            await query.answer(text="Mode diubah ke WITH TAG.✨", show_alert=True)
            new_text = 'F̶̢̉͝O̷̧̡̙̹̥̱̹͈̯͗̌R̸̡̰̯̥͙̘̩̀̅̊̇̈́̕W̶͕̬̻͎̜͑́͋A̴̦̘͎̾̊̉̋̄͊̏Ṙ̸̢̫̥̦̦̌̊̂D̸͉̾̆̄̕ ̷͕̗͇̿̽̂̍͠͝B̴͍̪̮͕͒̐́̄͂͜͠͝͝͠͝Ở̶̳̿̑̕T̵̳̭͉̄̓̾̓̄̀̀̄ͅ ̴̡͓̥̬͂̊͆͌̉̈́̓͠͝T̴̟̦̟͕͆͂͒́̊͝É̸̢̺͉͎̩̮̪̂̑͐͐̊̌͊͆̅L̴̨̯͍̞̞̩̞̯̀̈̋͋́͐̚̕Ȩ̸̢̺̲͉̰͚̭͔͒̀͝G̶̢̧̢̻̜̮̳̝̞̱̈́̑̅̑̍̍̽̓R̶̫͍͇̯̔̆̕Ą̷̰̭͚͔̖͉͙̇͒̏̐̋͗̀͠M̷̧͔͚̠͉͔͈̝̗͇̈̃̓̎̚\n\n' + await get_active_mode_text()
            await query.message.edit_caption(new_text, reply_markup=await create_mode_keyboard())
    elif data == 'set_remov':
        if mode_remof:
            await query.answer(text="Mode REMOVE TAG sudah aktif.✨", show_alert=True)
        else:
            mode_remof = True  # Ubah ke mode REMOV
            await query.answer(text="Mode diubah ke REMOVE TAG.✨", show_alert=True)
            new_text = 'F̶̢̉͝O̷̧̡̙̹̥̱̹͈̯͗̌R̸̡̰̯̥͙̘̩̀̅̊̇̈́̕W̶͕̬̻͎̜͑́͋A̴̦̘͎̾̊̉̋̄͊̏Ṙ̸̢̫̥̦̦̌̊̂D̸͉̾̆̄̕ ̷͕̗͇̿̽̂̍͠͝B̴͍̪̮͕͒̐́̄͂͜͠͝͝͠͝Ở̶̳̿̑̕T̵̳̭͉̄̓̾̓̄̀̀̄ͅ ̴̡͓̥̬͂̊͆͌̉̈́̓͠͝T̴̟̦̟͕͆͂͒́̊͝É̸̢̺͉͎̩̮̪̂̑͐͐̊̌͊͆̅L̴̨̯͍̞̞̩̞̯̀̈̋͋́͐̚̕Ȩ̸̢̺̲͉̰͚̭͔͒̀͝G̶̢̧̢̻̜̮̳̝̞̱̈́̑̅̑̍̍̽̓R̶̫͍͇̯̔̆̕Ą̷̰̭͚͔̖͉͙̇͒̏̐̋͗̀͠M̷̧͔͚̠͉͔͈̝̗͇̈̃̓̎̚\n\n' + await get_active_mode_text()
            await query.message.edit_caption(new_text, reply_markup=await create_mode_keyboard())
    elif data == 'close':
        await query.message.delete()
        return
    elif data.startswith('confirm_forward:'):
        # Panggil fungsi untuk meneruskan pesan
        await confirm_forward(update, context)
    elif data == 'cancel_forward':
        # Hapus pesan konfirmasi
        await cancel_forward(update, context)

# Fungsi untuk menangani konfirmasi meneruskan pesan
async def confirm_forward(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data = query.data.split(':')
    message_id = int(data[1])

    action = "pengcopyan" if mode_remof else "penerusan"
    status_message = await query.message.reply_text(f'Memulai {action} pesan...', reply_to_message_id=message_id)
    error_channels = []
    success_channels = []
    total_channels = len(TARGET)

    # Tampilkan loading sederhana untuk 0%
    await status_message.edit_text(f"{action.capitalize()} pesan: 0%")
    last_status_message_content = f"{action.capitalize()} pesan: 0%"

    for index, target in enumerate(TARGET):
        try:
            if mode_remof:
                await context.bot.copy_message(chat_id=target, from_chat_id=query.message.chat_id, message_id=message_id)
            else:
                await context.bot.forward_message(chat_id=target, from_chat_id=query.message.chat_id, message_id=message_id)
            success_channels.append(target)
        except Exception as e:
            logger.error(f'Gagal meneruskan pesan ke {target}: {e}')
            error_channels.append(target)

        # Update progress setiap 10%
        progress = int((index + 1) / total_channels * 100)
        progress_bar = '█' * (progress // 10) + '▒' * (10 - (progress // 10))  # Membuat bar progres
        new_content = f"{action.capitalize()} pesan: {progress_bar} {progress}%"
        if new_content != last_status_message_content:  # Periksa apakah konten baru berbeda
            await status_message.edit_text(new_content)
            last_status_message_content = new_content  # Update konten terakhir

    # Pastikan persentase ditampilkan sebagai 100% jika sudah selesai
    final_content = f"{action.capitalize()} pesan: 100%"
    if final_content != last_status_message_content:  # Periksa apakah konten baru berbeda
        await status_message.edit_text(final_content)
        last_status_message_content = final_content  # Update konten terakhir

    # Summary of forwarding
    summary_message = f"{action.capitalize()} pesan selesai.\n"
    if success_channels:
        summary_message += f"Berhasil {action} ke: {', '.join(success_channels)}\n"
    if error_channels:
        summary_message += f"Gagal {action} ke: {', '.join(error_channels)}"

    await status_message.edit_text(summary_message)
    await query.message.delete()  # Hapus pesan tombol setelah selesai

# Fungsi untuk menangani pembatalan
async def cancel_forward(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.message.delete()  # Hapus pesan konfirmasi

# Fungsi untuk menampilkan informasi channel
async def list_channels(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_authorized(update.effective_user):
        await update.message.reply_text('Anda tidak diizinkan untuk menggunakan bot ini.')
        return

    bot = context.bot
    status_message = await update.message.reply_text('Memuat daftar channel...')
    total_channels = len(TARGET)
    default_photo_url = "https://ibb.co.com/5gWGBtv1"  # URL gambar default

    # Pastikan folder 'Profil' ada
    os.makedirs('Profil', exist_ok=True)

    # Tampilkan loading sederhana untuk 0%
    await status_message.edit_text(f"Memuat daftar: 0%")

    for index, channel_id in enumerate(TARGET):
        try:
            chat = await bot.get_chat(chat_id=channel_id)
            link = f"https://t.me/{chat.username}" if chat.username else "Link tidak tersedia"
            info = (
                "✦•┈๑⋅⋯ ⋯⋅๑┈•✦\n"
                f"Channel ID: {chat.id}\n"
                f"Nama Channel: {chat.title}\n"
                f"Username Channel: {chat.username}\n"
                f"Jumlah Anggota: {await chat.get_member_count()}\n"
                f"Link Channel: {link}\n"
                "✦•┈๑⋅⋯ ⋯⋅๑┈•✦\n"
            )

            # Cek apakah channel memiliki foto profil
            if chat.photo:
                file = await bot.get_file(chat.photo.big_file_id)
                file_path = os.path.join('Profil', f"{channel_id}.jpg")
                await file.download_to_drive(custom_path=file_path)
                await bot.send_photo(chat_id=update.effective_chat.id, photo=open(file_path, 'rb'), caption=info)
                os.remove(file_path)  # Hapus file setelah dikirim
            else:
                await bot.send_photo(chat_id=update.effective_chat.id, photo=default_photo_url, caption=info)
        except Exception as e:
            await update.message.reply_text(f"Gagal mengakses channel {channel_id}: {e}")

        # Update progress setiap 10%
        progress = int((index + 1) / total_channels * 100)
        progress_bar = '█' * (progress // 10) + '▒' * (10 - (progress // 10))  # Membuat bar progres
        await status_message.edit_text(f"Memuat daftar: {progress_bar} {progress}%")

    await status_message.delete()  # Hapus pesan loading setelah selesai
    await update.message.reply_text(f'Daftar channel berhasil dimuat. Total channel: {total_channels}.', quote=True)  # Tambahkan pesan sukses dengan format quote

# Fungsi untuk menampilkan informasi channel tanpa foto
async def list_channels_no_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_authorized(update.effective_user):
        await update.message.reply_text('Anda tidak diizinkan untuk menggunakan bot ini.')
        return

    bot = context.bot
    status_message = await update.message.reply_text('Memuat daftar channel tanpa foto...')
    total_channels = len(TARGET)

    # Tampilkan loading sederhana untuk 0%
    await status_message.edit_text(f"Memuat daftar tanpa foto: 0%")

    for index, channel_id in enumerate(TARGET):
        try:
            chat = await bot.get_chat(chat_id=channel_id)
            link = f"https://t.me/{chat.username}" if chat.username else "Link tidak tersedia"
            info = (
                "⋆˖⁺‧₊☽◯☾₊‧⁺˖⋆\n"
                f"Channel ID: {chat.id}\n"
                f"Nama Channel: {chat.title}\n"
                f"Username Channel: {chat.username}\n"
                f"Jumlah Anggota: {await chat.get_member_count()}\n"
                f"Link Channel: {link}\n"
                "✦•┈๑⋅⋯ ⋯⋅๑┈•✦\n"
            )
            await update.message.reply_text(info)
        except Exception as e:
            await update.message.reply_text(f"Gagal mengakses channel {channel_id}: {e}")

        # Update progress setiap 10%
        progress = int((index + 1) / total_channels * 100)
        progress_bar = '█' * (progress // 10) + '▒' * (10 - (progress // 10))  # Membuat bar progres
        await status_message.edit_text(f"Memuat daftar tanpa foto: {progress_bar} {progress}%")

    await status_message.delete()  # Hapus pesan loading setelah selesai
    await update.message.reply_text(f'Daftar channel tanpa foto berhasil dimuat. Total channel: {total_channels}.', quote=True)  # Tambahkan pesan sukses

# Tentukan nama sesi dari variabel lingkungan atau gunakan default
SESSION_NAME = os.getenv('SESSION_NAME', 'forward_session')

# Gunakan nama sesi ini untuk mengatur direktori kerja atau file yang berbeda
session_directory = os.path.join(tempfile.gettempdir(), SESSION_NAME)
os.makedirs(session_directory, exist_ok=True)
logger.info(f"Session directory created at: {session_directory}")

# Contoh penggunaan: menyimpan log atau data di direktori sesi
log_file_path = os.path.join(session_directory, 'bot.log')
logger.info(f"Log file path: {log_file_path}")

# Set up logging dengan file log yang berbeda
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

async def main() -> None:
    # Inisialisasi Application
    application = Application.builder().token(API_TOKEN).build()

    # Daftarkan handler
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("settings", settings))
    application.add_handler(CommandHandler("list", list_channels))
    application.add_handler(CommandHandler("list2", list_channels_no_photo))
    application.add_handler(MessageHandler(filters.ALL, forward_post))
    application.add_handler(CallbackQueryHandler(button))

    # Log saat bot dijalankan
    logger.info("Bot dimulai dan siap menerima pesan.")

    # Jalankan bot
    await application.run_polling()

    # Log saat bot dihentikan
    logger.info("Bot dihentikan.")

if __name__ == '__main__':
    try:
        # Dapatkan event loop yang ada
        loop = asyncio.get_event_loop()
        # Jalankan coroutine main() di dalam event loop yang ada
        loop.run_until_complete(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot dihentikan oleh pengguna.")
