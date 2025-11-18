############################################
3. インスタンスプリンシパルを使ってログインする
############################################

前のセクションではAPIキーを使用してDBトークンを取得しましたが、このセクションでは、クライアント環境に資格証明を一切残さないインスタンス・プリンシパルを利用してDBトークンを取得し、データベースにアクセスする手順を試みます。

.. topic:: 実施内容

    + OCIコンピュートインスタンスの準備とIAMポリシーの作成
    + コンピュートインスタンスにOCI CLIをインストールする
    + DBユーザーを作成する
    + トークンを使用してアクセスする



*******************************************************
OCIコンピュートインスタンスの準備とIAMポリシーの作成
*******************************************************

インスタンス・プリンシパルを使用するには、Databaseにアクセスするコンピュートインスタンスと、そのインスタンスを認証するためのIAM設定が必要です。
ここでは詳細な手順は省きますが、Databaseアクセスに使用するOCIコンピュートインスタンスを準備しておきます。

作成したコンピュートインスタンスのOCIDを指定し、動的グループを作成します。これにより、特定のインスタンスがIAMのプリンシパルとして扱えるようになります。

.. figure:: ../_img/domain-policy-03.png

作成した動的グループに対して、Autonomous Databaseへの接続権限を付与するIAMポリシーを設定します。動的グループは今回使用しているIdentity Domain内に作成した場合、動的グループ名は ``<domain名>/<動的グループ名>`` で指定します。

.. code-block::

    Allow dynamic-group 'domain-db'/'dbclient' to use autonomous-database-family in tenancy



***************************************************
コンピュートインスタンスにOCI CLIをインストールする
***************************************************

準備したコンピュートインスタンスにOCI CLIをインストールし、インスタンス・プリンシパル認証でOCI CLIが正常に実行できるかを確認します。

インスタンスプリンシパルで認証を行う場合、オプションに ``--auth instance_principal`` を指定します。

.. code-block:: bash

    $ oci iam region list --auth instance_principal
    {
        "data": [
            {
            "key": "AMS",
            "name": "eu-amsterdam-1"
            },
            {
            "key": "ARN",
            "name": "eu-stockholm-1"
            },
    ...
    (以下省略)

OCI CLIが正常に動作し、認証が成功したことが確認できれば準備完了です。



***************************************************
DBユーザーを作成する
***************************************************

インスタンス・プリンシパルをDatabase側で認証するための専用のDBユーザーを作成します。

このDBユーザーは、インスタンスのOCIDにマッピングされます。

.. code-block:: sql

    -- インスタンスOCIDに紐づくグローバルユーザーを作成
    SQL> create user DBUSER_COMPUTE identified globally as 'IAM_PRINCIPAL_OCID=ocid1.instance.oc1.ap-sydney-1.yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy';

    -- 接続するための権限を付与
    SQL> grant create session to USER_COMPUTE;



***************************************************
トークンを使用してアクセスする
***************************************************

インスタンスプリンシパルを使ってdb-tokenを取得し、接続します。

DBトークンの取得
==========================

``--auth instance_principal`` オプションを指定して ``db-token get`` コマンドを実行します。

.. code-block:: bash
    
    $ oci iam db-token get --auth instance_principal
    Private key written at /home/ubuntu/.oci/db-token/oci_db_key.pem
    db-token written at: /home/ubuntu/.oci/db-token/token
    db-token is valid until 2025-11-08 22:16:17


.. dropdown:: DBトークンをデコードした例

    .. code-block:: json
        :caption: ヘッダー

        {
            "kid": "scoped_sk_db_token_syd_1713219551687",
            "alg": "RS256"
        }

    .. code-block:: json
        :caption: ペイロード

        {
            "sub": "ocid1.instance.oc1.ap-sydney-1.yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy",
            "opc-certtype": "instance",
            "iss": "authService.oracle.com",
            "fprint": "A2:82:C9:B0:F3:5B:B8:DF:22:57:0F:10:3D:3F:27:B0:0E:78:3C:B6",
            "ptype": "instance",
            "sess_exp": "Sat, 08 Nov 2025 18:56:17 UTC",
            "aud": "urn:oracle:db:ocid1.tenancy.oc1..xxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "opc-tag": "V3,ocid1.tenancy.oc1..xxxxxxxxxxxxxxxxxxxxxxxxxxxx,AAAAAgAAAAAAAMmB,AAAAAgAAAAAbhip6AACBaA==,AAAAAQAAAAAAlERs",
            "ttype": "scoped_access",
            "scope": "urn:oracle:db::id::*",
            "opc-instance": "ocid1.instance.oc1.ap-sydney-1.yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy",
            "exp": 1762607777,
            "opc-compartment": "ocid1.compartment.oc1..zzzzzzzzzzzzzzzzzzzzzzzzzzzzzz",
            "iat": 1762606577,
            "jti": "68aa4a1d-65c2-4e6c-9c12-2650d83abe60",
            "tenant": "ocid1.tenancy.oc1..xxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "jwk": "{\"kid\":\"ocid1.tenancy.oc1..xxxxxxxxxxxxxxxxxxxxxxxxxxxx\",\"n\":\"rAU48ZSgchpnl-eXFyKQUF8bq5kGHtqx7LPWgHn_kWUh6rRWHkHvIf0--KD45hM_Yvi8L4edU7W_X7-qaYno2mWo4RBCx51wfo2EChOfktcZjJdK385g6xG6dclCQVT4IjUg1C6LmjHCCsKMhD2G9Q1sagJTipYZfbMSgT5IjtaM4kCwEdMLq6azzJ22ku8UqSVOZdrEVjYGVB-XIxr4xqjPMzvFo-DJLQrqnmKAGuf2HMbyxkCajiYBgAb1uYREXbtHuuS4CetirevBR5vIFWKYIYU3sUmZnA59-opYJuBfnpa-3eTmMdUD_fmCpMSAusYz-zR-vWKNSxM1qZjxww\",\"e\":\"AQAB\",\"kty\":\"RSA\",\"alg\":\"RS256\",\"use\":\"sig\"}",
            "opc-tenant": "ocid1.tenancy.oc1..xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        }


``tnsnames.ora`` の設定を利用し、取得したトークンを使用して接続します。

.. code-block:: sql
    
    $ sql /nolog

    SQL> connect /@db-token
    Connected.

    SQL> show user
    USER is "DBUSER_COMPUTE"

Databaseクライアント（コンピュートインスタンス）にAPIキーやパスワードといった静的な資格証明を持たせることなく、インスタンス・プリンシパル経由で取得したDBトークンを用いて、マッピングした専用DBユーザー(``DBUSER_COMPUTE``)としてログインできることが確認できました。

これで、DBトークンを利用したOracle Databaseへのアクセスのチュートリアルは終了です。