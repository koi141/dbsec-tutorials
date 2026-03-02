---
title: ネットワーク暗号化
sidebar:
  label: 概要
  order: 0
---


Oracle Database には、クライアント〜DB間の通信を暗号化する仕組みとして、大きく次の2系統があります。

- ネイティブ・ネットワーク暗号化（NNE: Native Network Encryption）
- TLS（TCPS）


このチュートリアルでは ネイティブ・ネットワーク暗号化（NNE）とTLSのセットアップをそれぞれ扱います。
NNEは Oracle Netの機能で、sqlnet.ora の設定により、通信内容の暗号化と改ざん検出を提供します。簡単にセットアップできる点が