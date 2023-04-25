# シリアルデータからAzure Event Hubsへ

このPythonスクリプトは、接続されたデバイスからシリアルデータを読み取り、Event Hub Producer Clientを使用して解析されたデータをAzure Event Hubsに送信します。

## 必要条件

- Python 3.6+
- `azure-eventhub` ライブラリ
- `pyserial` ライブラリ

## インストール

1. 必要なパッケージをインストールします。

```bash
pip install azure-eventhub pyserial
```

2. 次の環境変数を設定するか、`src/config.ini` ファイルを編集します。

- `AZURE_CONNECTION_STR`: Azure Event Hubsの名前空間の接続文字列。
- `AZURE_EVENTHUB_NAME`: Event Hub インスタンスの名前。

## スクリプトの実行

1. デバイスをシリアルポート（既定では `/dev/ttyACM0`）に接続します。
2. スクリプトを実行します：

```bash
python serial_to_eventhubs.py
```

## 動作の仕組み

スクリプトは以下の手順で動作します。

1. 指定されたデバイスとのシリアル接続を開きます。
2. シリアルデータを逐次的に読んで、「RECV::」で始まる行を探します。
3. 受信したデータを検証し、ホスト名、ビーコンアドレス、RSSIに分割します。
4. JSON形式のイベントデータとして解析したデータをAzure Event Hubsに送信します。

スクリプトは、終了シグナル（SIGINT, SIGTERM）を処理し、シリアル接続を閉じて正常に終了します。

## 貢献

改善やバグ修正に関する問題やプルリクエストを提出してください。


docker run -d --restart always  --device=/dev/ttyACM0:/dev/ttyACM0 pptdxsoliag/mmtr_scanner_receiver:0.0.2 