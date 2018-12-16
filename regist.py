import csv
import os.path
from datetime import datetime as dt
from logging import getLogger, StreamHandler, Formatter, DEBUG, FileHandler
import sqlite3
from contextlib import closing

## ログ出力設定
logger = getLogger("気象データ登録")
logger.setLevel(DEBUG)

# コンソール出力設定
stream_handler = StreamHandler()
formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# 登録対象csv名
FILE_NAME = 'data.csv'

# DB名
DB_NAME = 'db.sqlite3'

# DBへの追加用SQL
sql_insert = ("insert into weather_data (data_datetime, temperature, humidity, location_id, created_at, updated_at) "
              "select * from (select ? as data_datetime, ? as temperature, ? as humidity, ? as location_id, "
              "? as created_at, ? as updated_at) as tmp "
              "where not exists (select * from weather_data where location_id = ? and data_datetime = ?)")


def regist_data(db):
    ## ファイル読み込み（CSV形式）
    try:
        file = open(FILE_NAME, newline='')
    except IOError:
        logger.warning('対象ファイルが存在しません：' + FILE_NAME)
        logger.warning('DB登録は行いません：' + FILE_NAME)
    else:
        logger.info('=== > Start DB登録 ==')
        cursor = db.cursor()
        with file:
            reader = csv.reader(file)
            header = next(reader)  # ヘッダーをスキップ

            for row in reader:
                str_time = [dt.now().strftime('%Y-%m-%d %H:%M:%S')]
                add_data = []  # ロケーションID
                add_data.extend(row)  # csvから読み取った情報
                add_data.extend(str_time)  # created_at
                add_data.extend(str_time)  # updated_at
                add_data.append(row[3])  # ロケーションID：DBから取得する
                add_data.append(row[0])  # 対象日時（対象レコードがDBに存在するかの確認に使用する）
                logger.debug('add_data = ' + str(add_data))
                #logger.debug('add_data = ' + sql_insert)
                # レコード追加
                cursor.execute(sql_insert, add_data)

            # コミット
            db.commit()
            logger.info("=== > End DB登録 ==")

        # DB後処理
        cursor.close()


### 実処理（main） ###
def main():
    logger.info('== batch処理開始 ==')

    # DB処理
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, DB_NAME)
    logger.info('db_path = ' + db_path)

    with closing(sqlite3.connect(db_path)) as db:
        regist_data(db)

    logger.info('== batch処理終了 ==')


## main関数を実行
if __name__ == '__main__':
    main()
