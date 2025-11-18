############################################
0. イントロダクション
############################################

***********************
概要
***********************

Oracle Databaseへの接続には、従来、ユーザー名とパスワードの組み合わせが一般的に用いられてきました。このチュートリアルでは、OCI Identity and Access Management (IAM) が発行するトークンを利用した、よりセキュアな認証方式について解説します。

https://docs.oracle.com/ja-jp/iaas/autonomous-database-serverless/doc/iam-access-database.html

| この方式は、IAMユーザーのパスワードを利用するIAM DBパスワード認証と類似していますが、クレデンシャルとしてトークンを使用する点が異なります。トークン認証は、従来のパスワード認証と比べて有効期限（60分）を持った一時的なクレデンシャルを使用することで、セキュリティを向上させることができます。
| ただし、トークン認証をサポートしているクライアント接続方式とバージョンに注意が必要です。

- JDBC-Thin
    - バージョン 19.13.0.0.1 以降
    - バージョン 21.4.0.0.1 以降
- SQL*Plus / Oracle Instant Client
    - バージョン 19.13 以降
    - バージョン 21.4 以降

参照ドキュメント (JDBC): https://docs.oracle.com/en/database/oracle/oracle-database/19/jjdbc/client-side-security.html#GUID-62AD3F23-21B5-49D3-8325-313267444ADD

参照ドキュメント (OCI): https://docs.oracle.com/en/database/oracle/oracle-database/19/lnoci/introduction.html#GUID-02C903AA-30C9-487E-AD25-9FBF3856D177

DBトークンを使用したログインのためには、DatabaseにTLS接続されていることが必須となります。

| Base DatabaseやExadataのようなユーザー管理のDatabaseサービスの場合、TLS接続を構成するために、証明書管理が必要となります。
| 一方ADBの場合はデフォルトで TLS接続が構成されているため、特別なセットアップは不要であり、この認証方式はより適しています。



***********************
実施内容
***********************

本手順では以下の手順を実施します。

1. OCI CLIを使用して「DBトークン」を取得します。資格証明としてはAPIキーを使用します。
2. 取得したトークンを使用し、Autonomous Database にアクセスしますするまでを行っていきます。
3. 発展的な内容として、手順の最後にインスタンス・プリンシパルを使用したアクセスも試してみます。これにより、クライアント環境にクレデンシャルを残さない、より高度なことを行うことができます。



***********************
前提条件  
***********************

本手順を実施するために、以下の条件を満たしている必要があります。

- Database環境
    - データベースがTLS接続できるように構成されていること。
    - 今回はAutonomous Databaseを使用します。Autonomous AI DatabaseはmTLS接続を使用するため、追加のセットアップは不要です。
    - Autonomous AI Database の作成方法等については `OCIチュートリアル「101: ADBインスタンスを作成してみよう」 <https://oracle-japan.github.io/ocitutorials/adb/adb101-provisioning/>`__ を参照ください。
    - また、mTLS接続には Wallet（クライアント証明書）が必要になりますので、OCI コンソールからダウンロードしておきます。
- クライアント環境
    - 本手順では、DBクライアントとしてSQLclを使用します。
    - バージョン情報は以下の通りです
        - ``SQLcl: Release 25.3 Production on Sat Nov 08 19:04:26 2025``



***********************
関連するORAエラー
***********************

この手順にて関連するエラーのリンクです。

- https://docs.oracle.com/error-help/db/ora-18718/
- https://docs.oracle.com/error-help/db/ora-25708/
- https://docs.oracle.com/error-help/db/ora-18718/