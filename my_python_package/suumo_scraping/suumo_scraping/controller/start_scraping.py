import logging

from suumo_scraping.models import model


def start_scraping():
    formatter = "%(asctime)s:%(message)s"
    logging.basicConfig(filename="./log/test.log", level=logging.INFO, format=formatter)
    try:
        logging.info("info %s", "start")
        model.scraping()
        logging.info("info %s", "end")
    #この書き方は本来するべきではないが、今回はエラーを拾う処理を実装することが第一目的なのでこう書いた
    except Exception as ex:
        logging.error("error")
        print(ex)




