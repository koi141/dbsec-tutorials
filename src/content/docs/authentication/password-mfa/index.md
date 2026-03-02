---
title: 多要素認証
description: Oracle Mobile Authenticator（OMA）を使用したOracle Databaseの多要素認証（MFA）の概要と前提条件を説明します。
sidebar:
  label: 概要
  order: 0
---

## 概要

Oracle Database では、セキュリティ強化のために多要素認証（MFA）を構成できます。MFA は、ユーザー名とパスワードに加えて、追加の認証要素を要求することでログインを強化します。Oracle Database のローカルユーザー向けMFAは、OMA（Oracle Mobile Authenticator）または Cisco Duo のプッシュ通知、あるいは証明書ベースの方式として説明されています。

以下の接続や認証方式では、現在MFAはサポートされていませんので、注意が必要です。

- 直接ログインの RAS ユーザー
- アプリケーション接続（サーバー間接続を含む）
- 集中管理ユーザー（CMU）接続
- OMA / Duo プッシュ用の外部パスワード・ファイルを使用した管理接続
- HTTP ダイジェスト認証
- ロール・パスワード

また、データベース（またはPDB）がクローズ状態の場合、プッシュ通知MFAは失敗し、証明書ベースの方式のみがサポートされます。

一方で、Autonomous AI Database のドキュメントには、ログイン時MFAはOMAまたはDuoのプッシュ通知で実装することが可能です。チュートリアルでは Oracle Base Database Service を前提に進めますので、Autonomous Database のMFAは別のドキュメントに従って確認してください。

## サポートされるバージョン
ローカルユーザー向けMFAは、次のバージョン条件が示されています。
サポートされるバージョンは次のとおりです。
- 19.28 以降
- 23.9 以降

## チュートリアル
本チュートリアルでは、Oracle Mobile Authenticator (OMA) を使用したMFA接続の設定と手順を解説します。

### 実施内容

本チュートリアルでは、以下の手順を実施します。

1. OCI IAM および Database 側の設定
2. Oracle Mobile Authenticator(OMA)を使用したMFA接続の確認

### 前提条件  

チュートリアルを実施するためには、以下の条件を満たしている必要があります。

- Database 環境
  - Oracle Base Database Service が作成済みであること。
- クライアント環境
  - 本手順では、DBクライアントとしてSQLclを使用します。
  - バージョン情報は以下の通りです
    - ``SQLcl: Release 25.3 Production on Sat Nov 08 19:04:26 2025``
- モバイル認証アプリ
  - プッシュ通知を受け取るために、Oracle Mobile Authenticator (OMA) アプリケーションがインストールされた端末を用意していること。


## 参考リンク


- https://docs.oracle.com/cd/G11854_01/sqlrf/CREATE-USER.html
- https://docs.oracle.com/cd/G11854_01/dbseg/configuring-authentication.html#GUID-10E4F568-0FA3-4F82-99AA-14FB2947469C