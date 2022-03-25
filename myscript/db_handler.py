import sqlite3
from .type_models import Sentence

class DBHandler:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)

    def __del__(self):
        self.conn.close()

    def create_table(self):
        sql_create_utterance = '''
        create table if not exists utterance (
            id integer primary key autoincrement,
            sentence text unique not null
        )
        '''
        sql_create_vector = '''
        create table if not exists vector(
            id integer primary key ,
            vector blob,
            foreign key(id) references sql_utterance(id) on delete cascade
        )
        '''
        cur = self.conn.cursor()
        cur.execute(sql_create_utterance)
        self.conn.commit()
        cur.execute(sql_create_vector)
        self.conn.commit()

    def insert_utterance(self, utterance):
        sql = '''
        insert into utterance (sentence)
        values(?)
        on conflict do nothing
        '''
        utterance = utterance.strip()
        cur = self.conn.cursor()
        cur.execute(sql, (utterance,))
        self.conn.commit()

    def get_unvectorized(self):
        def convert_return(data):
            return Sentence(id=data[0], sentence=data[1], vector=data[2])
        sql_select_unvectorized = '''
        select utterance.id, sentence, vector from utterance
        left join vector on utterance.id = vector.id
        where vector is null
        '''
        cur = self.conn.cursor()
        cur.execute(sql_select_unvectorized)
        data = cur.fetchall()
        data = list(map(convert_return, data))
        return data

    def get_vectorized_by_sentence(self, sentences):
        def convert_return(data):
            return Sentence(id=data[0], sentence=data[1], vector=data[2])
        sentences = list(map(lambda x: x.strip(), sentences))
        arg = str(tuple(sentences)).replace(',)', ')')
        sql = f'''
        select utterance.id, sentence, vector from utterance
        join vector on utterance.id = vector.id
        where vector is not null and sentence in {arg}
        '''
        cur = self.conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        data = list(map(convert_return, data))
        return data

    def set_vector(self, id, vector):
        sql = '''
        insert or replace into vector(id, vector)
        values(?, ?)
        '''
        cur = self.conn.cursor()
        cur.execute(sql, (id, vector))
        self.conn.commit()

