---
title: このサイトについて
description: サイトの目的・対象読者・扱うトピックと免責事項
---

## サイトについて

このサイトは、Oracle Database のセキュリティ機能に関するメモとチュートリアルをまとめたドキュメントサイトです。
環境構築から設定・検証手順・注意点まで、できるだけ手順ベースで整理しています。

## 対象読者

- Oracle Database のセキュリティ機能を学んでみたい方
- TDE・VPD・Database Vault などの機能を実際に動かしながら理解したい方
- OCI IAM 連携や MFA などのクラウドセキュリティ機能を試したい方

## 扱うトピック

| カテゴリ | 機能 |
|---|---|
| **環境セットアップ** | Oracle Database 26ai FREE のインストール、SQLcl、HR サンプルスキーマ |
| **認証** | OCI IAM DBパスワード / DBトークン、MS Entra ID トークン、ローカルユーザー MFA |
| **アクセス制御** | Database Vault、Oracle Label Security、Virtual Private Database、SQL Firewall |
| **暗号化** | TDE（透過的データ暗号化）、ネットワーク暗号化（NNE / TLS） |
| **データマスキング** | Data Redaction |

## 免責事項

- 内容は学習・検証用途を想定しています。コマンド例や設定例は再現しやすさを優先して簡略化している場合があります。
- 実運用に適用する際は、利用するバージョンや組織のセキュリティポリシーに合わせて十分に検討してください。
- 実行結果の一部は見やすさのため整形・省略しています。実際の出力と異なる場合があります。

## ソースコード

ドキュメントのソースは GitHub で管理しています。

> https://github.com/koi141/dbsec-tutorials
