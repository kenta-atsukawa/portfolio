import datetime

def save_csv(df):
    to_day = str(datetime.date.today())
    to_day = to_day.replace("-","")
    name = "data/suumo_oshiage"
    df.to_csv(name + "_" + to_day + ".csv",index=False)