import pandas as pd
import pymysql
import numpy as np
class Mysql:
    def __init__(self,path):
        self._path = path
        self._null_fill = pd.DataFrame()
        self._database = ()
    #輸入要連結的資料庫基本資料，並將表格內的空值替換成None
    def database_set(self):
        data = pd.read_csv(self._path)
        self._null_fill = data.fillna("None")
        self._database = pymysql.connect(host="localhost",
                     port=3306,
                     user="username",
                     passwd="password",
                     db="database_name",
                     charset="utf8")
        return self._database
    #在mysql創建資料表
    def create_table(self):
        cursor = self._database.cursor()
        sql = "CREATE TABLE box_office (data_name varchar(500) NULL,original_name varchar(500) NULL,releaseDate date NULL,country varchar(100) NULL,issue varchar(100) NULL,produce varchar(500) NULL,movie_rating varchar(100) NULL,genre varchar(100) NULL,IMDB_rating varchar(100) NULL,total_time varchar(100) NULL,theaterCount int NULL,totalTickets int NULL,totalAmounts int NULL);"
        cursor.execute(sql)
        data = self._null_fill
        data.columns = ["data_name", "original_name", "releaseDate", "country", "issue", "produce",
                "movie_rating", "genre", "IMDB_rating", "total_time", "theaterCount", "totalTickets", "totalAmounts"]

        self._database.commit()
        self._database.close()
    #在mysql創建的資料表中新增資料
    def add_data(self):
        cursor = self._database.cursor()
        data = self._null_fill
        data.columns = ["data_name", "original_name", "releaseDate", "country", "issue", "produce",
                "movie_rating", "genre", "IMDB_rating", "total_time", "theaterCount", "totalTickets", "totalAmounts"]
        for index, row_values in data.iterrows():
            cursor.execute("INSERT INTO 110movie.box_office (data_name, original_name, releaseDate, country,issue,produce,movie_rating,genre,IMDB_rating,total_time,theaterCount,totalTickets,totalAmounts) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",
                    (row_values.data_name, row_values.original_name, row_values.releaseDate, row_values.country, row_values.issue, row_values.produce, row_values.movie_rating, row_values.genre, row_values.IMDB_rating, row_values.total_time, row_values.theaterCount, row_values.totalTickets, row_values.totalAmounts))
        self._database.commit()
        self._database.close()

# path = "./110box_office_merge.csv"
# sql = Mysql(path)
# sql.database_set()
# sql.create_table()
# sql.add_data()


