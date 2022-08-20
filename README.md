# Python-use-Notion-API
App using Notion API

## 概要 Description
Notion API を使用して Notion データベースを操作します。  
Work with Notion databases using the Notion API.  

## 特徴 Features

- notion-clienを使用してbotion APIを操作  
	Working with notion API using notion-clien  
- データベースの内容をJSONファイルに出力  
	Output database contents to JSON file  
- データベースのデータ更新のテスト。辞書をリテラルで与えて更新  
	Testing database data updates. Update by giving a dictionary in literal  
- CSV ファイルを読んでデータベースを更新  
	Read CSV file and update database  
- データベースのデータ削除  
	Delete database data  

## 依存関係 Requirement

- Notion 2022年7月のNotionサービス  
- Python 3.8.5  
- notion-client 1.0.0  

追加される Notion データベースと追加するデータは次のリンクで紹介したものが必要です。  

- データベース：『[ブログ記事管理](https://www.notion.so/03bc19abb3594cc5bf1d156615aab943?v=53c6671107e543e0b34c2e04ad09e4f0)』
- データベースの記事：『[ブログの記事を管理する(使い方)【Notionデータベース】](/entry/notion/blog/usage)』
- 追加するデータの記事：『[はてなブログのスターとブックマークの数を取得するアプリ【フリー】](get-stars-bm-exe)』

## 使い方 Usage

notion_blog.pyのswitch変数を1～4に変えて起動する。  
Start by changing the switch variable in the source code to 1 to 4.  

## インストール方法 Installation

	pip install notion-client

## プログラムの説明サイト Program description site

[〖実践〗Notion API の使い方【Python】 - プログラムでおかえしできるかな](https://juu7g.hatenablog.com/entry/Python/blog/notion-api)  



## 作者 Authors
juu7g

## ライセンス License
このソフトウェアは、MITライセンスのもとで公開されています。LICENSE.txtを確認してください。  
This software is released under the MIT License, see LICENSE.txt.

