import pandas as pd
import json
#每週票房json檔匯整成年度資料的csv檔
class Converter:
    def __init__(self,path):
        self._path = path
        self._list = []
        self._transdata = []
        self._merge = pd.DataFrame()
    #將四個json檔轉成Dataframe
    def get_json(self):
        data_list = []
        for item in self._path:
            with open(item) as file:
                url_json = json.load(file)
            url_json = url_json["list"]
            df = pd.DataFrame(url_json)
            data_list.append(df)
        self._list = data_list
        return True
    #挑選需要的欄位資料
    def choose_columns(self):
        data_list = []
        for item in self._list:
            df = item[["country", "name", "releaseDate", "issue",
                         "produce", "theaterCount", "totalTickets", "totalAmounts"]]            
            new_df = pd.DataFrame(df)
            #print(new_df.info())
            data_list.append(new_df)
        self._transdata = data_list
        return True
    #合併四個表格（方向：上下合併）
    def merge_dataframe(self):
        merge_df = pd.concat(self._transdata, ignore_index=True)
        self._merge = merge_df
        return True
    #剔除重複片名的列（以票房較低者做剔除標準）
    def drop_duplicate_value(self):
        name_duplicate = self._merge.sort_values(by=['name', 'totalAmounts'], ascending=False, ignore_index=True)
        name_duplicate.drop_duplicates(subset="name", keep="first", inplace=True)
        final_df = pd.DataFrame(name_duplicate)
        final_df.reset_index(inplace=True, drop=True)
        return final_df.to_csv("./110box_office_done.csv", index=False)

# json_data = ["./boxoffice20210101_20210331.json","./boxoffice20210401_20210630.json","./boxoffice20210701_20210930.json","./boxoffice20211001_20211231.json"]   

# con = Converter(json_data)
# con.get_json()
# con.choose_columns()
# con.merge_dataframe()
# con.drop_duplicate_value()
