from suumo_scraping.models import scraping_suumo
from suumo_scraping.models import process
from suumo_scraping.models import save_csv


def deco(func):
    def message(*args, **kwargs):
        print("スクレイピングを開始します")
        print("スクレイピング中です...")
        func(*args, **kwargs)
        print("スクレイピング終了")
    return message

@deco    
def scraping():
    name, station, price, sikikinreikin, room, age, address, count_new_list = scraping_suumo.suumo_scraping()
    df = process.preprocessing(name, station, price, sikikinreikin, room, age, address, count_new_list)
    save_csv.save_csv(df)