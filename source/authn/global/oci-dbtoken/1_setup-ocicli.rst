############################################
1. セットアップ
############################################

このセクションでは、OCI IAMトークンを取得し、Databaseへ接続するために必要な OCI（クラウド側）と Database 側の環境設定を行います。

DBトークンを取得するには、通常OCI CLIまたはOCI SDK（あるいはネイティブAPI）を使用します。本チュートリアルでは、OCI CLIを使用してトークンを取得します

このセクションで実施する内容は以下の通りです。

.. topic:: 実施内容

    + Identity Domain および IAM ユーザー/グループの準備 
    + DBユーザーの作成
    + IAMポリシーの作成
    + OCI CLIの準備



******************************************************
Identity Domain および IAM ユーザー/グループの準備
******************************************************

| Identity Domain を準備し、そのドメイン内にトークンを発行する主体（ユーザーとグループ）を準備します。
| Default ドメインの使用も可能ですが、データベースアクセスに関する管理を分離したい場合は、専用の Identity Domain を作成することを推奨します。

本手順では、DBトークンを発行する専用の IAMユーザーを用意し、使用するトークンによってDatabaseでの権限が変化することを確認します。

手順としては、 `1. Identity Domain のセットアップ <../oci-dbcredential/1_setup-identityDomain.html>`__ を参照し、以下に該当する内容を行います。

- Identity Domain の作成
- IAMユーザーの作成
- IAMグループの作成



***************************************************
DBユーザーの作成
***************************************************

Database側でも、OCI IAMユーザーと連携するための設定およびユーザーを作成します。

こちらも、手順としては `2. Databaseのセットアップ <../oci-dbcredential/2_setup-database.html>`__ を参照し、以下の内容すべてを実施してください。

- サンプルスキーマの作成
- 外部認証の有効化
- グローバルユーザーの作成
- グローバルロールの作成



***************************************************
IAMポリシーの作成
***************************************************

| DBトークンを発行したユーザーが、対象の Autonomous Database に接続できるよう、OCIのIAMポリシーを設定します。
| このポリシーにより、特定の IAM グループに属するユーザーが、テナンシ内の Autonomous Database リソースファミリーを利用できるようになります。
| OCIコンソールの左上のメニューより、[アイデンティティとセキュリティ] → [ポリシー] と遷移。次の IAM ポリシーを追加します。

.. code-block::
    :caption: 追加するIAMポリシー

    Allow group '<IdentityDomain名>'/'<グループ名>' to use autonomous-database-family in tenancy

下の画面ショットの例では ``iamgroup-connect`` グループを作成し、APIキーを登録したユーザーをこのグループに所属させています。

.. figure:: ../_img/domain-policy-02.png



***************************************************
OCI CLIの準備
***************************************************

DBトークンを取得するために使用する OCI CLI をセットアップします。


OCI CLI のインストール
=============================

以下リンクを参考に、OCI CLIをインストールします。

- `OCIチュートリアル「コマンドライン(CLI)でOCIを操作する」 <https://oracle-japan.github.io/ocitutorials/intermediates/using-cli/>`__
- `OCI CLI クイックスタート - OCIドキュメント <https://docs.oracle.com/ja-jp/iaas/Content/API/SDKDocs/cliinstall.htm>`__`


APIキーの準備と設定
=============================

OCI CLIをダウンロードしたら、OCIに接続するためのクレデンシャルが必要です。
この手順では CLI の認証に APIキーを使用しますので、APIキーを準備します。

OCIコンソールのユーザー詳細画面の [APIキー] タブより、「APIキーの追加」を追加します。

.. figure:: ../_img/domain-user-apikey-01.png

「追加」を選択したら、[構成ファイルのプレビュー] として、OCI CLIの設定ファイル(``$HOME/.oci/config``)に記述するための設定文字列が表示されます。これをコピーします。

.. figure:: ../_img/domain-user-apikey-02.png

.. code-block::
    :caption: 例

    [DEFAULT]
    user=ocid1.user.oc1..aaaaaaaaxxxxxxxxxxxxxxxxxxxxxxx
    fingerprint=11:01:83:61:d6:fc:09:c3:f6:7b:8b:8d:d4:6b:1b:71
    tenancy=ocid1.tenancy.oc1..aaaaaaaayyyyyyyyyyyyyyyyyyyyyyyyyyyy
    region=ap-tokyo-1
    key_file=<path to your private keyfile> # TODO


コピーした設定文字列を ``$HOME/.oci/config`` に追記します。この際、 ``key_file`` のパスを、APIキーの秘密鍵が配置されている実際のパスに書き換えてください。

このAPIキーの登録を、IAMユーザー「iamuser-hr-admin-01」「iamuser-hr-dev-01」でそれぞれおこないます。
この際、使用するユーザーのプロファイルを使い分けられるよう、 ``[DEFAULT]`` ではなく、 ``[iamuser-hr-admin-01]`` と ``iamuser-hr-dev-01`` で作成しておくといいでしょう。

.. code-block::
    :caption: 例

    [iamuser-hr-admin-01]
    user=ocid1.user.oc1..aaaaaaaaxxxxxxxxxxxxxxxxxxxxxxx
    fingerprint=xx:xx...

    ...
    [iamuser-hr-dev-01]
    user=ocid1.user.oc1..aaaaaaaaxxxxxxxxxxxxxxxxxxxxxxx
    fingerprint=yy:yy...


接続確認
=============================

cliが問題なく実行できることを確認します。OCI CLIの設定ファイルでプロファイルを指定している場合は ``--profile`` オプションを使用します。

.. code-block:: bash

    $ oci iam region list

    or 

    $ oci iam region list --profile iamuser-hr-admin-01
    $ oci iam region list --profile iamuser-hr-dev-01


.. dropdown:: 実行例

    .. code-block:: bash

        $ oci iam region list --profile iamuser-hr-admin-01
        {
            "data": [
                {
                "key": "AMS",
                "name": "eu-amsterdam-1"
                },
                {
                "key": "ARN",
                "name": "eu-stockholm-1"
        ...
        （以下省略）


次のステップでは、DBトークンを取得するしDBに接続する手順に進みます。

