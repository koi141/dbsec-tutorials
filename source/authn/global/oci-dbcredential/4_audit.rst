############################################
4. 監査ログを見てみる
############################################

前セクションでは、2つの異なるIAMユーザー（iamuser-hr-admin-01 と iamuser-hr-dev-01）が、Database側では単一のグローバルユーザー（DBUSER_IAM）として扱われることを確認しました。

この設計では、「誰が操作したか」を後から追跡できるかが重要になります。
そこで、このセクションでは、Oracle Databaseの統合監査（Unified Auditing）を使用して、操作を行ったユーザーを特定できるかを確認します。

.. topic:: 実施内容

    + 統合監査の設定
    + 監査ログの確認



***************************************************
統合監査の設定
***************************************************

現在、統合監査が有効になっていること、および現在有効な監査ポリシーを確認します。


統合監査の事前確認
===================================================

まずは統合監査が有効化になっているかを確認します。何も操作していなければ、デフォルトで ``TRUE`` となっているはずです。

.. code-block:: sql

    SQL> select * from V$OPTION where PARAMETER = 'Unified Auditing';

    PARAMETER        VALUE CON_ID 
    ________________ _____ ______ 
    Unified Auditing TRUE       0 


現在有効な監査ポリシーを確認します。

.. code-block:: sql

    SQL> select POLICY_NAME, ENABLED_OPTION, ENTITY_NAME from AUDIT_UNIFIED_ENABLED_POLICIES;

    POLICY_NAME                    ENABLED_OPTION ENTITY_NAME      
    ______________________________ ______________ ________________ 
    ADB_ADMIN_AUDIT                EXCEPT USER    SYS              
    ADB_PARURL_ACCESS_AUDIT        BY USER        C##CLOUD$SERVICE 
    ADB_ADMIN_AUDIT                EXCEPT USER    C##CLOUD$SERVICE 
    ORA_LOGON_FAILURES             BY USER        ALL USERS        
    ADB_PARURL_PKG_ACCESS_AUDIT    BY USER        ALL USERS        
    ORA$DICTIONARY_SENS_COL_ACCESS BY USER        ALL USERS        
    ORA$DICTIONARY_SNET_RPC_ACCESS BY USER        ALL USERS        
    COMMON_USER_LOGONS             BY USER        SYS              
    COMMON_USER_LOGONS             BY USER        PUBLIC           
    COMMON_USER_LOGONS             BY USER        SYSBACKUP        

    10 rows selected. 


統合監査ポリシーの作成
===================================================

すべてSQLアクションを補足する監査ポリシーを作成します。

.. code-block:: sql

    SQL> CREATE AUDIT POLICY audit_all_actions ACTIONS ALL;

    Audit POLICY created.

作成したポリシーをターゲットユーザーである ``DBUSER_IAM`` に適用します。これで ``DBUSER_IAM`` ユーザーの行動を監査できるようになりました。

.. code-block:: sql

    SQL> audit policy audit_all_actions by DBUSER_IAM;

    Audit succeeded.

    -- DBUSER_IAM ユーザーに対して有効になっているかを確認する
    SQL> select POLICY_NAME, ENABLED_OPTION, ENTITY_NAME from AUDIT_UNIFIED_ENABLED_POLICIES;

    POLICY_NAME                    ENABLED_OPTION ENTITY_NAME      
    ______________________________ ______________ ________________ 
    ADB_ADMIN_AUDIT                EXCEPT USER    SYS              
    ADB_PARURL_ACCESS_AUDIT        BY USER        C##CLOUD$SERVICE 
    ADB_ADMIN_AUDIT                EXCEPT USER    C##CLOUD$SERVICE 
    AUDIT_ALL_ACTIONS              BY USER        DBUSER_IAM       
    ORA_LOGON_FAILURES             BY USER        ALL USERS        
    ADB_PARURL_PKG_ACCESS_AUDIT    BY USER        ALL USERS        
    ORA$DICTIONARY_SENS_COL_ACCESS BY USER        ALL USERS        
    ORA$DICTIONARY_SNET_RPC_ACCESS BY USER        ALL USERS        
    COMMON_USER_LOGONS             BY USER        SYS              
    COMMON_USER_LOGONS             BY USER        PUBLIC           
    COMMON_USER_LOGONS             BY USER        SYSBACKUP        



***************************************************
監査ログの確認
***************************************************

前セクションで実施した AdminユーザーやDevユーザーの操作（接続、テーブル作成など）を行った後、監査ログを取得します。

``UNIFIED_AUDIT_TRAIL`` ビューから、 ``DBUSER_IAM`` の操作ログを取得し、特に ``EXTERNAL_USERID`` の値に注目して確認します。

次のコマンドで直近の監査ログを20行取得します。

.. code-block:: sql

    select EVENT_TIMESTAMP_UTC, ACTION_NAME, DBUSERNAME, EXTERNAL_USERID, CLIENT_IDENTIFIER, USERHOST, OS_USERNAME, CLIENT_PROGRAM_NAME, SESSIONID, RETURN_CODE, SQL_TEXT 
        from UNIFIED_AUDIT_TRAIL 
        where DBUSERNAME = 'DBUSER_IAM'
        order by EVENT_TIMESTAMP_UTC desc
        fetch first 20 ROWS ONLY;

.. code-block:: sql
    :caption: 実行例

    SQL> select
    2      EVENT_TIMESTAMP_UTC,
    3      ACTION_NAME,
    4      DBUSERNAME,
    5      EXTERNAL_USERID,
    6      CLIENT_IDENTIFIER,
    7      USERHOST,
    8      OS_USERNAME,
    9      CLIENT_PROGRAM_NAME,
    10      SESSIONID,
    11      RETURN_CODE,
    12      SQL_TEXT
    13  from
    14      UNIFIED_AUDIT_TRAIL
    15  where
    16      DBUSERNAME = 'DBUSER_IAM'
    17  order by
    18      EVENT_TIMESTAMP_UTC desc
    19* fetch first 20 ROWS ONLY;

    EVENT_TIMESTAMP_UTC             ACTION_NAME DBUSERNAME EXTERNAL_USERID                                                              CLIENT_IDENTIFIER USERHOST OS_USERNAME CLIENT_PROGRAM_NAME SESSIONID            RETURN_CODE SQL_TEXT        
    _______________________________ ___________ __________ ____________________________________________________________________________ _________________ ________ ___________ ___________________ ____________________ ___________ ________________________________________________________________________________
    10-NOV-25 08.02.42.490882000 AM LOGOFF      DBUSER_IAM ocid1.user.oc1..aaaaaaaarojkl3cvp2yawyhip7to6txdbevd3jrzkgtubkr2wsicxxm2vgna                   edge-dev ubuntu      SQLcl               16620439162436382782           0                 
    10-NOV-25 08.02.21.408382000 AM EXECUTE     DBUSER_IAM ocid1.user.oc1..aaaaaaaarojkl3cvp2yawyhip7to6txdbevd3jrzkgtubkr2wsicxxm2vgna                   edge-dev ubuntu      SQLcl               16620439162436382782           0 DECLARE         
                                                                                                                                                                                                                                    CHECKONE VARCHAR2(1000):=NULL;
                                                                                                                                                                                                                                    BEGIN           
                                                                                                                                                                                                                                    BEGIN          
                                                                                                                                                                                                                                    CHECKONE:=substr(SYS_
    10-NOV-25 07.58.45.434648000 AM EXECUTE     DBUSER_IAM ocid1.user.oc1..aaaaaaaarojkl3cvp2yawyhip7to6txdbevd3jrzkgtubkr2wsicxxm2vgna                   edge-dev ubuntu      SQLcl               16620439162436382782           0 DECLARE         
                                                                                                                                                                                                                                    CHECKONE VARCHAR2(1000):=NULL;
                                                                                                                                                                                                                                    BEGIN           
                                                                                                                                                                                                                                    BEGIN          
                                                                                                                                                                                                                                    CHECKONE:=USER;
                                                                                                                                                                                                                                    EXC            
    10-NOV-25 07.58.41.378117000 AM SELECT      DBUSER_IAM ocid1.user.oc1..aaaaaaaarojkl3cvp2yawyhip7to6txdbevd3jrzkgtubkr2wsicxxm2vgna                   edge-dev ubuntu      SQLcl               16620439162436382782        2004 select INITCAP(TO_CHAR(last_login ,'DY MON DD YYYY HH24:MI:SS TZH:TZM')) from db
    10-NOV-25 07.58.41.377238000 AM SELECT      DBUSER_IAM ocid1.user.oc1..aaaaaaaarojkl3cvp2yawyhip7to6txdbevd3jrzkgtubkr2wsicxxm2vgna                   edge-dev ubuntu      SQLcl               16620439162436382782        2004 select INITCAP(TO_CHAR(last_login ,'DY MON DD YYYY HH24:MI:SS TZH:TZM')) from db
    10-NOV-25 07.58.41.376377000 AM SELECT      DBUSER_IAM ocid1.user.oc1..aaaaaaaarojkl3cvp2yawyhip7to6txdbevd3jrzkgtubkr2wsicxxm2vgna                   edge-dev ubuntu      SQLcl               16620439162436382782        2004 select INITCAP(TO_CHAR(last_login ,'DY MON DD YYYY HH24:MI:SS TZH:TZM')) from db
    10-NOV-25 07.58.41.375499000 AM SELECT      DBUSER_IAM ocid1.user.oc1..aaaaaaaarojkl3cvp2yawyhip7to6txdbevd3jrzkgtubkr2wsicxxm2vgna                   edge-dev ubuntu      SQLcl               16620439162436382782        2004 select INITCAP(TO_CHAR(last_login ,'DY MON DD YYYY HH24:MI:SS TZH:TZM')) from db
    10-NOV-25 07.58.41.374631000 AM SELECT      DBUSER_IAM ocid1.user.oc1..aaaaaaaarojkl3cvp2yawyhip7to6txdbevd3jrzkgtubkr2wsicxxm2vgna                   edge-dev ubuntu      SQLcl               16620439162436382782        2004 select INITCAP(TO_CHAR(last_login ,'DY MON DD YYYY HH24:MI:SS TZH:TZM')) from db
    10-NOV-25 07.58.41.373752000 AM SELECT      DBUSER_IAM ocid1.user.oc1..aaaaaaaarojkl3cvp2yawyhip7to6txdbevd3jrzkgtubkr2wsicxxm2vgna                   edge-dev ubuntu      SQLcl               16620439162436382782        2004 select INITCAP(TO_CHAR(last_login ,'DY MON DD YYYY HH24:MI:SS TZH:TZM')) from db
    10-NOV-25 07.58.41.372846000 AM SELECT      DBUSER_IAM ocid1.user.oc1..aaaaaaaarojkl3cvp2yawyhip7to6txdbevd3jrzkgtubkr2wsicxxm2vgna                   edge-dev ubuntu      SQLcl               16620439162436382782        2004 select INITCAP(TO_CHAR(last_login ,'DY MON DD YYYY HH24:MI:SS TZH:TZM')) from db
    10-NOV-25 07.58.41.371867000 AM SELECT      DBUSER_IAM ocid1.user.oc1..aaaaaaaarojkl3cvp2yawyhip7to6txdbevd3jrzkgtubkr2wsicxxm2vgna                   edge-dev ubuntu      SQLcl               16620439162436382782        2004 select INITCAP(TO_CHAR(last_login ,'DY MON DD YYYY HH24:MI:SS TZH:TZM')) from db
    10-NOV-25 07.58.41.363708000 AM SELECT      DBUSER_IAM ocid1.user.oc1..aaaaaaaarojkl3cvp2yawyhip7to6txdbevd3jrzkgtubkr2wsicxxm2vgna                   edge-dev ubuntu      SQLcl               16620439162436382782        2004 select INITCAP(TO_CHAR(last_login ,'DY MON DD YYYY HH24:MI:SS TZH:TZM')) from db
    10-NOV-25 07.58.41.362776000 AM SELECT      DBUSER_IAM ocid1.user.oc1..aaaaaaaarojkl3cvp2yawyhip7to6txdbevd3jrzkgtubkr2wsicxxm2vgna                   edge-dev ubuntu      SQLcl               16620439162436382782        2004 select INITCAP(TO_CHAR(last_login ,'DY MON DD YYYY HH24:MI:SS TZH:TZM')) from db
    10-NOV-25 07.58.41.361888000 AM SELECT      DBUSER_IAM ocid1.user.oc1..aaaaaaaarojkl3cvp2yawyhip7to6txdbevd3jrzkgtubkr2wsicxxm2vgna                   edge-dev ubuntu      SQLcl               16620439162436382782        2004 select INITCAP(TO_CHAR(last_login ,'DY MON DD YYYY HH24:MI:SS TZH:TZM')) from db
    10-NOV-25 07.58.41.361020000 AM SELECT      DBUSER_IAM ocid1.user.oc1..aaaaaaaarojkl3cvp2yawyhip7to6txdbevd3jrzkgtubkr2wsicxxm2vgna                   edge-dev ubuntu      SQLcl               16620439162436382782        2004 select INITCAP(TO_CHAR(last_login ,'DY MON DD YYYY HH24:MI:SS TZH:TZM')) from db
    10-NOV-25 07.58.41.360132000 AM SELECT      DBUSER_IAM ocid1.user.oc1..aaaaaaaarojkl3cvp2yawyhip7to6txdbevd3jrzkgtubkr2wsicxxm2vgna                   edge-dev ubuntu      SQLcl               16620439162436382782        2004 select INITCAP(TO_CHAR(last_login ,'DY MON DD YYYY HH24:MI:SS TZH:TZM')) from db
    10-NOV-25 07.58.41.359275000 AM SELECT      DBUSER_IAM ocid1.user.oc1..aaaaaaaarojkl3cvp2yawyhip7to6txdbevd3jrzkgtubkr2wsicxxm2vgna                   edge-dev ubuntu      SQLcl               16620439162436382782        2004 select INITCAP(TO_CHAR(last_login ,'DY MON DD YYYY HH24:MI:SS TZH:TZM')) from db
    10-NOV-25 07.58.41.358373000 AM SELECT      DBUSER_IAM ocid1.user.oc1..aaaaaaaarojkl3cvp2yawyhip7to6txdbevd3jrzkgtubkr2wsicxxm2vgna                   edge-dev ubuntu      SQLcl               16620439162436382782        2004 select INITCAP(TO_CHAR(last_login ,'DY MON DD YYYY HH24:MI:SS TZH:TZM')) from db
    10-NOV-25 07.58.41.357498000 AM SELECT      DBUSER_IAM ocid1.user.oc1..aaaaaaaarojkl3cvp2yawyhip7to6txdbevd3jrzkgtubkr2wsicxxm2vgna                   edge-dev ubuntu      SQLcl               16620439162436382782        2004 select INITCAP(TO_CHAR(last_login ,'DY MON DD YYYY HH24:MI:SS TZH:TZM')) from db
    10-NOV-25 07.58.41.356631000 AM SELECT      DBUSER_IAM ocid1.user.oc1..aaaaaaaarojkl3cvp2yawyhip7to6txdbevd3jrzkgtubkr2wsicxxm2vgna                   edge-dev ubuntu      SQLcl               16620439162436382782        2004 select INITCAP(TO_CHAR(last_login ,'DY MON DD YYYY HH24:MI:SS TZH:TZM')) from db

    20 rows selected.



このように、 ``EXTERNAL_USERID`` 列に使用したOCI IAMユーザーのOCIDが記録されるため、この情報を利用して、操作した人間を特定することができます。
したがって、グローバルユーザーとしてマッピングされた場合でも、Oracle Databaseの統合監査機能を使用することで、「誰が」その操作を行ったかを追跡することが可能です。

これで OCI IAM の DBパスワードを使用したアクセス方法についてのチュートリアル手順は終了です。