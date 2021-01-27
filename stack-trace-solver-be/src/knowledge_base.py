import sqlite3
from exception_template import ExceptionTemplate

class KnowledgeBase():
    def __init__(self, fileName):
        self.conn = sqlite3.connect(f"ignored_data/{fileName}")
        c = self.conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS knowledge (
            knowledge_id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT, 
            template TEXT)''')

        c.execute('''CREATE TABLE IF NOT EXISTS generated_from (
            generated_from_id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT,
            knowledge_id INTEGER,
            FOREIGN KEY(knowledge_id) REFERENCES knowledge(knowledge_id))''')

    def insert_exception_template(self, template):
        if self.does_message_exist(template.type, template.template):
            return

        c = self.conn.cursor()
        try:
            c.execute('''INSERT INTO knowledge(type, template) VALUES(?, ?)''', (template.type, template.template))

            knowledge_id = c.lastrowid
            generated_from_values = [(message, knowledge_id) for message in template.messages]

            c.executemany('''INSERT INTO generated_from(message, knowledge_id) VALUES(?, ?)''', generated_from_values)

            self.conn.commit()
        except:
            self.conn.rollback()

    def get_exception_templates(self):
        c = self.conn.cursor()

        templates = []
        c.execute('''SELECT * FROM knowledge''')
        for row in c.fetchall():
            k_id, k_type, k_template = row
            c.execute('''SELECT message FROM generated_from WHERE knowledge_id=?''', (k_id,))

            messages = c.fetchall()
            templates.append(ExceptionTemplate(k_type, messages, k_template))

        return templates

    def does_message_exist(self, type, template):
        c = self.conn.cursor()
        c.execute('''SELECT * FROM knowledge WHERE type = ? AND template = ?''', (type, template))
        
        return len(c.fetchall()) > 0

    def get_knowledge_dict(self):
        templates = self.get_exception_templates()
        knowledge_base = {}
        for template in templates:
            if template.type not in knowledge_base:
                knowledge_base[template.type] = []

            entry = template.template
            knowledge_base[template.type].append(entry)

        return knowledge_base

    def __del__(self):
        self.conn.close()
    