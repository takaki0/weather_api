# Wether API

Wether APIは、バックエンドはPython/Flaskで作成したWeb-APIです。  
フロントはReactで作成されてます。

都市名と期間を指定して、その都市の気象情報（未来日付の場合は予測値）を表示するアプリです。

気象情報APIは、DarkSkyを利用しました。
https://darksky.net/dev
(Powered by Dark Sky, https://darksky.net/poweredby/)

※本当は株価APIから情報を取得、同業界どうしの企業比較、各種指標を選択してグラフ化、機械学習による株価予測、などを実装したかったのですが、無料で使える株価APIがあまりなくいったん断念して代わりに気象情報を使うことにしました。

## サイトURL
http://ec2-3-112-209-42.ap-northeast-1.compute.amazonaws.com/

## 主な機能

- 都市名から気象情報検索・表示  
- 気象情報グラフ化（予定）
- 都市間気象比較（予定）
- 機械学習による気象情報予測（予定）

## 注目して欲しい点
- DIを利用し、オニオンアーキテクチャっぽくしているところ。
- ３種類のサーバーサイド言語を利用しているところ（予定）
- CircleCIとAWSコードデプロイで自動でのテストとデプロイを実装している点（予定）  
- 実践を意識して、ブランチを切って開発をしている点  
- React-Reduxで実装している点（予定）
- GCPでマップ機能を実装している点

## 使用技術
- 言語/フレームワーク
  - サーバーサイド
    - Python237 / Flask
    - Golang (予定)
    - Kotlin (予定)
  - フロント
  - React
- 開発環境
    - Docker for Mac
    - Pycharm, WebStorm
- 本番環境
    - AWS EC2
- 使用技術
    - CircleCI(予定)
    - GitHub
    - AWS
        - EC2
        - Code deploy
    - GCP
        - Geocoding API
        - Maps JavaScript API
- コードチェック
    -　PEP8, Eslint
- テスト
    - pytest

## 今後の課題
・（未定）
