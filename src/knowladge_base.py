import re
import sqlite3
from exception_template import ExceptionTemplate
class KnowladgeBase():
    def __init__(self):
        self.conn = sqlite3.connect("ignored_data/knowladge_base.sqlite")
        c = self.conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS knowladge (
            knowladge_id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT, 
            template TEXT)''')

        c.execute('''CREATE TABLE IF NOT EXISTS generated_from (
            generated_from_id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT,
            knowladge_id INTEGER,
            FOREIGN KEY(knowladge_id) REFERENCES knowladge(knowladge_id))''')

    def insert_exception_template(self, template):
        c = self.conn.cursor()

        try:
            c.execute('''INSERT INTO knowladge(type, template) VALUES(?, ?)''', (template.type, template.template))

            knowladge_id = c.lastrowid
            generated_from_values = [(message, knowladge_id) for message in template.messages]

            c.executemany('''INSERT INTO generated_from(message, knowladge_id) VALUES(?, ?)''', generated_from_values)

            self.conn.commit()
        except:
            self.conn.rollback()

    def get_exception_templates(self):
        c = self.conn.cursor()

        templates = []
        c.execute('''SELECT * FROM knowladge''')
        for row in c.fetchall():
            k_id, k_type, k_template = row
            c.execute('''SELECT message FROM generated_from WHERE knowladge_id=?''', (k_id,))

            messages = c.fetchall()
            templates.append(ExceptionTemplate(k_type, messages, k_template))

        return templates

    def get_knowladge_dict(self):
        templates = self.get_exception_templates()
        knowladge_base = {}
        for template in templates:
            if template.type not in knowladge_base:
                knowladge_base[template.type] = []

            entry = template.template
            knowladge_base[template.type].append(entry)

        return knowladge_base

    def __del__(self):
        self.conn.close()
    