import sqlite3


class Database:
    def __init__(self,db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def get_questions(self):
        with self.conn:
            result=self.cursor.execute("SELECT id,questions FROM support",()).fetchall()
            data={}
            for row in result:
                questions=tuple(row[1].split(":"))
                data[row[0]]=questions
            return data

    def get_answer(self,answer_id):
        with self.conn:
            return self.cursor.execute("SELECT answer from support WHERE id=?",(answer_id,)).fetchone()[0]