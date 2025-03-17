from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста

support_ids = [
    env.str("operator")
]
