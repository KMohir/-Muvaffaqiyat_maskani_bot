import logging
import asyncio
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart, Command
from aiogram.types import ParseMode, Message, ReplyKeyboardRemove, MediaGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from db import Database, create_database  # Импортируем реальную базу данных

# Replace with your actual Telegram Bot Token
BOT_TOKEN = "6528403005:AAEKDJJDu5S0H2QZrD_NmdV2LKvnDkxlzUk"
ADMIN_ID = 5657091547  # Replace with your actual Admin ID

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Создаем БД, если она не существует
create_database('databaseprotestim.db')
# Используем реальную базу данных вместо MockDB
db = Database('databaseprotestim.db')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Mock database implementation (replace with your actual database logic)


# Translation function (mock implementation)
def _(text, lang):
    return text  # Replace with actual translation logic if needed

# Keyboards
def get_lang_for_button(message):
    return types.ReplyKeyboardMarkup(resize_keyboard=True).add("Support", "About")

def key(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if lang == "uz":
        keyboard.add("Kontaktni yuborish")
    elif lang == "ru":
        keyboard.add("Отправить контакт")
    return keyboard

langMenu = types.InlineKeyboardMarkup(row_width=2)
langMenu.add(
    types.InlineKeyboardButton("🇺🇿 O'zbek", callback_data="lang_uz"),
    types.InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")
)

# States
class RegistrationStates:
    lang = "lang"
    name = "name"
    address = "address"
    status = "status"
    custom_status = "custom_status"
    employees = "employees"
    phone = "phone"

# Start command
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    logger.info(f"User {message.from_user.id} started the bot")
    if not db.user_exists(message.from_user.id):
        await bot.send_message(
            message.from_user.id,
            'Assalomu aleykum, Centris Towers yordamchi botiga hush kelibsiz!\nЗдравствуйте, добро пожаловать в бот поддержки Centris Towers!'
        )
        await bot.send_message(
            message.from_user.id,
            'Tilni tanlang:\nВыберите язык:',
            reply_markup=langMenu
        )
        await RegistrationStates.lang.set()
    else:
        try:
            lang = db.get_lang(message.from_user.id)
            video_path = 'Centris.mp4'  # Ensure this file exists
            caption = (
                _("Centris Tower - innovatsiya va zamonaviy uslub gullab-yashnaydigan yangi avlod biznes markazi\n\nMuvaffaqiyatli biznesingizning kaliti bo'ladigan hashamatli ish joyingizni kashf eting.", lang)
            )
            with open(video_path, 'rb') as video:
                await bot.send_video(
                    chat_id=message.chat.id,
                    video=video,
                    caption='',
                    supports_streaming=True,
                    reply_markup=get_lang_for_button(message)
                )
        except Exception as e:
            logger.error(f"Error sending video to {message.from_user.id}: {e}")
            await bot.send_message(
                message.from_user.id,
                "Buyruqlar ro'yxati:\n/ask - Texnik yordamga habar yozish\n/change_language - Tilni o'zgartish\n/about - Centris Towers haqida bilish",
                reply_markup=get_lang_for_button(message)
            )

# Send image command (Admin only)
@dp.message_handler(Command('send_image'), user_id=ADMIN_ID)
async def send_image_command(message: types.Message, state: FSMContext):
    await message.answer(
        "Iltimos, barcha foydalanuvchilarga jo'natmoqchi bo'lgan rasmlarni yuboring. Tugatganingizdan so'ng /done buyrug'ini kiritin.")
    await state.set_state("waiting_for_images")
    await state.update_data(images=[])

@dp.message_handler(content_types=types.ContentType.PHOTO, state="waiting_for_images")
async def process_image(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Sizda bu buyruqni bajarish uchun ruxsat yo'q.")
        await state.finish()
        return

    data = await state.get_data()
    images = data.get('images', [])
    photo = message.photo[-1]
    images.append(photo.file_id)
    await state.update_data(images=images)
    await message.answer(
        f"Rasm qo'shildi. Jami: {len(images)}. Yana yuboring yoki /done buyrug'i bilan yakunlang.")

@dp.message_handler(Command('done'), state="waiting_for_images")
async def finish_image_collection(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Sizda bu buyruqni bajarish uchun ruxsat yo'q.")
        await state.finish()
        return

    data = await state.get_data()
    images = data.get('images', [])

    if not images:
        await message.answer("Siz birorta ham rasm yubormadingiz.")
        await state.finish()
        return

    total_images = len(images)
    await message.answer(f"Jami {total_images} ta rasm qabul qilindi. Jo'natish boshlanadi...")

    users = db.get_all_users()
    logger.info(f"Found {len(users)} users to send images to")

    chunk_size = 10
    image_chunks = [images[i:i + chunk_size] for i in range(0, len(images), chunk_size)]

    sent_count = 0
    for user_id in users:
        try:
            lang = db.get_lang(user_id)
            caption = _("Administratoridan yangi rasmlar!", lang)
            for chunk in image_chunks:
                media_group = MediaGroup()
                for i, file_id in enumerate(chunk):
                    if i == 0:
                        media_group.attach_photo(file_id, caption=caption)
                    else:
                        media_group.attach_photo(file_id)
                await bot.send_media_group(chat_id=user_id, media=media_group)
                await asyncio.sleep(1)  # Rate limiting
            sent_count += 1
        except Exception as e:
            logger.error(f"Failed to send media group to user {user_id}: {e}")
            continue

    await message.answer(f"{total_images} ta rasmdan media guruhlar {sent_count} foydalanuvchilarga muvaffaqiyatli yuborildi!")
    await state.finish()

@dp.message_handler(state="waiting_for_images")
async def invalid_input(message: types.Message, state: FSMContext):
    await message.answer("Iltimos, rasm yuboring yoki /done buyrug'i bilan kirishni yakunlang.")
    await state.set_state("waiting_for_images")

# Registration process
@dp.callback_query_handler(text_contains="lang_", state=RegistrationStates.lang)
async def set_lang(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    if not db.user_exists(call.from_user.id):
        lang = call.data[5:]
        async with state.proxy() as data:
            data['lang'] = lang

        if lang == 'uz':
            await bot.send_message(call.from_user.id, "Ism familiyangizni kiriting")
        elif lang == 'ru':
            await bot.send_message(call.from_user.id, "Введите свое имя и фамилию")
        await RegistrationStates.name.set()

@dp.message_handler(state=RegistrationStates.name)
async def register_name_handler(message: types.Message, state: FSMContext):
    name = message.text
    async with state.proxy() as data:
        data['name'] = name
        lang = data.get('lang')

    regions_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if lang == "uz":
        regions = [
            "Andijon viloyati", "Buxoro viloyati", "Farg'ona viloyati", "Jizzax viloyati",
            "Xorazm viloyati", "Namangan viloyati", "Navoiy viloyati", "Qashqadaryo viloyati",
            "Samarqand viloyati", "Sirdaryo viloyati", "Surxondaryo viloyati", "Toshkent viloyati",
            "Toshkent shahri"
        ]
        await message.answer("Manzilingizni tanlang:", reply_markup=regions_keyboard.add(*regions))
    elif lang == "ru":
        regions = [
            "Андижанская область", "Бухарская область", "Ферганская область", "Джизакская область",
            "Хорезмская область", "Наманганская область", "Навоийская область", "Кашкадарьинская область",
            "Самаркандская область", "Сырдарьинская область", "Сурхандарьинская область", "Ташкентская область",
            "Город Ташкент"
        ]
        await message.answer("Выберите ваш регион:", reply_markup=regions_keyboard.add(*regions))
    await RegistrationStates.address.set()

@dp.message_handler(state=RegistrationStates.address)
async def register_address_handler(message: types.Message, state: FSMContext):
    address = message.text
    async with state.proxy() as data:
        data['address'] = address
        lang = data.get('lang')

    status_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if lang == "uz":
        status_options = ["Asoschi", "Rahbar", "Top menejer", "Investor", "Boshqa lavozim"]
        await message.answer("Biznesdagi maqom statusingizni tanlang:",
                             reply_markup=status_keyboard.add(*status_options))
    elif lang == "ru":
        status_options = ["Основатель", "Руководитель", "Топ-менеджер", "Инвестор", "Другая должность"]
        await message.answer("Выберите ваш статус в бизнесе:", reply_markup=status_keyboard.add(*status_options))
    await RegistrationStates.status.set()

@dp.message_handler(state=RegistrationStates.status)
async def register_status_handler(message: types.Message, state: FSMContext):
    status = message.text
    async with state.proxy() as data:
        lang = data.get('lang')

    if (lang == "uz" and status == "Boshqa lavozim") or (lang == "ru" and status == "Другая должность"):
        if lang == "uz":
            await message.answer("Iltimos, lavozimingizni qo'lda kiriting:", reply_markup=ReplyKeyboardRemove())
        elif lang == "ru":
            await message.answer("Пожалуйста, введите вашу должность вручную:", reply_markup=ReplyKeyboardRemove())
        await RegistrationStates.custom_status.set()
    else:
        async with state.proxy() as data:
            data['status'] = status
        if lang == "uz":
            await message.answer("Hodimlaringiz sonini kiriting (agar bo'lsa):", reply_markup=ReplyKeyboardRemove())
        elif lang == "ru":
            await message.answer("Введите количество ваших сотрудников (если есть):",
                                 reply_markup=ReplyKeyboardRemove())
        await RegistrationStates.employees.set()

@dp.message_handler(state=RegistrationStates.custom_status)
async def register_custom_status_handler(message: types.Message, state: FSMContext):
    custom_status = message.text
    async with state.proxy() as data:
        data['status'] = custom_status
        lang = data.get('lang')

    if lang == "uz":
        await message.answer("Hodimlaringiz sonini kiriting (agar bo'lsa):")
    elif lang == "ru":
        await message.answer("Введите количество ваших сотрудников (если есть):")
    await RegistrationStates.employees.set()

@dp.message_handler(state=RegistrationStates.employees)
async def register_employees_handler(message: types.Message, state: FSMContext):
    employees = message.text
    async with state.proxy() as data:
        data['employees'] = employees
        lang = data.get('lang')

    if lang == "uz":
        await message.answer("Telefon raqamingizni kiriting", reply_markup=key(lang))
    elif lang == "ru":
        await message.answer("Введите свой номер телефона", reply_markup=key(lang))
    await RegistrationStates.phone.set()

@dp.message_handler(state=RegistrationStates.phone, content_types=types.ContentType.TEXT)
async def process_phone_text(message: Message, state: FSMContext):
    contact = message.text
    async with state.proxy() as data:
        lang = data.get('lang')

    if contact.startswith('+998') and len(contact) == 13:
        await save_user_data(message, state, contact)
    else:
        if lang == "uz":
            await message.answer(
                "Telefon raqam noto'g'ri kiritildi, iltimos telefon raqamni +998XXXXXXXXX formatda kiriting yoki 'Kontakni yuborish' tugmasiga bosing.",
                reply_markup=key(lang))
        elif lang == "ru":
            await message.answer(
                "Номер телефона введен неверно, пожалуйста, введите номер в формате +998XXXXXXXXX или нажмите кнопку 'Отправить контакт'.",
                reply_markup=key(lang))
        await RegistrationStates.phone.set()

@dp.message_handler(state=RegistrationStates.phone, content_types=types.ContentType.CONTACT)
async def process_phone_contact(message: Message, state: FSMContext):
    contact = message.contact.phone_number
    await save_user_data(message, state, contact)

async def save_user_data(message: Message, state: FSMContext, contact: str):
    try:
        async with state.proxy() as data:
            lang = data.get('lang')
            name = data.get('name')
            address = data.get('address')
            status = data.get('status')
            employees = data.get('employees')

            db.update(lang, message.from_user.id, name, contact, address=address, status=status, employees=employees)

            await message.answer(_("Ro'yxatdan muvaffaqiyatli o'tdingiz!", lang), reply_markup=ReplyKeyboardRemove())

            video_path = 'Centris.mp4'  # Ensure this file exists
            caption = (
                _("Centris Tower - innovatsiya va zamonaviy uslub gullab-yashnaydigan yangi avlod biznes markazi\n\nMuvaffaqiyatli biznesingizning kaliti bo'ladigan hashamatli ish joyingizni kashf eting.", lang)
            )
            with open(video_path, 'rb') as video:
                await bot.send_video(
                    chat_id=message.chat.id,
                    video=video,
                    caption='',
                    supports_streaming=True,
                    reply_markup=get_lang_for_button(message)
                )
    except Exception as e:
        logger.error(f"Error saving user data for {message.from_user.id}: {e}")
        await message.answer("Произошла ошибка при регистрации. Пожалуйста, попробуйте снова.")
    finally:
        await state.finish()

# Get all users command (Admin only)
@dp.message_handler(commands=['get_all_users'], user_id=ADMIN_ID)
async def get_all_users_command(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.reply("Sizda bu buyruqni bajarish uchun ruxsat yo'q.")
        return

    users_data = db.get_all_users_data()

    if not users_data:
        await message.reply("Foydalanuvchilar bazada mavjud emas.")
        return

    response = "Foydalanuvchilar ro'yxati:\n\n"
    for user in users_data:
        user_id, lang, name, phone, address, status, employees = user
        response += (
            f"User ID: {user_id}\n"
            f"Til: {lang}\n"
            f"Ism: {name or 'Belgilanmagan'}\n"
            f"Telefon: {phone or 'Belgilanmagan'}\n"
            f"Manzil: {address or 'Belgilanmagan'}\n"
            f"Status: {status or 'Belgilanmagan'}\n"
            f"Xodimlar: {employees or 'Belgilanmagan'}\n"
            "------------------------\n"
        )

    if len(response) > 4096:
        for i in range(0, len(response), 4096):
            await message.reply(response[i:i + 4096])
    else:
        await message.reply(response)

# Main execution
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)