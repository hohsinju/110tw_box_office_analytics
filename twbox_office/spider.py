import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import re
from random import randint
import numpy as np
class Spider:
    def __init__(self, path):
        self._path = path
        self._search_list = []
        self._search_info = ()
        self._movie_info = []
        self._search_keyword = str
        self._first_soup = str
        self._main_soup = str
        self._web_info = str
    #匯入電影名稱並將多餘字詞做替換
    def get_CsvTitle(self):
        data = pd.read_csv(self._path)
        movie_name = data.name.values
        name_list = []
        for item in movie_name:
            name = re.sub("4K數位修復版", "", item)
            name = re.sub("4K修復版", "", name)
            name = re.sub("數位修復", "", name)
            name = re.sub("\(\w\w\w\)", "", name)
            name = re.sub("\(版\)", "", name)
            name = re.sub("（下）", "後篇", name)
            name = re.sub("（上）", "前篇", name)
            name = re.sub("\:版", "", name)
            name = re.sub("：版", "", name)
            name = re.sub("\(數位國語2D版\)", "", name)
            # print(len(new))
            name_list.append(name)
            self._search_list = name_list
        return self._search_list
    #從yahoo電影網頁爬蟲搜集電影資訊
    def web_crawler(self, start, end):
        length = len(self._search_list)
        name_list = []
        original_name_list = []
        genre_list = []
        movie_time_list = []
        rating_list = []
        movie_level_list = []
        for i in range(start, end):
            print("讀進來了")
            url = 'https://movies.yahoo.com.tw/moviesearch_result.html?movie_type=movie&keyword='
            self._search_keyword = self._search_list[i]
            # get yahoo movie search page response
            self._first_soup = self.first_request(url)
            # make sure the code doesn't stop running if it can't find data
            try:
                # parse the URL of the corresponding movie information page from the document
                url_export = self._first_soup.find_all(href=re.compile("^https://movies.yahoo.com.tw/movieinfo_main/"))
                url_list = []
                for element in url_export:
                    url_list.append(element.get('href'))
                #print(url_list)
                search_num = self.search_response_num()
                movie_web = url_list[search_num]
                print(movie_web)
                # get yahoo movie search page response
                info_text = self.second_request(movie_web)
                self._movie_info = info_text
                movie_title = self.web_title()
                print(movie_title)
                name_list.append(movie_title[0])
                original_name_list.append(movie_title[1])
                genre = self.web_genre()
                genre_list.append(genre)
                movie_length = self.web_movie_length()
                movie_time_list.append(movie_length)
                imdb_rating = self.web_imdb_rating()
                rating_list.append(imdb_rating)
                movie_rating = self.web_movie_rating()
                movie_level_list.append(movie_rating)

            except:
                print("不符合比對，輸入nan!")
                name_list.append(np.nan)
                original_name_list.append(np.nan)
                genre_list.append(np.nan)
                movie_time_list.append(np.nan)
                rating_list.append(np.nan)
                movie_level_list.append(np.nan)
        self._search_info = name_list, original_name_list, movie_level_list, genre_list, rating_list, movie_time_list
        return self._search_info
    #yahoo電影關鍵字搜尋第一次請求
    def first_request(self,url):
        movie_data = requests.get(url+self._search_keyword)
        try:
            time.sleep(randint(2, 5))
            return BeautifulSoup(movie_data.text, "html.parser")
        except:
            time.sleep(randint(3, 8))
            return BeautifulSoup(movie_data.text, "html.parser")
        
   #取得資料搜尋筆數、導演資訊，用來確認搜尋結果符合電影資訊而非文章。
    def search_response_num(self):        
        try:
            num_export = self._first_soup.find('div', class_="search_num _c")
            export = num_export.get_text()
            export =export.replace("筆"," ")
            num = export.split()
            num = int(num[1])
            normal_export = self._first_soup.find('div', class_="search_actor")
            actor = normal_export.get_text()
            if num >= 1 and actor == "導演資訊：":
                return -1
        except :
            return "wrong search"
    #取得搜尋頁結果後向指定網頁請求
    def second_request(self,movie_web):
        web = requests.get(movie_web)
        try:
            time.sleep(randint(3, 8))
            self._main_soup = BeautifulSoup(web.text, "html.parser")
        except:
            time.sleep(randint(2, 5))
            self._main_soup = BeautifulSoup(web.text, "html.parser")
        information = self._main_soup.find_all(class_="movie_intro_info_r")
        for tag in information:
            text = tag.get_text()
            info_text = text.strip()
            return info_text.split('\n')
   #取得電影中文名稱和原文名稱 
    def web_title(self):
        name = self._movie_info[0]
        original_name = self._movie_info[1]
        return name,original_name
    #取得電影種類
    def web_genre(self):
        try :
            genre = self._movie_info[5].strip()
            return genre
        except:
            return np.nan
    #取得電影片長
    def web_movie_length(self):
        try:
            for movie_length in self._movie_info:
                if "片　　長" in movie_length:
                    movie_time = movie_length.split('：')
                    movie_time = movie_time[1]
                    return movie_time
        except:
            return np.nan
    #取得imdb分數
    def web_imdb_rating(self):
        try:
            for movie_rating in self._movie_info:
                if "IMDb分數" in movie_rating:
                    raise
            return np.nan
        except:
            rating = movie_rating.split('：')
            rating = rating[1]
            return rating
    #取得電影級別icon代稱
    def web_movie_rating(self):
        try:
            level_name = self._main_soup.find_all('div')
            level_list = []
            for tag in level_name:
                level = tag.get('class')
                level_list.append(level)
            movie_level = level_list[89][0]
            return movie_level
        except:
            return np.nan
    def merge_table(self,csv):
        df = pd.concat(csv, ignore_index=True)
        return df
    #創建表格存進csv檔中
    def create_csv(self, number):
        movie_df = pd.DataFrame()
        movie_df["name"] = pd.Series(self._search_info[0])
        movie_df["original_name"] = pd.Series(self._search_info[1])
        movie_df["movie_rating"] = pd.Series(self._search_info[2])
        movie_df["genre"] = pd.Series(self._search_info[3])
        movie_df["IMDB_rating"] = pd.Series(self._search_info[4])
        movie_df["movie_time"] = pd.Series(self._search_info[5])
        return movie_df.to_csv("./yahoo_110movie"+number+".csv", index=False)


# path = "./110box_office_done.csv"
# web = Spider(path)
# web.get_CsvTitle()
# data01 = web.web_crawler(0, 100)
# data01
# web.create_csv("01")
# data02 = web.web_crawler(100, 250)
# data02
# web.create_csv("02")
# data03 = web.web_crawler(250, 400)
# data03
# web.create_csv("03")
# data04 = web.web_crawler(400, 550)
# data04
# web.create_csv("04")
# data05 = web.web_crawler(550, 681)
# data05
# web.create_csv("05")
# csv_list = [data01,data02,data03,data04,data05]
# df = web.merge_table(csv_list)
# print(df)
# print(df.info())
# df.to_csv("./110movie.csv", index=False)