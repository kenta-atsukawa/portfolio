def deco(func):
    def message(*args, **kwargs):
        print("スクレイピングを開始します")
        print("スクレイピング中です...")
        func(*args, **kwargs)
        print("スクレイピング終了")
    return message
