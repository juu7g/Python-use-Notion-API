"""
はてなブログの記事をNotionデータベースに追加
"""
from notion_client import Client
# import logging
from notion_client import APIErrorCode, APIResponseError
import json
import csv
import os, sys
from datetime import datetime
import notion_db_scm

class NotionAPI():
    """
    Notion APIを操作するクラス
    """
    def __init__(self) -> None:
        """
        初期設定
        Notionはインテグレーションからシェアされたデータベースに対して操作できるようになる
        そのためインテグレーションのトークンとシェアされたデータベースのIDが必要になる
        """
        self.AUTH = os.getenv("py_notion_int_token")    # Notionのインテグレーショントークン
        self.DATABASE_ID = os.getenv("py_notion_db")    # NotionデータベースID
        self.notion = Client(auth=self.AUTH)            # Notion Clientのインスタンス作成

    def get_database(self) -> dict:
        """
        データベースを取得
        Returns:
            dict:   データベースの内容
        """
        try:
            my_page = self.notion.databases.query(
                **{
                    "database_id": self.DATABASE_ID,
                }
            )
        except APIResponseError as error:
            # if error.code == APIErrorCode.ObjectNotFound:
            if error.code == APIErrorCode.ValidationError:
                # For example: handle by asking the user to select a different database
                print("データベースIDを確認してください")
            else:
                # Other error handling code
                print("インテグレーションのトークンを確認してください")
                # logging.exception(error.code)
        return my_page

    def dump_results(self, doc:dict):
        """
        辞書をjson形式のファイルに出力
        Args:
            dict:   出力したい辞書
        """
        file_name = f"myDictionary_{datetime.now().strftime('%m%d')}.json"
        jf = open(file_name, "w", encoding="utf_8_sig")
        json.dump(doc, jf, ensure_ascii=False)
        jf.close()

    def get_page_by_url(self, url:str) -> dict:
        """
        データベースを取得
        　データベースの「リンク」プロパティを引数でフィルタリングした結果
        Args:
            str:    記事のURL(データベースのキーとして扱う)
        Returns:
            dict:   データベースの内容
        """
        my_page = None
        try:
            my_page = self.notion.databases.query(
                **{
                    "database_id": self.DATABASE_ID,
                    "filter":{"or":[{
                        "property":"リンク",
                        "url":{"equals":url}
                    }]}
                }
            )
        except APIResponseError as error:
            # if error.code == APIErrorCode.ObjectNotFound:
            if error.code == APIErrorCode.ValidationError:
                # For example: handle by asking the user to select a different database
                print("データベースIDを確認してください")
            else:
                # Other error handling code
                print("インテグレーションのトークンを確認してください")
                # logging.exception(error.code)
        return my_page

    def append_page_2database(self, properties:dict):
        """
        データベースに引数の内容を追加
        Args:
            dict:   記事情報
        Returns:
            dict:   操作の結果
        """
        try:
            my_page = self.notion.pages.create(
                **{
                    "parent":{"database_id": self.DATABASE_ID},
                    "properties":properties
                }
            )
        except APIResponseError as error:
            if error.code == APIErrorCode.ObjectNotFound:
                # For example: handle by asking the user to select a different database
                print("データベースIDを確認してください")
            else:
                # Other error handling code
                print(f"target properties:{properties}")
                # logging.exception(error.code)
        return my_page

    def update_page(self, page_id:str, properties:dict) -> dict:
        """
        データベースの既存のpage_idのデータに引数の内容を更新
        Args:
            str:    page ID
            dict:   記事情報
        Returns:
            dict:   操作の結果
        """
        try:
            my_page = self.notion.pages.update(
                **{
                    "page_id":page_id,
                    "properties":properties
                }
            )
        except APIResponseError as error:
            if error.code == APIErrorCode.ObjectNotFound:
                # For example: handle by asking the user to select a different database
                print("データベースIDを確認してください")
            else:
                # Other error handling code
                # logging.exception(error.code)
                pass
        return my_page

    def delete_block(self, page_id:str) -> dict:
        """
        データベースから引数のデータを削除
        Args:
            str:    page ID
        Returns:
            dict:   操作の結果
        """
        try:
            my_page = self.notion.blocks.delete(
                **{
                    "block_id":page_id
                }
            )
        except APIResponseError as error:
            if error.code == APIErrorCode.ObjectNotFound:
                # For example: handle by asking the user to select a different database
                print("データベースIDを確認してください")
            else:
                # Other error handling code
                # logging.exception(error.code)
                pass
        return my_page

if __name__ == '__main__':

    notion_api = NotionAPI()

    """ switchで処理を切り分け
        1: データベースの内容をJSONファイルに出力
        2: データベースのデータ更新のテスト。辞書をリテラルで与えて更新
        3: CSVファイルを読んでデータベースを更新。
        4: データベースのデータ削除
    """
    switch = 3

    if switch == 1:
        doc = notion_api.get_database() # データベースを取得
        notion_api.dump_results(doc)    # JSONファイルに出力
    elif switch == 2:
        data = {"url":"https://xxx.hatenablog.com/entry/xxx", "title":"タイトル", 
            "published":"2022-06-01 21:50:15", "yellow":37, 
            "category":'シニア, 暮らし'
            }

        properties = notion_db_scm.set_properties(**data)           # プロパティ用辞書作成
        notion_api.append_page_2database(properties=properties)     # 追加
    elif switch == 3:
        if len(sys.argv) > 1:
            file_name = sys.argv[1]
        else:
            print(f"ファイルを指定してください")
            input("\n確認したらEnterキーを押してください")
            sys.exit()
        
        print(f"{file_name} の内容で更新します。")

        try:
            # CSV(1行目がカラム定義)を辞書として読んで
            with open(file_name, newline='', mode="r", encoding="utf-8-sig") as csvfile:
                spamreader = csv.DictReader(csvfile)
                for row in spamreader:
                    properties = notion_db_scm.set_properties(**row)        # プロパティ用辞書作成
                    # 更新データが既にデータベースにあるかをurlでチェック
                    doc = notion_api.get_page_by_url(row.get("url"))        # 問合せ(urlでフィルタリング)
                    if doc:
                        if len(doc["results"]) > 0:
                            page_id = doc["results"][0].get("id")
                            notion_api.update_page(page_id, properties)     # 更新
                            print(f"更新：{row.get('title')}")
                        else:
                            notion_api.append_page_2database(properties)    # 追加
                            print(f"追加：{row.get('title')}")
                    else:
                        # データベース読み込みに問題があったので中断
                        break
                print(f"処理終了")
        except Exception as e:
            print(f"エラーが発生しました：{e}")
    elif switch == 4:
        print("データベースの要素を削除します")
        doc = notion_api.get_database()     # データベースを取得
        if len(doc["results"]) > 0:
            page_ids = [obj["id"] for obj in doc["results"] if obj["object"] == "page"] # 結果からpage_idを取得
            page_titles = [obj["properties"]["タイトル"]["title"][0]["text"]["content"] for obj in doc["results"] if obj["object"] == "page"] # 結果からタイトルを取得
            for page_id, page_title in zip(page_ids, page_titles):
                notion_api.delete_block(page_id)    # データベースから削除
                print(f"削除：{page_title}")
        print("削除完了")
    input("\n確認したらEnterキーを押してください")