import pandas as pd
import numpy as np
class Clean:
    def __init__(self,original_data,spider_data):
        self._first_data = original_data
        self._second_data = spider_data
        self._original_df = pd.DataFrame()
        self._spider_df = pd.DataFrame()
        self._merge_df = pd.DataFrame()
        self._trans_df = pd.DataFrame()
    # 將原始資料電影片名（非搜尋片名）新增至爬蟲表格中
    def add_original_name(self):
        self._original_df = pd.read_csv(self._first_data)
        web_data = pd.read_csv(self._second_data)
        new_df = pd.DataFrame(web_data)
        new_df["data_name"] = self._original_df.name
        self._spider_df = new_df.reindex(columns=['data_name', 'name', 'original_name',
                        'movie_rating', 'genre', 'IMDB_rating', 'movie_time'])
        return self._spider_df
    # 原始資料合併爬蟲資料
    def merge_dataframe(self):
        self._original_df = self._original_df.rename(columns={"name": "data_name"})
        df = pd.merge(self._original_df, self._spider_df, how='left')
        self._merge_df = df.drop(["name"], axis=1)
        return self._merge_df
    #將中文編寫的時間格式(時、分)轉換成整數分鐘制
    def convert_time(self):
        movie_time = self._merge_df.movie_time.values
        translate_list = []
        for i in movie_time:
            translate_list.append(str(i))
        new_time_list = []
        for i in translate_list:
            if "分" in i:
                i = i.strip()
                i = i.strip("分")
                if i[0:2] == "00":
                    hours = 0
                    if i[3] == "0":
                        minutes = int(i[4])
                        minutes = hours+minutes
                        new_time_list.append(minutes)
                    else:
                        minutes = int(i[3:5])
                        minutes = hours+minutes
                        new_time_list.append(minutes)
                elif i[0:2] == "01":
                    hours = 60
                    if i[3] == "0":
                        minutes = int(i[4])
                        minutes = hours+minutes
                        new_time_list.append(int(minutes))
                    else:
                        minutes = int(i[3:5])
                        minutes = hours+minutes
                        new_time_list.append(int(minutes))
                elif i[0:2] == "02":
                    hours = 120
                    if i[3] == "0":
                        minutes = int(i[4])
                        minutes = hours+minutes
                        new_time_list.append(int(minutes))
                    else:
                        minutes = int(i[3:5])
                        minutes = hours+minutes
                        new_time_list.append(int(minutes))
                elif i[0:2] == "03":
                    hours = 180
                    if i[3] == "0":
                        minutes = int(i[4])
                        minutes = hours+minutes
                        new_time_list.append(int(minutes))
                    else:
                        minutes = int(i[3:5])
                        minutes = hours+minutes
                        new_time_list.append(int(minutes))
            else:
                new_time_list.append(np.nan)
        return new_time_list
    #將圖片代號轉換成分級制度類別名稱
    def convert_level(self):
        level = self._merge_df.movie_rating.values
        level_list = []
        for i in level:
            # print(type(i))
            level_list.append(str(i))
        define_level_list = []
        for i in level_list:
            if "icon" in i:
                if i == "icon_0":
                    define_level_list.append("普遍級")
                elif i == "icon_6":
                    define_level_list.append("保護級")
                elif i == "icon_12":
                    define_level_list.append("輔12級")
                elif i == "icon_15":
                    define_level_list.append("輔15級")
                elif i == "icon_18":
                    define_level_list.append("限制級")
            else:
                define_level_list.append(np.nan)
        return define_level_list
    #新增欄位total_time,movie_rating將不需要的欄位刪除
    def drop_column(self):
        df = self.merge_dataframe().drop(["movie_rating", "movie_time"], axis=1)
        df["total_time"] = self.convert_time()
        df["movie_rating"] = self.convert_level()
        return df
    #totalAmounts欄位類別float轉成int
    #將合併好的資料儲存成csv檔
    def convert_dtype(self):
        df = self.drop_column()
        df["totalAmounts"] = df["totalAmounts"].astype(int)
        df_columns = ["data_name", "original_name", "releaseDate", "country", "issue", "produce",
                    "movie_rating", "genre", "IMDB_rating", "total_time", "theaterCount", "totalTickets", "totalAmounts"]
        self._trans_df = df.reindex(columns=df_columns)
        return self._trans_df.to_csv("./110box_office_merge.csv", index=False)
    #將合併好的資料從中剔除任何一列有空值的資料儲存成csv檔
    def csv_dropna(self):
        df = self._trans_df.dropna(how="any")
        return df.to_csv("./110box_office_no_null.csv", index=False)

# original_data = "./110box_office_done.csv"
# spider_data = "./110movie.csv"
# clean = Clean(original_data,spider_data)
# clean.add_original_name()
# clean.merge_dataframe()
# clean.convert_time()
# clean.convert_level()
# clean.drop_column()
# clean.convert_dtype()
# clean.csv_dropna()



