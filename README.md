# kawariniyomuhito-tweet

- 本リポジトリはTwitterへの予約投稿機能を提供するwebアプリケーションです。
- サーバ上で動作し、PC/モバイル端末等からwebでアクセスして使用します。
- 定期的にcronで起動されるスクリプトが予約されたツイートをTwitter APIを使用して投稿します。
- 簡単に実装するために、Python3と軽量なフレームワークbottle、ディプロイ時にはuWSGIを使用します。
- フロントエンドは、javascript、jQueryで実装しています。

## 動作環境
- Linux/MacOS
- Python3 (動作は3.7.0で確認)
  - 必要となるpackageは以下:  
    - bottle  
- SQLite3
- uWSGI

## コードの構成
├── README.md  
├── config.py.default  設定ファイル(default)  
├── crontab.sample  CRON設定サンプル  
├── db_create_tables.py  DB操作スクリプト  
├── exec.sh  アプリ実行スクリプト  
├── favicon.ico  
├── index.py  アプリ本体  
├── index.tpl  アプリテンプレート(index.html用)  
├── sched_tweet.py  予約投稿スクリプト(CRON用)  
├── scripts  
│   └── apioperations.js  top.html用Javascript  
├── top3.tpl  アプリテンプレート(top.html用)  
├── twitter_client.py  Twitter API操作スクリプト  
└── uwsgi.ini.default  uWSGI設定サンプル  

## 導入手順
- サーバに環境を整備する。
  - Python3および必要なパッケージのインストール(bottle他)
  - SQLite3, uWSGIのインストール(yum install <package name>)
  - 利用するポートを開く。
- 導入先サーバに本リポジトリをcloneする。
- config.py.defaultを編集し、config.pyを作成。Twitter API tokenなどを設定する。
- 初期ユーザ作成 (以下をCUIで実行し、"0"で初期化後、"02"でユーザ・パスワード登録)
  - > python db_create_tables.py
- uwsgi.ini.defaultを編集し、uwsgi.iniを作成。
- CRONの設定(> crontab -e で編集。サンプルはcrontab.sampleを参照)
- 実行 (> uwsgi uwsgi.ini)
- 停止 (> uwsgi --stop /var/run/uwsgi/uwsgi.pid)
  
## スクリーンショット
https://github.com/tomodaton/kawariniyomuhito-tweet/blob/master/schetweet_screenshot.jpg
