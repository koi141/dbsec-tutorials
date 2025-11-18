############################################
3. DBパスワードでログインする
############################################

これまでに、IAM側で2種類のIAMユーザー (iamuser-hr-admin-01 と iamuser-hr-dev-01) にDBパスワードを設定し、Database側でこれらのユーザーがマッピングされるグローバルユーザー (DBUSER_IAM) と、IAMグループに対応するグローバルロールを設定しました。

本セクションでは、各ユーザーに設定したDBパスワードを使って実際にDatabaseにアクセスし、IAMグループに基づいた権限分離が機能しているかを確認します。

.. topic:: 実施内容

    + AdminユーザーでDBに接続する
    + DevユーザーでDBに接続する



***************************************************
adminユーザーでDBに接続する
***************************************************

特別な準備は必要なく、 ``<ドメイン名>/<ユーザー名>`` の形式でユーザー名を指定し、DBにアクセスします。
「 ``/`` 」が含まれるため、SQLclやSQL*Plusを使用する場合は、ユーザー名をダブルクォート「 ``"`` 」で囲み、パスワードとして認識されないようにしてください。

まず、 ``iamuser-hr-admin-01`` ユーザーで接続してみます。

.. code-block:: sql

    $ sql -cloudconfig ./adb-wallet/Wallet_UQG5XBZV5LIND8ZF.zip /nolog

    SQL> conn "domain-db/iamuser-hr-admin-01"@uqg5xbzv5lind8zf_medium
    Password? (**********?) ******************
    Connected.

    -- ユーザー名を確認
    SQL> show user
    USER is "DBUSER_IAM"
    

無事、DBUSER_IAM ユーザーとしてアクセスすることができました。

所持している権限を確認し、試しに HR スキーマに TEST テーブルを作成してみます。

.. code-block:: sql

    -- 権限を確認
    SQL> select * from SESSION_PRIVS;

    PRIVILEGE      
    ______________ 
    CREATE SESSION 

    -- 所有するロールを確認
    SQL> select * from SESSION_ROLES;

    ROLE            
    _______________ 
    GLROLE_HR_ADMIN 

    -- グローバルロールは USER_ROLE_PRIVS には表示されない
    SQL> select * from user_role_privs;

    no rows selected

    -- HRスキーマに対して管理権限を持つため、tableを作成できる
    SQL> create table hr.test (
    2      id NUMBER
    3* );

    Table HR.TEST created.

    -- 作成したtableを削除する
    SQL> drop table hr.test;

    Table HR.TEST dropped.

Adminユーザーとして設定した権限が正しく適用されていることが確認できました。



***************************************************
devユーザーでDBに接続する
***************************************************

同様に、 ``iamuser-hr-dev-01`` でも接続してみます。

.. code-block:: sql

    $ sql -cloudconfig ./adb-wallet/Wallet_UQG5XBZV5LIND8ZF.zip /nolog

    SQL> conn "domain-db/iamuser-hr-dev-01"@uqg5xbzv5lind8zf_medium
    Password? (**********?) ******************
    Connected.
    
    -- ユーザー名を確認
    SQL> show user
    USER is "DBUSER_IAM"


接続先のDBユーザーはAdminの場合と同様 ``DBUSER_IAM`` です。異なる権限が適用されているかどうかを確認します。

.. code-block:: sql

    -- 権限を確認
    SQL> select * from SESSION_PRIVS;

    PRIVILEGE      
    ______________ 
    CREATE SESSION 

    -- 所有するロールを確認
    SQL> SELECT * FROM SESSION_ROLES;

    ROLE          
    _____________ 
    GLROLE_HR_DEV 

    -- 参照権限しかないため、table作成は失敗する
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
    *Cause:    A database operation was attempted without the required privilege(s).
    *Action:   Ask your database administrator or security administrator to grant you the required privilege(s).

Devユーザーとして設定した参照権限のみが適用され、IAMグループに基づいた権限分離が正常に機能していることが確認できました。

次のセクションでは、DBパスワードでログインしたユーザーの操作が、監査ログにどのように記録されるかを確認します。

