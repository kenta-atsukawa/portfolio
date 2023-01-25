import pandas as pd
import re
import datetime


def preprocessing(name, station, price, sikikinreikin, room, age, address, count_new_list):
    station_line_list = []
    time_move_list = []

    for i in station:
        station_line_list.append(i.split(" ")[0])
        time_move_list.append(i.split(" ")[1])

    station_list = []
    line_list = []

    for i in station_line_list:
        station_list.append(i.split("/")[1])
        line_list.append(i.split("/")[0])

    move_list =[]
    time_list = []

    for i in time_move_list:
        if "歩" in i:
            move_list.append("徒歩")
            time_list.append(re.sub(r"\D", "", i))
        else:
            move_list.append("バス")
            time_list.append(re.sub(r"\D", "", i))

    df=pd.DataFrame()        

    df["station"] = pd.Series(station_list)
    df["line"] = pd.Series(line_list)
    df["move"] = pd.Series(move_list)
    df["time_to_station_min"] = pd.Series(time_list).astype(float)


    price_list = []
    admin_list = []

    for i in price:
        price_list.append(i.split(" ")[0].replace("万円",""))
        admin_list.append(i.split(" ")[3].replace("円",""))

    admin_fee_list = []

    for i in admin_list:
        if i == "-":
            admin_fee_list.append("0")
        else:
            admin_fee_list.append(i)

    df["price_10k"] = pd.Series(price_list).astype(float)
    df["admin_fee"] = pd.Series(admin_fee_list).astype(float)

    sikikin_pre = []
    reikin_pre = []
    deposit_pre = []
    sikibiki_pre = []

    for i in sikikinreikin:
        sikikin_pre.append(i.split(" ")[0])
        reikin_pre.append(i.split(" ")[2])
        deposit_pre.append(i.split(" ")[4])
        sikibiki_pre.append(i.split(" ")[6])

    sikikin_list = []
    reikin_list = []
    deposit_list = []
    sikibiki_list = []

    for i in sikikin_pre:
        a = i.split("敷")[1]
        if "万円" in a:
            sikikin_list.append(a.replace("万円",""))
        else:
            sikikin_list.append(0)

    for i in reikin_pre:
        a = i.split('礼')[1]
        if "万円" in a:
            reikin_list.append(a.replace("万円",""))
        else:
            reikin_list.append(0)

    for i in deposit_pre:
        a = i.split('\xa0')[1]
        if "万円" in a:
            deposit_list.append(a.replace("万円",""))
        else:
            deposit_list.append(0)

    for i in sikibiki_pre:
        a = i.split("\xa0")[1]
        if "万円" in a:
            sikibiki_list.append(a.replace("万円",""))
        elif "-" in a:
            sikibiki_list.append(0)
        else:
            sikibiki_list.append("実費")

    df["sikikin_10k"] = pd.Series(sikikin_list).astype(float)
    df["reikin_10k"] = pd.Series(reikin_list).astype(float)
    df["deposit_10k"] = pd.Series(deposit_list).astype(float)
    df["sikibiki_10k"] = pd.Series(sikibiki_list)

    room_list = []
    area_pre = []
    direction_pre = []

    for i in room:
        room_list.append(i.split(" ")[0])
        area_pre.append(i.split(" ")[2])
        direction_pre.append(i.split(" ")[4])

    area_list = []

    for i in area_pre:
        area_list.append(i.replace("m2",""))

    df["room"] = pd.Series(room_list)
    df["area_m2"] = pd.Series(area_list)
    df["direction"] = pd.Series(direction_pre)

    type_list = []
    age_pre = []

    for i in age:
        type_list.append(i.split(" ")[0])
        age_pre.append(i.split(" ")[2])

    age_list = []

    for i in age_pre:
        if i == "新築":
            age_list.append(0)
        else:
            age_list.append(re.sub(r"\D", "", i))

    df["type"] = pd.Series(type_list)
    df["age_year"] = pd.Series(age_list).astype(float)

    df["scraping_date"] = datetime.date.today()
    df["name"] = pd.Series(name)
    df["address"] = pd.Series(address)

    id_range = 0
    for i in count_new_list:
        id_range = i + id_range


    id_list = []
    to_day = str(datetime.date.today())
    to_day = to_day.replace("-","")
    for i in range(0,id_range):
        if i < 10:
            i = str(i)
            id_list.append(to_day + "000"  + i)            
        elif i >= 10 and i < 100:
            i = str(i)
            id_list.append(to_day + "00" + i)
        elif i >= 100 and i < 1000:
            i = str(i)
            id_list.append(to_day + "0" + i)            
        else:
            i = str(i)
            id_list.append(to_day + i) 

    df["scraping_id"] = pd.Series(id_list)

    df = df.reindex(columns=["scraping_id","scraping_date","name","price_10k","age_year","admin_fee","sikikin_10k","reikin_10k","deposit_10k","sikibiki_10k","line","station","move","time_to_station_min","room","area_m2","direction","type","address"])
    # 最後のページのスクレイピングでは「本日の新着」以外のデータも混ざっている
    # pd.read_html(urls.content)で取得した賃貸価格など
    # それ以外で取得した物件名などは「本日の新着」分のデータしか取得していないのでNULLの部分が出てくる
    # NULLが入っているデータは余分なデータなので削除する
    df.dropna(inplace=True)
    
    return df


