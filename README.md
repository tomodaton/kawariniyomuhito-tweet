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
TBD

## 導入手順
TBD
