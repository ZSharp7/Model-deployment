import configparser
import pymysql

class DB:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('../config.ini')
        # 打开数据库连接
        self.db = pymysql.connect(host=self.config.get('database','host'),
                             user=self.config.get('database','user'),
                             password=self.config.get('database','password'),
                             db=self.config.get('database','db'))
    def create_table(self):
        # # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = self.db.cursor()
        #
        # # 使用 execute() 方法执行 SQL，如果表存在则删除
        # cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
        #
        # # 使用预处理语句创建表
        sql = """CREATE TABLE person_data (
                 id  INT NOT NULL PRIMARY KEY,
                 name  varchar(3) NOT NULL,
                 sex varchar(1) NOT NULL,
                 born DATE NOT NULL,
                 phone varchar(11),
                 adress varchar(100),
                 image_path varchar(100) 
                 )ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 执行sql语句
            self.db.commit()
        except:
            print('error')
            # 发生错误时回滚
            self.db.rollback()
        self.db.close()

    def insert_data(self,id,name,sex,born,phone,adress,path):
        cursor = self.db.cursor()
        sql = """insert into  person_data
                (id,name,sex,born,phone,adress,image_path)
                values 
                (%s,"%s","%s","%s","%s","%s","%s");""" %(
            id,name,sex,born,phone,adress,path
        )

        try:
            # 执行sql语句
            cursor.execute(sql)
            # 执行sql语句
            self.db.commit()
            flag = True
        except:
            # 发生错误时回滚
            self.db.rollback()
            flag = False
        self.db.close()

        return flag
    def select_all (self):
        cursor = self.db.cursor()
        sql = """
                select * from person_data ;
                """
        try:
            cursor.execute(sql)
            self.db.commit()
            result = cursor.fetchall()
        except:
            self.db.rollback()
            return False

        return result


    def select(self,id):
        cursor = self.db.cursor()
        sql = """
        select * from person_data where id=%s;
        """%id
        try:
            cursor.execute(sql)
            self.db.commit()
            result = cursor.fetchone()
        except:
            self.db.rollback()
            return False

        return {
            'id':result[0],
            'name':result[1],
            'sex':result[2],
            'born':result[3],
            'phone':result[4],
            'adress':result[5],
            'image_path':result[6]
        }

    def delete_data(self,id):
        self.cursor = self.db.cursor()
        sql = """
        delete from person_data where id=%s;
        """%id
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

if __name__ == '__main__':
    # DB().create_table()
    # DB().insert_data(
    #     id='100',
    #     name="沈佐航",
    #     sex = "男",
    #     born = '2019-1-3',
    #     phone='18355700201',
    #     adress = "安徽省",
    #     path = "../data/db/images"
    # )
    result = DB()
    print(result.select('0'))
    # print(result)