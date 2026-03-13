---
title: Entra ID トークンによる接続
description: Microsoft Entra ID を使用した Database アクセス
sidebar:
  label: 概要
  order: 0
---

ここでは、Microsoft Entra ID が発行するアクセストークンを利用して Oracle Database に接続する手順を紹介します。

従来のデータベース認証では、ユーザー名とパスワードを Database 側で管理する必要がありました。  
一方、Entra ID と連携することで、認証を外部の ID プロバイダに統合でき、既存のユーザーやアプリケーションの認証基盤を活用したアクセス制御が可能になります。

本チュートリアルでは、Entra ID 側でのアプリケーション設定、Oracle Database 側での ID プロバイダ構成、Entra ID ユーザーやアプリロールに対応する Database ユーザーの作成、さらに実際にアクセストークンを取得して SQLcl から接続するまでの流れを順に確認します。

また、ユーザーのサインインによる委任されたアクセス許可だけでなく、クライアントクレデンシャル フローを利用したアプリケーション認証についても扱います。これにより、対話的なログインを伴う接続と、バックグラウンド処理やサーバー間連携のような非対話型の接続の両方を試すことができます。

Entra ID を利用したトークン認証を構成することで、パスワード管理の負担を軽減しつつ、より一元化された認証・認可モデルで Oracle Database へ接続できるようになります。

1. [Entra ID の設定](/dbsec-tutorials/authentication/entraid-dbtoken/tutorial/1-setup-entraid)
2. [Databaseの設定](/dbsec-tutorials/authentication/entraid-dbtoken/tutorial/2-setup-database)
3. [ログインを試す](/dbsec-tutorials/authentication/entraid-dbtoken/tutorial/3-login-entraid)

