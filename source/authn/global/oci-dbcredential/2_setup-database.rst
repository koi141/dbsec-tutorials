############################################
2. Databaseのセットアップ
############################################

このセクションでは、Oracle Database (Autonomous Database)を OCI IAMと連携させるために必要な、Database側の設定を行います。
本手順を始める前に `前提条件（特にADBの準備とWalletのダウンロード） <./0_intro.rst>`__ が満たされていることを確認してください。

.. topic:: 実施内容

    + サンプルスキーマの作成
    + 外部認証の有効化
    + グローバルユーザーの作成
    + グローバルロールの作成


***************************************************
サンプルスキーマの作成
***************************************************

チュートリアルの動作確認用として、HRスキーマとその中にテーブルを作成します。（すでに存在する場合は省略可能です。）

まず、Walletを使用してログインします。

.. code-block:: bash

    sql -cloudconfig <ダウンロードしたWalletへのパス> admin/<Password>@<ConnectString>


.. code-block:: bash
    :caption: 実行例

    $ sql -cloudconfig ./adb-wallet/Wallet_UQG5XBZV5LIND8ZF.zip /nolog

    SQL> conn admin@uqg5xbzv5lind8zf_medium
    Password? (**********?) ******************
    Connected.
    
    SQL> sho user con_name
    USER is "ADMIN"
    CON_NAME 
    ------------------------------
    G884BFFDDED7D8C_UQG5XBZV5LIND8ZF


次に、HRスキーマとテーブルを作成します。

    
.. code-block:: sql
    
    create user HR quota unlimited on data;

    create table HR.DEPARTMENTS (
        DEPT_ID number primary key,
        DEPT_NAME varchar2(50) not null,
        LOCATION varchar2(50)
    );

    -- サンプルデータを挿入
    insert into hr.departments (dept_id, dept_name, location) values (10, 'Accounting', 'Tokyo');
    insert into hr.departments (dept_id, dept_name, location) values (20, 'Reserch', 'Osaka');
    insert into hr.departments (dept_id, dept_name, location) values (30, 'Sales', 'Nagoya');
    insert into hr.departments (dept_id, dept_name, location) values (40, 'HR', 'Fukuoka');

    commit;



***************************************************
外部認証の有効化
***************************************************

IAMユーザーによる接続を許可するために、Databaseの外部認証機能をOCI IAMと連携するように設定します。

有効化のためのコマンドは、DBプラットフォームによって異なりますので、詳細は公式ドキュメントを参照ください

- ADB-S：https://docs.oracle.com/en/cloud/paas/autonomous-database/serverless/adbsb/enable-iam-authentication.html
- 非ADB：https://docs.oracle.com/cd/F19136_01/dbseg/authenticating-and-authorizing-iam-users-oracle-dbaas-databases.html#GUID-4149CF38-FE2E-4682-806E-8100CB7A9835

Autonomous Database (ADB) の場合、 ``DBMS_CLOUD_ADMIN`` パッケージを使用してOCI IAM 認証を有効化します。

.. code-block:: sql
    
    BEGIN
        DBMS_CLOUD_ADMIN.ENABLE_EXTERNAL_AUTHENTICATION( 
            type => 'OCI_IAM' );
    END;
    /

.. note::

    非ADBの場合は、 ``IDENTITY_PROVIDER_TYPE`` パラメータを設定します。

    .. code-block::

        ALTER SYSTEM SET IDENTITY_PROVIDER_TYPE=OCI_IAM SCOPE=BOTH;


設定が正しく反映されたか、状態を確認します。

.. code-block:: sql
    
    SELECT NAME, VALUE FROM V$PARAMETER WHERE NAME='identity_provider_type';

    -- または以下のコマンドでも可
    SHOW PARAMETER identity_provider_type;

.. code-block:: sql
    :caption: 実行例

    SQL> select name, value from v$parameter where name='identity_provider_type';

    NAME                   VALUE   
    ______________________ _______ 
    identity_provider_type OCI_IAM 



***************************************************
グローバルユーザーの作成
***************************************************

OCI IAMユーザーがDatabaseに接続する際のマッピング先となるグローバルユーザーを作成します。

| 本手順では、IAMのグループ (``domain-db/iamgroup-connect``) に属するすべてのユーザーが、Database上では単一のユーザー ``DBUSER_IAM`` として接続するように設定します。
| そのため、作成するグローバルユーザーは以下の１ユーザーのみとします。

- ``DBUSER_IAM``

管理者権限を持つユーザーでDBに接続し、グローバルユーザーを作成します。

.. code-block:: sql
    
    SQL> create user DBUSER_IAM identified globally as 'IAM_GROUP_NAME=domain-db/iamgroup-connect';
    User DBUSER_IAM created.

.. note::

    | Identity Domainを別に作成している場合、 ``<ドメイン名>/<グループ名>`` で指定することに注意してください。
    | また、Defaultドメインの場合このドメイン名は省略できますが、その場合でもできるだけ記述するようにしておきます。

これで、 ``iamgroup-connect`` グループに属するユーザーは、DBでは ``DBUSER_IAM`` ユーザーとして扱われることになります。
また、接続するための権限を ``DBUSER_IAM`` ユーザー自体に直接付与しておきます。

.. code-block:: sql

    SQL> grant create session to DBUSER_IAM;



***************************************************
グローバルロールの作成
***************************************************

グローバルユーザーと同様にグローバルロールも作成します。作成するロールは次の２つです。

- ``GLROLE_HR_ADMIN`` （iamgroup-hr-admin グループと対応付け。admin用の権限を与える）
- ``GLROLE_HR_DEV`` （iamgroup-hr-dev グループと対応付け。dev用の権限を与える）


``GLROLE_HR_ADMIN`` ロールには、HRスキーマのすべての管理権限を付与します。

.. code-block:: sql

    SQL> create role GLROLE_HR_ADMIN identified globally as 'IAM_GROUP_NAME=domain-db/iamgroup-hr-admin';

    Role GLROLE_HR_ADMIN created.

    SQL> grant all privileges on schema hr to GLROLE_HR_ADMIN;

    Grant succeeded.

``GLROLE_HR_DEV`` ロールへは参照権限のみ付与します。

.. code-block:: sql

    SQL> create role GLROLE_HR_DEV identified globally as 'IAM_GROUP_NAME=domain-db/iamgroup-hr-dev';

    Role GLROLE_HR_DEV created.

    SQL> grant select on hr.departments to GLROLE_HR_DEV;

    Grant succeeded.


次のセクションでは、実際にDBパスワードを使ってログインする手順に進みます。