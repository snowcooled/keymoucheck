import os
import random
from datetime import date
from PySide6.QtSql import QSqlDatabase, QSqlQuery
from PySide6.QtCore import QCoreApplication

class SQLite3DB:

    CREATE_CLICK_SQL = """
        create table if not exists events(
            id integer primary key,
            name varchar(200) ,
            is_key integer default 1,
            create_at timestamp default CURRENT_TIMESTAMP,
            update_at timestamp  default CURRENT_TIMESTAMP
        )
        """
    
    CREATE_KEY_MAP_SQL = """
        create table if not exists key_map(
            id integer primary key,
            code  varchar(20) not null,
            name varchar(200),
            create_at timestamp default CURRENT_TIMESTAMP,
            update_at timestamp  default CURRENT_TIMESTAMP
        )
        """

    CLEAR_CLICK_SQL = "DELETE FROM events"
    CLEAR_KEY_MAP_SQL = "DELETE FROM key_map"

    db  = None

    def __init__(self, debug=False):
        self.debug = debug
        self.database = 'data.dat'
        self.db = self.get_db()
        self.q = QSqlQuery(self.db)
        self.tables_check()
    
    def get_db(self):
        db = QSqlDatabase.addDatabase("QSQLITE")
        #db.setDatabaseName(":memory:")
        #BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        BASE_DIR = QCoreApplication.applicationDirPath()
        if self.debug:
            print(BASE_DIR+'\\data.dat')
        db.setDatabaseName(BASE_DIR+'\\'+self.database)
        if not db.open():
            print("数据库打开失败")
            return None
        return db

    def close(self):
        self.db.close()

    def table_exist(self, table_name):
        QUERY_SQL = "select * from sqlite_master where name = '%s'" % (table_name)
        if self.debug:
            print(QUERY_SQL)
        self.q.exec(QUERY_SQL)
        return  True if self.q.next() else False

    def tables_check(self):
        if not self.table_exist('events'):
            if self.debug:
                print('table events is not exist')
            self.q.exec(self.CREATE_CLICK_SQL)
        if not self.table_exist('key_map'):
            if self.debug:
                print('table key_map is not exist')
            self.q.exec(self.CREATE_KEY_MAP_SQL)

    def add_events(self, name, is_key):
        INSERT_EVENTS_SQL = """
            insert into events(name, is_key) 
            values(:name, :is_key)
            """
        self.q.prepare( INSERT_EVENTS_SQL )
        self.q.bindValue(':name', name)
        self.q.bindValue(':is_key', is_key)
        self.q.exec()
        if self.debug:
            print( "insert into events(name, is_key) values('%s', '%d')" % (name, is_key) )
        self.db.commit()
        return self.q.lastInsertId()

    def events_list(self, name=''):
        if name == '':
            QUERY_SQL = "SELECT * FROM events ORDER BY create_at DESC"
        else :
            QUERY_SQL = "SELECT * FROM events WHERE name='%s' ORDER BY create_at DESC" % (name)
        if self.debug:
            print(QUERY_SQL)
        data = []
        self.q.exec(QUERY_SQL)
        while self.q.next():
            item = {
                'id': self.q.value(0),
				'name' : self.q.value(1),
				'is_key' : self.q.value(2),
				'create_at' : self.q.value(3),
				'update_at' : self.q.value(4),
            }
            data.append(item)
        return data

    def get_day_keyboard_count(self):
        QUERY_SQL = "select count(*) as counter from events where is_key = 1 AND create_at>=datetime('now','start of day','+0 day') and create_at<datetime('now','start of day','+1 day')"
        self.q.exec(QUERY_SQL)
        return 0 if not self.q.next() else self.q.value(0)

    def get_day_mouse_count(self):
        QUERY_SQL = "select count(*) as counter from events where is_key = 0 AND create_at>=datetime('now','start of day','+0 day') and create_at<datetime('now','start of day','+1 day')"
        self.q.exec(QUERY_SQL)
        return 0 if not self.q.next() else self.q.value(0)
    
    def get_month_keyboard_count(self):
        QUERY_SQL = "select count(*) as counter from events where is_key = 1 AND create_at>=datetime('now','start of month','+0 month','-0 day') AND create_at < datetime('now','start of month','+1 month','0 day')"
        self.q.exec(QUERY_SQL)
        return 0 if not self.q.next() else self.q.value(0)

    def get_month_mouse_count(self):
        QUERY_SQL = "select count(*) as counter from events where is_key = 0 AND create_at>=datetime('now','start of month','+0 month','-0 day') AND create_at < datetime('now','start of month','+1 month','0 day')"
        self.q.exec(QUERY_SQL)
        return 0 if not self.q.next() else self.q.value(0)
    
    def get_year_keyboard_count(self):
        QUERY_SQL = "select count(*) as counter from events where is_key = 1 AND create_at>=datetime('now','start of year', '+0 month','-0 day') and create_at<datetime('now','start of year','+12 month', '-0 day')"
        self.q.exec(QUERY_SQL)
        return 0 if not self.q.next() else self.q.value(0)

    def get_year_mouse_count(self):
        QUERY_SQL = "select count(*) as counter from events where is_key = 0 AND create_at>=datetime('now','start of year', '+0 month','-0 day') and create_at<datetime('now','start of year','+12 month', '-0 day')"
        self.q.exec(QUERY_SQL)
        return 0 if not self.q.next() else self.q.value(0)
    
    def get_month_count(self, month=''):
        if month == '':
            QUERY_SQL = self.get_cur_month_count_sql()
        else:
            QUERY_SQL = self.get_month_count_sql(month)
        self.q.exec(QUERY_SQL)
        data = []
        while self.q.next():
            data.append({
                'code': self.q.value(0),
                'name': self.q.value(1),
                'is_key_val': self.q.value(2),
                'is_key': self.q.value(3),
                'counter': self.q.value(4),
            })
        return data
 
    def get_year_count(self, year=''):
        if year == '':
            QUERY_SQL = self.get_cur_year_count_sql()
        else:
            QUERY_SQL = self.get_year_count_sql(year)
        self.q.exec(QUERY_SQL)
        data = []
        while self.q.next():
            data.append({
                'code': self.q.value(0),
                'name': self.q.value(1),
                'is_key_val': self.q.value(2),
                'is_key': self.q.value(3),
                'counter': self.q.value(4),
            })
        return data
    
    def get_cur_month_count_sql(self):
        QUERY_SQL = "select km.code, km.name, iif(e.is_key==0, '鼠标', '键盘') as is_key_val, e.is_key, count(e.name) as counter from events e LEFT JOIN key_map km ON e.name=km.code where e.create_at>=datetime('now','start of month','+0 month','-0 day') AND e.create_at < datetime('now','start of month','+1 month','0 day') GROUP BY km.code, km.name, e.is_key ORDER BY e.is_key ASC, counter DESC"
        return QUERY_SQL
 
    def get_cur_year_count_sql(self):
        QUERY_SQL = "select km.code, km.name, iif(e.is_key==0, '鼠标', '键盘') as is_key_val, e.is_key, count(e.name) as counter from events e LEFT JOIN key_map km ON e.name=km.code where e.create_at>=datetime('now','start of year', '+0 month','-0 day') and e.create_at<datetime('now','start of year','+12 month', '-0 day') GROUP BY km.code, km.name, e.is_key ORDER BY e.is_key ASC, counter DESC"
        return QUERY_SQL

    def get_month_count_sql(self, month):
        QUERY_SQL = "select km.code, km.name, iif(e.is_key==0, '鼠标', '键盘') as is_key_val, e.is_key, count(e.name) as counter from events e LEFT JOIN key_map km ON e.name=km.code where STRFTIME('%Y%m', e.create_at)='"+month+"' GROUP BY km.code, km.name, e.is_key ORDER BY e.is_key ASC, counter DESC"
        return QUERY_SQL
 
    def get_year_count_sql(self, year):
        QUERY_SQL = "select km.code, km.name, iif(e.is_key==0, '鼠标', '键盘') as is_key_val, e.is_key, count(e.name) as counter from events e LEFT JOIN key_map km ON e.name=km.code where STRFTIME('%Y', e.create_at)='"+year+"' GROUP BY km.code, km.name, e.is_key ORDER BY e.is_key ASC, counter DESC"
        return QUERY_SQL

    def  get_all_month(self):
        QUERY_SQL = "SELECT STRFTIME('%Y%m', create_at) AS code, STRFTIME('%Y年%m月', create_at) AS value, count(*) counter FROM events GROUP BY STRFTIME('%Y%m', create_at) ORDER BY STRFTIME('%Y%m', create_at) DESC "
        self.q.exec(QUERY_SQL)
        data = []
        while self.q.next():
            data.append({
                'code': self.q.value(0),
                'name': self.q.value(1),
                'counter': self.q.value(2),
            })
        return data

    def  get_all_year(self):
        QUERY_SQL = "SELECT STRFTIME('%Y', create_at) AS code, STRFTIME('%Y年', create_at) AS value, count(*) counter FROM events GROUP BY STRFTIME('%Y', create_at) ORDER BY STRFTIME('%Y', create_at) DESC "
        self.q.exec(QUERY_SQL)
        data = []
        while self.q.next():
            data.append({
                'code': self.q.value(0),
                'name': self.q.value(1),
                'counter': self.q.value(2),
            })
        return data

    def insert_test_data(self):
        for i in range(0, 1000):
            year = random.randint(2010, 2023)
            month = random.randint(1, 12)
            create_at = '%s-%s-01 12:00:00' % (year, month)
            #print(create_at)
            is_key = random.randint(0, 1)
            if is_key:
                name = str(random.randint(1, 127))
            else:
                name = random.choice(['-1', '-2', '-3', '-4', '-5'])
            INSERT_EVENTS_SQL = """
                insert into events(name, is_key, create_at) 
                values(:name, :is_key, :create_at)
                """
            self.q.prepare( INSERT_EVENTS_SQL )
            self.q.bindValue(':name', name)
            self.q.bindValue(':is_key', is_key)
            self.q.bindValue(':create_at', create_at)
            self.q.exec()

            if self.debug:
                print( "insert into events(name, is_key, create_at) values('%s', '%d', '%s')" % (name, is_key, create_at) )
        self.db.commit()
            


if __name__ == "__main__":
    db = SQLite3DB()
    #db.insert_test_data()
    #db.init_db()
    #db.add_events('k', 1)
    #db.add_events('2', 1)
    #db.add_events('3', 1)
    #db.add_events('k', 1)
    #print(db.events_list())
    #print(db.events_list(name='k'))
    #print(db.get_day_keyboard_count())
    #print(type(db.get_day_keyboard_count()))
    #print(db.get_day_mouse_count())
    #print(db.get_month_keyboard_count())
    #print(db.get_month_mouse_count())
    #print(db.get_year_keyboard_count())
    #print(db.get_year_mouse_count())
    #print(db.get_month_count_sql('202309'))
    #print(db.get_year_count_sql('2020'))
    #print(db.get_year_count_sql('2023'))
    print(db.get_month_count('202201'))
    print(db.get_year_count('2017'))
    #print(db.get_all_month())
    #print(db.get_all_year())

    '''
    data = db.get_month_count()
    
    for row in data:
        print(type(row['name']))
        print(row['name'])
    '''

    
