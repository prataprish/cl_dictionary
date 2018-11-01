import sqlite3
import requests
import fetch_online

class Dictionay(object):

    def __init__(self):
        self.connection = sqlite3.connect('dictionary.db')
        if self.init_db():
            pass
        else:
            print('Database Connection Error!!!')

    def init_db(self):
        try:
            self.connection.execute("CREATE TABLE IF NOT EXISTS words" \
                            "(id INTEGER PRIMARY KEY AUTOINCREMENT," \
                            "word VARCHAR(20) UNIQUE NOT NULL," \
                            "syn_group INTEGER NOT NULL," \
                            "hits INTEGER DEFAULT 0," \
                            "meaning TEXT)")
            yield True
            return
        except Exception:
            yield False
            return

    def add_word(self,name,meaning,syns = []):
        syn_group = self.get_max_syn_id()
        if syn_group:
            syn_group += 1
        else:
            syn_group = 1

        try:
            self.connection.execute("INSERT OR REPLACE INTO words (word,meaning,syn_group,hits) VALUES(?,?,?,1)",tuple([name,meaning,syn_group]))
            if syns:
                syn_group = [tuple([syn,syn_group]) for syn in syns]
                self.connection.executemany("INSERT OR IGNORE INTO words (word,syn_group) VALUES(?,?)",syn_group)
        finally:
            self.connection.commit()
            return

    def get_max_syn_id(self):
        try:
            for row in self.connection.execute('SELECT MAX(syn_group) FROM words'):
                return row[0]
        except Exception:
            return

    def get_syn(self,word,syn_group):
        try:
            syns = self.connection.execute("SELECT word FROM words WHERE syn_group = ? and word != ?",tuple([syn_group,word]))
            if syns:
                for syn in self.connection.execute("SELECT word FROM words WHERE syn_group = ? and word != ?",tuple([syn_group,word])):
                    yield ' '.join(syn[0].split('_'))

        except Exception:
            pass

    def get_meaning(self,word):
        try:
            for meaning in self.connection.execute("SELECT meaning,syn_group,id FROM words WHERE word = ?",tuple([word])):
                if meaning[0]:
                    self.connection.execute("UPDATE words SET hits = hits + 1 WHERE id = ?",tuple([meaning[2]]))
                    self.connection.commit()
                    yield 'Here is what I found:'
                    yield meaning[0].encode('ascii')
                    return
                else:
                    if connection_ok():
                        pass
                    else:
                        yield 'Cannot find meaning, but a few similar word:'.encode('ascii')
                        for syn in self.get_syn(word,meaning[1]):
                            yield syn.encode('ascii')
                        return
            result = fetch_online.fetch(word)
            if result:
                self.add_word(word,result['meaning'],result['synonyms'])
            yield result['meaning'].encode('ascii')
            return
        except Exception:
            return

    def close(self):
        self.connection.close()


def connection_ok():
    try:
        requests.get('https://www.google.com')
        return True
    except Exception:
        return False
