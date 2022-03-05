import sqlite3


class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def add_user(self,user_id, user_name, full_name):
        self.cursor.execute("INSERT INTO `users` (`user_id`,`user_name`, `full_name`) VALUES (?, ?, ?)", (user_id,user_name,full_name,))
        return self.conn.commit()


    def close(self):
        self.cursor.close()