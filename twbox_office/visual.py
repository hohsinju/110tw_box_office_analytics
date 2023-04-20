import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib
import seaborn as sns
import numpy as np
class Visual:
    def __init__(self,path):
        self._path = path
        self._data = pd.DataFrame()
    #將IMDB_rating,total_time欄位空值以插值法填入代值
    def fill_null(self):
        # 避免pandas值出現科學計數法，顯示到小數點後兩位
        pd.set_option("display.float_format", lambda x: '%.2f' % x)
        df = pd.read_csv(self._path)
        fillna_data = pd.DataFrame()
        fillna_data["IMDB_rating"] = df["IMDB_rating"]
        fillna_data["movie_time"] = df["total_time"]
        fillna_data["totalTickets"] = df["totalTickets"]
        fillna_data["totalAmounts"] = df["totalAmounts"]
        fill_df = fillna_data.sort_values(["totalTickets"], ascending=False)
        self._data = fill_df.interpolate()
        return self._data
    #調整欄位最大最小值，去掉極端值，以利提升相關係數。
    def adjustment_skewness_kurtosis(self,column_name):
        #四分位距
        q3 = self._data[column_name].quantile(0.75)
        q1 = self._data[column_name].quantile(0.25)
        iqr = (q3 - q1)*1.5
        #重新拉取的最大值
        max_value = q3+iqr
        print(max_value)
        #重新拉取的最小值
        min_value = q1-iqr
        print(min_value)
        #取得落在此區間的數值
        new_area = self._data[(self._data[column_name] <= max_value) & (self._data[column_name] >= min_value)]
        df = pd.DataFrame()
        df[column_name] = new_area[column_name]
        df["totalTickets"] = new_area["totalTickets"]
        df["totalAmounts"] = new_area["totalAmounts"]
        #print(df)
        #print(df.corr())
        plt.figure(figsize=(11, 7))
        sns.heatmap(df.corr(), annot=True)
        plt.show()
        return df.to_csv("./110movie_"+column_name+"_df.csv", index=False)
    #使用對數轉換調整totalTickets,totalAmounts欄位數值的偏度和峰度
    def logarithmic_trans(self):
        trans_tickets_data = np.log(self._data["totalTickets"])
        trans_amounts_data = np.log(self._data["totalAmounts"])
        skewness = round(trans_tickets_data.skew(), 2)
        kurtosis = round(trans_tickets_data.kurt(), 2)
        #print(f"偏度：{skewness},峰度：{kurtosis}")
        self._data["totalTickets"] = trans_tickets_data
        self._data["totalAmounts"] = trans_amounts_data
        #print(self._data)
        return self._data.to_csv("./110movie_value_data.csv", index=False)
# path = "./110box_office_merge.csv"
# visual = Visual(path)
# visual.fill_null()
# visual.adjustment_skewness_kurtosis("IMDB_rating")
# visual.adjustment_skewness_kurtosis("movie_time")
# visual.logarithmic_trans()
