"""
Notion用プロパティデータ作成
"""
import re

def set_properties(url:str="", title:str="", published:str="", updated:str="", 
                    bookmark:int=0, yellow:int=0, green:int=0, red:int=0, blue:int=0, purple:int=0, 
                    category:str="", eye_catch:str=""):
    """
    引数を値にしたNotionデータベースのプロパティ用辞書を作成する
    Args:
        any:    get_hatena_infoで出力したCSVの各カラム
    Returns:
        dict:   特定Notionデータベースのプロパティ用辞書
    """
    # カスタマイズURLはURLのentryより後ろだけ
    c_url = re.sub("^.+/entry/", "", url)
    # CSVを読み込んだデータはすべて文字列なので数値は変換が必要
    star_num = int(yellow) + int(green) + int(red) + int(blue) + int(purple)
    bookmark_num = int(bookmark)
    # マルチセレクト用のデータはカンマ区切りの文字列("a,b")なので"name"をキーにした辞書のリストにする
    c1 = [{"name":c} for c in category.split(",")]
    # t1 = [{"name":t} for t in tags]
    properties = {
                "スター": {
                    "number": star_num
                },
                "掲載日": {
                    "date": {
                        # タイムゾーンは動かないので日時に標準時との差を付加する
                        "start": published+"+09:00",
                        # "time_zone": "Asia/Tokyo"
                    }
                },
                "アイキャッチ画像": {
                    "files": [
                        {
                            "name": eye_catch,
                            "external": {
                                "url": eye_catch
                            }
                        }
                    ]
                },
                "ブックマーク": {
                    "number": bookmark_num
                },
                "カスタムURL": {
                    "rich_text": [
                        {
                            "text": {
                                "content": c_url,
                            }
                        }
                    ]
                },
                "カテゴリ": {
                    "multi_select": list(c1)
                },
                # "タグ": {
                #     "multi_select": list(t1)
                # },
                "リンク": {
                    "url": url
                },
                "タイトル": {
                    "title": [
                        {
                            "text": {
                                "content": title
                            }
                        }
                    ]
                },
            }
    # 設定がないキーは削除する
    if category == "":
        del properties["カテゴリ"] 
    if eye_catch == "":
        del properties["アイキャッチ画像"] 
    return properties
