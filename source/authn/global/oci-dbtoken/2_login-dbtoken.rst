############################################
2. トークンを取得してアクセスする
############################################

このセクションでは、OCI CLIを使用してDBトークンを取得し、そのトークンを使ってAutonomous Databaseへの接続を試みます。

.. topic:: 実施内容

    + DBトークンの取得 
    + DB接続設定の編集
    + Adminユーザーのトークンで接続し権限を確認
    + Devユーザーのトークンで接続し権限を確認


***************************************************
DBトークンを取得する 
***************************************************

次のコマンドを実行しDBトークンを取得します。ここで使用するAPIキー（プロファイル）は、作成した ``iamuser-hr-admin-01`` ユーザーのものを使用してください。

.. code-block:: bash

    $ oci iam db-token get

    or 

    $ oci iam db-token get --profile iamuser-hr-admin-01

コマンドの実行結果として、DBトークンとそれに対応する秘密鍵が保存されたパスが表示されます。

.. code-block:: 

    Private key written at /home/ubuntu/.oci/db-token/oci_db_key.pem
    db-token written at: /home/ubuntu/.oci/db-token/token

作成されたファイルを確認します。デフォルトでは、秘密鍵 (oci_db_key.pem)、公開鍵 (oci_db_key_public.pem)、そしてDBトークン本体 (token) の3つのファイルが ``$HOME/.oci/db-token/`` ディレクトリに生成されます。

.. code-block:: bash

    $ tree .oci/db-token/
    .oci/db-token/
    ├── oci_db_key.pem
    ├── oci_db_key_public.pem
    └── token

DBトークンは JWT (JSON Web Token) 形式です。中身を `JSON Web Tokens - jwt.io <https://www.jwt.io/ja>`__ などのデコーダーツールで確認することができます。

.. dropdown:: デコードした例

    .. code-block:: json
        :caption: ヘッダー

        {
            "kid": "scoped_sk_db_token_syd_1713219551687",
            "alg": "RS256"
        }

    .. code-block:: json
        :caption: ペイロード

        {
            "sub": "ocid1.user.oc1..aaaaaaaaaaaaaaaaaaaaaaaaaa",
            "iss": "authService.oracle.com",
            "ptype": "user",
            "sess_exp": "Sat, 08 Nov 2025 17:19:55 UTC",
            "dbUserName": "iamuser-hr-admin-01",
            "userName": "iamuser-hr-admin-01",
            "aud": "urn:oracle:db:ocid1.tenancy.oc1..xxxxxxxxxxxxxxxxxxxxxx",
            "domain_name": "domain-db",
            "pstype": "natv",
            "ttype": "scoped_access",
            "scope": "urn:oracle:db::id::*",
            "exp": 1762604395,
            "iat": 1762600795,
            "jti": "f5a3618f-4b3b-43d8-b679-0eaea2853ca3",
            "tenant": "ocid1.tenancy.oc1..xxxxxxxxxxxxxxxxxxxxxx",
            "jwk": "{\"kid\":\"ocid1.tenancy.oc1..xxxxxxxxxxxxxxxxxxxxxx\",\"n\":\"qsx0rUB6MREieANpIYe0y1TCYb70uNuJgPOommm9aYGrOqomDW5Hgh1U08mGvPsr9AgewCExUQZdnxLegyo6QYi0y2xlD49zn5BMW-sk9m-U0IdmpFGIHHFd3NYwfxEBSxOhdjE86XObZypHtPQetxHRTLtwLt5Cjak91aEwSCUbKPaoaRkFE7ZBI3K7bNxKayey8AebXfZyzADKivYIqEtHOntu6d0kvLZ-WXDTJTOy7Ybds2uBg0adrls4h-lF1IRYyjXZEsETtVDJ788jkWVGMnCgBOlVdyFUrT60mVTsh6mlD5VZVPsSukdHQFyDJj62D5u9ckaPpF3Iz7LaSw\",\"e\":\"AQAB\",\"kty\":\"RSA\",\"alg\":\"RS256\",\"use\":\"sig\"}"
        }

    ``userName`` より adminユーザーであることが確認できます。



***************************************************
DB接続設定を編集する
***************************************************

DBトークンを使用して接続するために、Walletに含まれている ``tnsnames.ora`` ファイルに設定を追記します。

ADBの場合、Walletを解凍することで該当のファイルを見つけることができます。

.. code-block:: bash

    $ adb-wallet unzip Wallet_UQG5XBZV5LIND8ZF.zip 
    Archive:  Wallet_UQG5XBZV5LIND8ZF.zip
    
    $  adb-wallet tree
    .
    ├── README
    ├── Wallet_UQG5XBZV5LIND8ZF.zip
    ├── cwallet.sso
    ├── ewallet.p12
    ├── ewallet.pem
    ├── keystore.jks
    ├── ojdbc.properties
    ├── sqlnet.ora
    ├── tnsnames.ora
    └── truststore.jks

    1 directory, 10 files


``tnsnames.ora`` を開き、使用したい接続記述子に ``security=(TOKEN_AUTH=OCI_TOKEN)`` パラメータを追記します。接続記述子名は、任意で ``db-token`` などに変更しても構いません。

.. code-block::
    :caption: 追記例
    
    # 変更前（before） 
    uqg5xbzv5lind8zf_medium = (
        description= 
            (retry_count=20)
            (retry_delay=3)
            (address=(protocol=tcps)(port=1522)(host=adb.ap-sydney-1.oraclecloud.com))
            (connect_data=(service_name=g884bffdded7d8c_uqg5xbzv5lind8zf_medium.adb.oraclecloud.com))
            (security=(ssl_server_dn_match=yes))
        )

    # 変更後（after） 
    db-token = (
        description= 
            (retry_count=20)
            (retry_delay=3)
            (address=(protocol=tcps)(port=1522)(host=adb.ap-sydney-1.oraclecloud.com))
            (connect_data=(service_name=g884bffdded7d8c_uqg5xbzv5lind8zf_medium.adb.oraclecloud.com))
            (security=(ssl_server_dn_match=yes)(TOKEN_AUTH=OCI_TOKEN))
        )

.. note::

    tokenを別の場所においている場合はその位置を ``TOKEN_LOCATION`` で指定します。この際、tokenとともに秘密鍵も移動させておくことに気をつけておきます。

    .. code-block::
        :caption: 例
        
        db-token = (
            description= 
                (retry_count=20)
                (retry_delay=3)
                (address=(protocol=tcps)(port=1522)(host=adb.ap-sydney-1.oraclecloud.com))
                (connect_data=(service_name=g884bffdded7d8c_uqg5xbzv5lind8zf_medium.adb.oraclecloud.com))
                (security=(ssl_server_dn_match=yes)(TOKEN_AUTH=OCI_TOKEN)(TOKEN_LOCATION=/home/ubuntu))
            )



***************************************************
Adminユーザーのトークンで接続し権限を確認
***************************************************

接続する準備が整ったところで、実際に接続を行ってみます。

.. code-block:: sql

    $ ~ sql /nolog

    SQL> connect /@db-token
    Connected.

接続後、ユーザー名、付与されているロールおよび権限を確認してみます。

.. code-block:: sql

    -- DBユーザー名を確認
    SQL> show user
    USER is "DBUSER_IAM"

    -- 持っている権限を確認
    SQL> select * from session_privs;

    PRIVILEGE      
    ______________ 
    CREATE SESSION 

    -- 持っているロールを確認する
    SQL> select * from session_roles;

    ROLE            
    _______________ 
    GLROLE_HR_ADMIN 

    -- HRスキーマの管理権限を持つため、表作成・削除が成功する
    SQL> create table hr.test (
    2    id number
    3* );

    Table HR.TEST created.

    SQL> drop table hr.test;

    Table HR.TEST dropped.

トークンを発行したユーザー(``iamuser-hr-admin-01``)が、Database側でグローバルユーザーとしてマッピングされ、対応する ``GLROLE_HR_ADMIN`` ロールでログインできていることが確認できます。



***************************************************
Devユーザーのトークンで接続し権限を確認
***************************************************

次に、権限の異なるユーザーのトークンを使用し、接続時の権限の違いを確認します。セットアップ時に用意した ``iamuser-hr-dev-01`` ユーザーのAPIキーを使用してDBトークンを取得してみます。

.. code-block:: bash

    $ oci iam db-token get --profile iamuser-hr-dev-01
    Private key written at /home/ubuntu/.oci/db-token/oci_db_key.pem
    db-token written at: /home/ubuntu/.oci/db-token/token
    db-token is valid until 2025-11-08 22:29:05

接続してみます。

.. code-block:: sql

    $ ~ sql /nolog

    SQL> connect /@db-token
    Connected.

ロールと権限を確認し、 ``iamuser-hr-admin-01`` の時と異なるロールが付与されているかを確認します。

.. code-block:: sql

    -- DBユーザー名を確認
    SQL> show user
    USER is "DBUSER_IAM"

    -- 持っている権限を確認
    SQL> select * from session_privs;

    PRIVILEGE      
    ______________ 
    CREATE SESSION 

    -- 持っているロールを確認
    SQL> select * from session_roles;

    ROLE          
    _____________ 
    GLROLE_HR_DEV 

    -- HRスキーマへのSELECTは成功する
    SQL> select * from hr.departments;

    DEPT_ID DEPT_NAME  LOCATION 
    _______ __________ ________ 
        10 Accounting Tokyo    
        20 Reserch    Osaka    
        30 Sales      Nagoya   
        40 HR         Fukuoka  

    -- HRスキーマへの表作成は権限が足りないため失敗する
    SQL> create table hr.test (
    2    id number
    3* );

    Error starting at line : 1 in command -
    create table hr.test (
    id number
    )
    Error report -
    ORA-01031: insufficient privileges

    https://docs.oracle.com/error-help/db/ora-01031/
    01031. 00000 -  "insufficient privileges"
    *Document: YES
    *Cause:    A database operation was attempted without the required
            privilege(s).
    *Action:   Ask your database administrator or security administrator to grant
            you the required privilege(s).

これでトークンを発行したユーザー(``iamuser-hr-dev-01``)が、同じマッピング先のDBユーザー(``DBUSER_IAM``)でログインしましたが、付与されたロールは (GLROLE_HR_DEV) となり、権限が分離されていることが確認できました。


次のセクションでは、よりセキュアな認証方法であるインスタンスプリンシパルをつかってDBトークンを取得し、接続してみます。