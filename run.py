from twbox_office import Converter,Spider,Clean,Mysql,Visual
json_data = ["./boxoffice20210101_20210331.json","./boxoffice20210401_20210630.json","./boxoffice20210701_20210930.json","./boxoffice20211001_20211231.json"]   

con = Converter(json_data)
con.get_json()
con.choose_columns()
con.merge_dataframe()
con.drop_duplicate_value()


path = "./110box_office_done.csv"
web = Spider(path)
web.get_CsvTitle()
data01 = web.web_crawler(0, 100)
data01
web.create_csv("01")
data02 = web.web_crawler(100, 250)
data02
web.create_csv("02")
data03 = web.web_crawler(250, 400)
data03
web.create_csv("03")
data04 = web.web_crawler(400, 550)
data04
web.create_csv("04")
data05 = web.web_crawler(550, 681)
data05
web.create_csv("05")
csv_list = [data01,data02,data03,data04,data05]
df = web.merge_table(csv_list)
print(df)
print(df.info())
df.to_csv("./110movie.csv", index=False)

original_data = "./110box_office_done.csv"
spider_data = "./110movie.csv"
clean = Clean(original_data,spider_data)
clean.add_original_name()
clean.merge_dataframe()
clean.convert_time()
clean.convert_level()
clean.drop_column()
clean.convert_dtype()
clean.csv_dropna()

path = "./110box_office_merge.csv"
sql = Mysql(path)
sql.database_set()
sql.create_table()
sql.add_data()

path = "./110box_office_merge.csv"
visual = Visual(path)
visual.fill_null()
visual.adjustment_skewness_kurtosis("IMDB_rating")
visual.adjustment_skewness_kurtosis("movie_time")
visual.logarithmic_trans()