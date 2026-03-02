---
title: DBトークン
description: OCI IAM が発行する DBトークンを利用した認証方式の概要と、チュートリアルの前提条件をまとめます。
sidebar:
  label: 概要
  order: 0
---

## 概要

Oracle Databaseへの接続には、従来、ユーザー名とパスワードの組み合わせが一般的に用いられてきました。  
このチュートリアルでは、OCI Identity and Access Management (IAM) が発行するトークンを利用した、よりセキュアな認証方式について解説します。

https://docs.oracle.com/ja-jp/iaas/autonomous-database-serverless/doc/iam-access-database.html

この方式は、IAMユーザーのパスワードを利用するIAM DBパスワード認証と類似していますが、クレデンシャルとしてトークンを使用する点が異なります。
トークン認証は、従来のパスワード認証と比べて有効期限（60分）を持った一時的なクレデンシャルを使用することで、セキュリティを向上させることができます。ただし、トークン認証をサポートしているクライアント接続方式とバージョンに注意が必要です。

## サポートされる接続方式とクライアント

DBトークンでの接続は、クライアントの対応状況（方式・バージョン）に注意が必要です。
Autonomous Database のドキュメントでは、少なくとも Oracle Database Client 19c（19.16 以上）が必要と記載されています。

例として、次が挙げられています。

- **JDBC-Thin**
  - バージョン 19.13.0.0.1 以降
  - バージョン 21.4.0.0.1 以降
- **SQL\*Plus / Oracle Instant Client**
  - バージョン 19.13 以降
  - バージョン 21.4 以降

参照ドキュメント (JDBC): <https://docs.oracle.com/en/database/oracle/oracle-database/19/jjdbc/client-side-security.html#GUID-62AD3F23-21B5-49D3-8325-313267444ADD>  
参照ドキュメント (OCI): <https://docs.oracle.com/en/database/oracle/oracle-database/19/lnoci/introduction.html#GUID-02C903AA-30C9-487E-AD25-9FBF3856D177>


## 注意事項

DBトークンでデータベース・アクセスを行う場合、TCPS（TLS）接続が必要です。また、DBトークンを渡す接続ではネイティブ・ネットワーク暗号化は構成できず、TLSのみがサポートされる旨が記載されています。

Base Database や Exadata のようなユーザー管理の Database サービスでは TLS を構成するために証明書管理が必要になります。  
一方 ADB はデフォルトで TLS 接続（ウォレット利用）が前提のため、この認証方式はより適しています。


## チュートリアル

### 実施内容

チュートリアルでは以下の手順を実施します。

1. OCI CLIを使用して「DBトークン」を取得します。資格証明としてはAPIキーを使用します。
2. 取得したトークンを使用し、Autonomous Database にアクセスします。

また、発展的な内容として、手順の最後にインスタンス・プリンシパルを使用したアクセスも試してみます。これにより、クライアント環境にクレデンシャルを残さない、より高度なことを行うことができます。

### 前提条件

本手順を実施するために、以下の条件を満たしている必要があります。

- Database環境
  - データベースがTLS接続できるように構成されていること。
  - 今回はAutonomous Databaseを使用します。Autonomous AI DatabaseはmTLS接続を使用するため、追加のセットアップは不要です。
  - Autonomous AI Database の作成方法等については  
    [OCIチュートリアル「101: ADBインスタンスを作成してみよう」](https://oracle-japan.github.io/ocitutorials/adb/adb101-provisioning/) を参照ください。
  - また、mTLS接続には Wallet（クライアント証明書）が必要になりますので、OCI コンソールからダウンロードしておきます。

- クライアント環境
  - 本手順では、DBクライアントとしてSQLclを使用します。
  - バージョン情報は以下の通りです：
    - `SQLcl: Release 25.3 Production on Sat Nov 08 19:04:26 2025`

