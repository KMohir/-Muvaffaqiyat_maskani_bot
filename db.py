import sqlite3

def create_database(db_file):
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

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def get_questions(self):
        with self.conn:
            result = self.cursor.execute("SELECT id, questions FROM support;").fetchall()
            data = {}
            for row in result:
                questions = tuple(row[1].split(":"))
                data[row[0]] = questions
            return data

    def add_questions(self, userid, question):
        with self.conn:
            return self.cursor.execute("INSERT INTO userquestions (userid, question) VALUES (?, ?)", (userid, question))

    def get_question(self, answer_id):
        with self.conn:
            return self.cursor.execute("SELECT question FROM userquestions WHERE userid=?", (answer_id,)).fetchall()[-1][0]

    def get_id(self):
        with self.conn:
            return self.cursor.execute("SELECT id FROM userquestions").fetchall()[-1][0]

    def question(self, answer_id):
        with self.conn:
            return self.cursor.execute("SELECT question FROM userquestions WHERE id=?", (answer_id,)).fetchone()

    def user_exists(self, user_id):
        with self.conn:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self, user_id, lang):
        with self.conn:
            return self.cursor.execute("INSERT INTO users (user_id, lang) VALUES (?, ?)", (user_id, lang))

    def get_lang(self, user_id):
        with self.conn:
            return self.cursor.execute("SELECT lang FROM users WHERE user_id=?", (user_id,)).fetchone()[0]

    def change_lang(self, user_id, language):
        with self.conn:
            return self.cursor.execute("UPDATE users SET lang = ? WHERE user_id=?", (language, user_id))

    def update(self, lang, user_id, name, phone, address=None, status=None, employees=None):
        with self.conn:
            if self.user_exists(user_id):
                return self.cursor.execute(
                    "UPDATE users SET lang=?, name=?, phone=?, address=?, status=?, employees=? WHERE user_id=?",
                    (lang, name, phone, address, status, employees, user_id)
                )
            else:
                return self.cursor.execute(
                    "INSERT INTO users (user_id, lang, name, phone, address, status, employees) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (user_id, lang, name, phone, address, status, employees)
                )

    def get_name(self, user_id):
        with self.conn:
            return self.cursor.execute("SELECT name FROM users WHERE user_id=?", (user_id,)).fetchone()[0]

    def get_phone(self, user_id):
        with self.conn:
            return self.cursor.execute("SELECT phone FROM users WHERE user_id=?", (user_id,)).fetchone()[0]

    def get_address(self, user_id):
        with self.conn:
            result = self.cursor.execute("SELECT address FROM users WHERE user_id=?", (user_id,)).fetchone()
            return result[0] if result else None

    def get_status(self, user_id):
        with self.conn:
            result = self.cursor.execute("SELECT status FROM users WHERE user_id=?", (user_id,)).fetchone()
            return result[0] if result else None

    def get_employees(self, user_id):
        with self.conn:
            result = self.cursor.execute("SELECT employees FROM users WHERE user_id=?", (user_id,)).fetchone()
            return result[0] if result else None

    def get_all_users(self):
        with self.conn:
            result = self.cursor.execute("SELECT user_id FROM users").fetchall()
            return [row[0] for row in result]

    def get_all_users_data(self):
        with self.conn:
            result = self.cursor.execute(
                "SELECT user_id, lang, name, phone, address, status, employees FROM users"
            ).fetchall()
            return result

# Создаем объект базы данных
db = Database('databaseprotestim.db')