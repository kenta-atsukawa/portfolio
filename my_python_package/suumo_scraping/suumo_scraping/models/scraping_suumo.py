import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
  
def suumo_scraping():
    name = []
    station = []
    price = []
    sikikinreikin = []
    room = []
    age = []
    address = []
    count_new_list = []
    url = "https://suumo.jp/jj/chintai/ichiran/FR301FC005/?ar=030&bs=040&ra=013&rn=0045&ek=004506820&cb=0.0&ct=9999999&mb=0&mt=9999999&et=9999999&cn=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&sngz=&po1=09&po2=99&pc=100"     

    urls=requests.get(url)
    # 連続してアクセスするのを防ぐために3秒待つ
    time.sleep(3)
    urls.encoding = urls.apparent_encoding 
    soup=BeautifulSoup()
    soup=BeautifulSoup(urls.content,"html.parser")
    get_url = soup.find("ol",class_="pagination-parts")
    # 物件のページ数を取得
    num_list =[]
    for i in get_url.find_all("li"):
        num_list.append(i.text)
    num = int(num_list[10]) + 1    

      # ページ数分だけスクレイピングを実行
    for p in range(1,num):
        page=str(p)
        url_2="https://suumo.jp/jj/chintai/ichiran/FR301FC005/?ar=030&bs=040&ra=013&rn=0045&ek=004506820&cb=0.0&ct=9999999&mb=0&mt=9999999&et=9999999&cn=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&sngz=&po1=09&po2=99&pc=100" + "&page=" + page
        urls=requests.get(url_2)
        # 連続してアクセスするのを防ぐために3秒待つ
        time.sleep(3)
        soup=BeautifulSoup(urls.content,"html.parser")
        # 「本日の新着」「新着」のタグを検索
        house_info = soup.find_all("span",class_="ellipse_pct ellipse_pct--red")
        # 「本日の新着」「新着」のタグの中で「本日の新着」の数をカウント
        count_new = 0
        for i in house_info:
            if i.text == "本日の新着":
                count_new += 1
        count_new_list.append(count_new)
        # ページ内の「本日の新着」の数が0でないならスクレイピングを実行
        if count_new != 0:
            house_name = soup.find_all("a",class_="js-cassetLinkHref")
            station_name = soup.find_all("div",style="font-weight:bold")
            table_data = pd.read_html(urls.content)
            for h in house_name:
                name.append(h.text)
            for s in station_name:
                station.append(s.text)
        
            for i in range(0,count_new):
                table = table_data[i]
                price.append(table.iloc[0,0])
                room.append(table.iloc[0,2])
                age.append(table.iloc[0,3])
                address.append(table.iloc[0,4])
                sikikinreikin.append(table.iloc[0,1])
        # ページ内の「本日の新着」が0ならスクレイピングをやめる
        else:
            break
    
    return name, station, price, sikikinreikin, room, age, address, count_new_list

