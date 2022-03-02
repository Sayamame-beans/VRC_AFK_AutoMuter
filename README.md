# VRC_AFK_AutoMuter
"VRChat"にて、AFK移行時に自動でミュートするOSCツールです。

## 開発環境と動作確認済み環境について

- Windows 10
- Python 3.9.2
  - python-osc 1.8.0

## 使い方
Releasesページ、またはBoothにてexeファイルを配布しています。
これを実行することで、VRChat標準の設定を基準に動作を開始します。
(IP:127.0.0.1, VRChat側受信ポート:9000, VRChat側送信ポート9001)

起動後は自動的に動作し、AFK移行時にミュートします。
あくまでAFK移行時にミュートするので、AFK移行後にミュートを外しても、自動でミュートされる事はありません。

注意点として、VRC起動後に本ツールを起動した場合、ミュートの初期状態が不明なため、誤ってミュートが外されてしまう場合があります。
この場合については、数秒後に自動的にミュートされるはずです。

なお、初回実行時にセキュリティの警告が出るかもしれません。信頼出来ないなと思った場合は使用しないことをお勧めします。
(信頼出来ないexeファイルは無闇に実行するべきではありませんので…)

## オプションについて
`-h`オプションを付けて実行すると、他のオプションについての説明が得られます。ここではその説明文を引用します。
```
usage: VRC_AFK_AutoMuter.exe [-h] [--tx_ip TX_IP] [--tx_port TX_PORT] [--rx_ip RX_IP] [--rx_port RX_PORT]

This is an OSC tool that automatically mutes when AFK in VRChat.

optional arguments:
  -h, --help         show this help message and exit
  --tx_ip TX_IP      Destination IP address. (Default: "127.0.0.1")
  --tx_port TX_PORT  Destination Port. (Default: 9000)
  --rx_ip RX_IP      Source IP address. (Default: "127.0.0.1")
  --rx_port RX_PORT  Source IP address. (Default: 9001)
```

## ライセンスについて
MITライセンスです。
大雑把に言うと、使用用途自由で、商用利用も可能、改造も可能。
ただし、改造の有無にかかわらず、再配布する場合はライセンスファイルの同梱と著作権表示(`Copyright (c) 2022 Sayamame-beans`)をしてください、という感じです。
