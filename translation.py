translations={

    'ru':{
        "Tilni o'zgartirish":"Смена языка",
        'Tilni tanlang':'Выберите язык',
        'Texnik yordamga xabar yozish':'Написание сообщения в службу технической поддержки',
        "Juda ko'p so'rovlar!":'Слишком много запросов!',
        "Texnik yordam bilan bog'lanmoqchimisiz? Quyidagi tugmani bosing":"Хотите связаться со службой технической поддержки? Нажмите кнопку ниже",
        "Javob yozish uchun shu tugmani bosing":"Нажмите эту кнопку, чтобы написать ответ",
        "Texnik yordamga ga xabar yozing":"Напишите сообщение в службу технической поддержки",
        "Pastki tugmani bosip Savolni to'liq yozing har qanday shaklda audio , rasm , video. Nomerinigiz bilan!":"Напишите полный вопрос , нажав на нижнюю кнопку аудио , фото, видео в любом виде. С вашим номером!",
        "Sizga xat! Quyidagi tugmani bpyosish orqali javob berishingiz mumkin":"Письмо тебе! Вы можете ответить, нажав кнопку ниже",
        'Xizmatimizdan foydalananangiz uchun rahmat\n/start - Savolni yuborish uchun,/help - Biz haqimizda':'Спасибо за использование нашего сервиса\n/start - отправить вопрос, /help - о нас',
        'Yuqoridagi tugmalardan birini tanlang':'Выберите одну из кнопок вверху',
        'Raqamingizni yuborish uchun pastdagi tugmani bosing':'Нажмите кнопку ниже, чтобы отправить свой номер',
        'Tugmani bosing':'Нажмите кнопку',
        "Siz yubormoqchi bo'lgan savolingizni to'liq shaklda yuboring":"Отправьте вопрос, который вы хотите отправить, в полной форме",
        "Operator bilan /taklif ni bosip boglansez boladi":"Operator bilan /ask ni bosip boglansez boladi",
        "sizni savolingiz bizning operatorlarga yuborildi yaqin orada sizga javob beramiz":"ваш вопрос был отправлен нашим операторам мы ответим вам в ближайшее время",
        "Pastdagi tugmani bosing tugmani bosing":"Нажмите кнопку внизу Нажмите кнопку",
        "Ro'yxatdan o'tdingiz":"Вы прошли регистрацию ",
        "Biz haqimizda":"О нас",
        "\nYana savol bolsa /taklif buyrugini ishlating":"Снова запустите команду / ask, если у вас есть вопрос",
        "Telefon raqam noto'g'ri kiritildi, iltimos telefon raqamni +998XXXXXXXX formatda kiriting yoki 'Kontakni yuborish' tugmasiga bosing.":'Номер телефона вставлен неправильно, пожалуйста отправьте номер телефона в формате +998XXXXXXXXX или нажмите на кнопку "Отправить контакт"',
        "Ro'yxatdan muvaffaqiyatli o'tdingiz!":"Вы успешно прошли регистрацию!",
        "Buyruqlar ro'yxati bilan tanishish uchun /help ni bosing.":"Чтобы ознакомиться с командами нажмите на /help",
        "Buyruqlar ro'yxati:\n/taklif - Texnik yordamga habar yozish\n/change_language - Tilni o'zgartish\n/about - Centris Towers haqida bilish":"Список команд:\n/ask - Написать в техническую поддержку\n/change_language - Изменить язык\n/about - Узнать про Centris Towers",
        "Savolingizni yoki murojatingizni 1 ta habar orqali yuboring.":"Отправьте свой вопрос или обращение 1-им сообщением",
        "Savolingiz / Murojatingiz bizning operatorlarga yuborildi, yaqin orada sizga javob beramiz!":"Ваш вопрос / обращение было отправлено нашим операторам, вам скоро ответят!",
        "Iltimos operator javobini kuting!":"Пожалуйста ожидайте ответа оператора!",
        "Yana savolingiz yoki murojatingiz bo'lsa, /taklif orqali berishingiz mumkin.":"Если у вас еще есть вопросы или обращение, нажмите на /ask.",
        "Centris Tower - innovatsiya va zamonaviy uslub gullab-yashnaydigan yangi avlod biznes markazi\n\nMuvaffaqiyatli biznesingizning kaliti bo'ladigan hashamatli ish joyingizni kashf eting.":'Centris Tower-бизнес-центр нового поколения, в котором процветают инновации и современный стиль\n\n откройте для себя свое роскошное рабочее место, которое станет ключом к вашему успешному бизнесу.',

        "Texnik yordamga habar yozish":"Написать в техническую поддержку",
        "Tilni o'zgartish":"Изменить язык",
        "Centris Towers haqida bilish":"Узнать про Centris Towers",
        "Centris Towers bilan bog'lanish":"Связь с Centris Towers",
        "Takliflarni yuborish":"Отправка предложений",
    }

}

def _(text,lang='uz'):
    if lang=='uz':
        return text
    else:
        try:
            return translations[lang][text]
        except:
            return text