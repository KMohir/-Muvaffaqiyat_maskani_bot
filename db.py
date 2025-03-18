import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_database(db_file):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS support (
                        id        INTEGER PRIMARY KEY AUTOINCREMENT,
                        questions TEXT    NOT NULL,
                        answer    TEXT
                        );""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS userquestions (
                            id       INTEGER PRIMARY KEY AUTOINCREMENT,
                            userid   INTEGER NOT NULL,
                            question TEXT);""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                            id       INTEGER      PRIMARY KEY AUTOINCREMENT,
                            user_id  INTEGER (11) UNIQUE,
                            lang     TEXT         NOT NULL DEFAULT 'uz',
                            name     TEXT,
                            phone    TEXT,
                            address  TEXT,
                            status   TEXT,
                            employees TEXT
                        );""")
        conn.commit()
        conn.close()
        logger.info(f"Database {db_file} created successfully")
    except sqlite3.Error as e:
        logger.error(f"Error creating database {db_file}: {e}")

class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            logger.error(f"Error connecting to database: {e}")

    def reconnect(self):
        if self.conn:
            self.conn.close()
        self.connect()

    def execute_query(self, query, params=(), fetch=False):
        try:
            with self.conn:
                if fetch:
                    return self.cursor.execute(query, params).fetchall()
                else:
                    self.cursor.execute(query, params)
                    return self.cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}. Query: {query}, Params: {params}")
            self.reconnect()
            return [] if fetch else None

    def get_questions(self):
        result = self.execute_query("SELECT id, questions FROM support;", fetch=True)
        data = {}
        for row in result:
            questions = tuple(row[1].split(":"))
            data[row[0]] = questions
        return data

    def add_questions(self, userid, question):
        return self.execute_query("INSERT INTO userquestions (userid, question) VALUES (?, ?)", (userid, question))

    def get_question(self, answer_id):
        result = self.execute_query("SELECT question FROM userquestions WHERE userid=?", (answer_id,), fetch=True)
        return result[-1][0] if result else None

    def get_id(self):
        result = self.execute_query("SELECT id FROM userquestions", fetch=True)
        return result[-1][0] if result else None

    def question(self, answer_id):
        return self.execute_query("SELECT question FROM userquestions WHERE id=?", (answer_id,), fetch=True)

    def user_exists(self, user_id):
        result = self.execute_query("SELECT * FROM users WHERE user_id=?", (user_id,), fetch=True)
        return bool(len(result))

    def add_user(self, user_id, lang):
        return self.execute_query("INSERT INTO users (user_id, lang) VALUES (?, ?)", (user_id, lang))

    def get_lang(self, user_id):
        result = self.execute_query("SELECT lang FROM users WHERE user_id=?", (user_id,), fetch=True)
        return result[0][0] if result else 'uz'  # Возвращаем 'uz' по умолчанию, если не найдено

    def change_lang(self, user_id, language):
        return self.execute_query("UPDATE users SET lang = ? WHERE user_id=?", (language, user_id))

    def update(self, lang, user_id, name, phone, address=None, status=None, employees=None):
        if self.user_exists(user_id):
            return self.execute_query(
                "UPDATE users SET lang=?, name=?, phone=?, address=?, status=?, employees=? WHERE user_id=?",
                (lang, name, phone, address, status, employees, user_id)
            )
        else:
            return self.execute_query(
                "INSERT INTO users (user_id, lang, name, phone, address, status, employees) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (user_id, lang, name, phone, address, status, employees)
            )

    def get_name(self, user_id):
        result = self.execute_query("SELECT name FROM users WHERE user_id=?", (user_id,), fetch=True)
        return result[0][0] if result else None

    def get_phone(self, user_id):
        result = self.execute_query("SELECT phone FROM users WHERE user_id=?", (user_id,), fetch=True)
        return result[0][0] if result else None

    def get_address(self, user_id):
        result = self.execute_query("SELECT address FROM users WHERE user_id=?", (user_id,), fetch=True)
        return result[0][0] if result else None

    def get_status(self, user_id):
        result = self.execute_query("SELECT status FROM users WHERE user_id=?", (user_id,), fetch=True)
        return result[0][0] if result else None

    def get_employees(self, user_id):
        result = self.execute_query("SELECT employees FROM users WHERE user_id=?", (user_id,), fetch=True)
        return result[0][0] if result else None

    def get_all_users(self):
        result = self.execute_query("SELECT user_id FROM users", fetch=True)
        return [row[0] for row in result]

    def get_all_users_data(self):
        return self.execute_query(
            "SELECT user_id, lang, name, phone, address, status, employees FROM users", fetch=True
        )