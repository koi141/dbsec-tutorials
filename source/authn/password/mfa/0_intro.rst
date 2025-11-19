############################################
0. はじめに
############################################

***********************
概要
***********************

Oracle Databaseでは、セキュリティ強化のために多要素認証（MFA）をサポートしています。本チュートリアルでは、Oracle Mobile Authenticator (OMA) を使用したMFA接続の設定と手順を解説します。

以下の接続や認証方式では、現在MFAはサポートされていませんので、注意が必要です。

- 直接ログインのRASユーザー
- サーバーとサーバーの間の接続を含むアプリケーション
- 集中管理ユーザー(CMU)接続
- OMAおよびDuoプッシュ用の外部パスワード・ファイルを使用した管理接続
- HTTPダイジェスト認証
- ロール・パスワード

また、Oracle Autonomous Database on Dedicated Exadata Infrastructure および Oracle Autonomous Database Serverless では、プッシュ通知によるMFAはサポートされていません。

サポートされるバージョンは次のとおりです。
- 19.28 以降
- 23.9 以降



***********************
実施内容
***********************
本チュートリアルでは、以下の手順を実施します。（手順の内容は後続のセクションで詳細化されます）

1. OCI IAM および Database 側の設定
2. Oracle Mobile Authenticator(OMA)を使用したMFA接続の確認



***********************
前提条件  
***********************

本手順を実施するために、以下の条件を満たしている必要があります。

- Database 環境
    - Oracle Base Database Service が作成済みであること。
- クライアント環境
    - 本手順では、DBクライアントとしてSQLclを使用します。
    - バージョン情報は以下の通りです
        - ``SQLcl: Release 25.3 Production on Sat Nov 08 19:04:26 2025``
- モバイル認証アプリ
    - プッシュ通知を受け取るために、Oracle Mobile Authenticator (OMA) アプリケーションがインストールされた端末を用意していること。



*****************************************
参考リンク
*****************************************

- https://docs.oracle.com/cd/G11854_01/sqlrf/CREATE-USER.html
- https://docs.oracle.com/cd/G11854_01/dbseg/configuring-authentication.html#GUID-10E4F568-0FA3-4F82-99AA-14FB2947469C



*****************************************
設定する初期化パラメータ
*****************************************

MFA設定では以下の初期化パラメータを設定します。

- MFA_OMA_IAM_DOMAIN_URL
- MFA_SMTP_HOST（任意）
- MFA_SMTP_PORT（任意）
- MFA_SENDER_EMAIL_ID（任意）
- MFA_SENDER_EMAIL_DISPLAYNAME（任意）