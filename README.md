# AWS IoT Greengrass Lambda
AWS IoT Greengrass Lambda を利用するサンプルです。
このサンプルでは、Raspberry Pi 上での AWS IoT Greengrass Lambda の動作、および、AWS IoT Core との連携を行います。

## Raspberry Pi のセットアップ

### Raspberry Pi 前提条件
以下の内容を利用します。

* Raspberry Pi ３ Model B+ / 4 Model B
* Python 3.7.x (Greengrass is not supported Python 3.8)

### Greengrass のセットアップ
以下の内容を参考に Raspberry Pi に Greengrass Core をセットアップします。

* Install Greengrass Core
    * https://docs.aws.amazon.com/ja_jp/greengrass/latest/developerguide/install-ggc.html
    * https://docs.aws.amazon.com/ja_jp/greengrass/latest/developerguide/gg-core.html

また、以下の内容を参考に Greengrass グループを作成します。

* Setup Greengrass Group
    * https://docs.aws.amazon.com/ja_jp/greengrass/latest/developerguide/quick-start.html


### Greengrass SDK のインストール
Raspberry Pi に Greengrass SDK をインストールします。
これは、Greengrass Core 上で Lambda を実行するのに必要なパッケージです。
`pip` を利用してインストール可能ですが、Raspberry Pi 上で `sudo` で実行してください。

```zsh
$ sudo pip install greengrasssdk
```

### デフォルトで利用するPythonモジュールのインストール
本サンプルで利用するPythonモジュールをインストールします。
ただ、通常、Raspberry Pi にインストールされているため、ここでは以下のモジュールが存在することを確認します。

* python3-gpiozero
* python3-psutil

```zsh
$ sudo apt search python3-gpiozero
python3-gpiozero/testing,now 1.5.1 all [インストール済み]

$ sudo apt search python3-psutil
python3-psutil/stable,now 5.5.1-1 armhf [インストール済み、自動]
```

## Serverless Framework によるAWSサービスのセットアップ

### Serverless Framework のインストール／アップデート
開発環境に、Serverless Framework をインストールします。
事前に npm がインストールされている必要があります。

```zsh
$ npm install -g serverless
$ npm update -g serverless
```

### 環境設定
本サンプルの設定について、自身の環境に応じて以下の設定を変更します。

- `services/customs/dev.yml`
    - クラウド側で動作する定義に利用されます。
```yaml
# provider
deployRegion: {your aws region}
profile: {your aws profile}
```

- `services/gg-functions/serverless.yml`
    - Raspberry Pi側で動作するLambdaの定義に利用されます。
```yaml
custom:
  # provider
  deployRegion: {your aws region}
  profile: {your aws profile}

  ・・・

  # serverless-plugin-greengrass
  # https://github.com/daaru00/serverless-plugin-greengrass
  greengrass:
    groupId: {greengrass group id (UUID)}
    autoDeploy: false
    deployTimeout: 30
    defaults:
      pinned: false        # Lambdaのライフサイクル -> false: on-demand / true: long-running
      memorySize: 16384    # Lambdaのメモリ制限 -> 16 MB expressed in KB
      timeout: 15          # Lambdaのタイムアウト
      encodingType: json   # 入力ペイロードのデータ型 -> json / binary
```

Raspberry Pi側（Greengrass上）で動作する Lamabda の定義は、以下のようになっています。
以下は、以下のような動作になります。

- 存続期間が長く無制限に稼働する
- サブスクリプションの定義
    - ソース：     Lambda
    - ターゲット： Cloud（AWS IoT Core）
    - トピック：   gg-example/#

```yaml
functions:
  pisys_monitor:
    handler: pisys_monitor_gg_handler.function_handler
    description: Monitor system resources on Greengrass
    greengrass:
      pinned: true
      accessSysfs: true
      subscriptions:
        - target: "cloud"
          subject: gg-example/#
```

### 関連リソースの構築
本サンプルでは、以下のリソースを利用します。

- DynamoDB

ここでは、Serverless Framework を利用して、DynamoDB のテーブルも構築します。

```zsh
$ cd resources
$ sls --config serverless-dynamodb.yml deploy
```

## デプロイ

### クラウド側のLambdaのデプロイ

先にクラウド側のデプロイを行っておきます。

```zsh
(開発環境)
$ cd services/pisys
$ sls deploy
```


### Raspberry Pi側のLambdaのデプロイ

Raspberry Pi側のLambdaのデプロイを行いますが、その前に Raspberry Pi 上で Greengrass Core を起動させてください。
Greengrass Core が起動していないと Lambda のデプロイが失敗します。

```bash
(Raspberry Pi)
$ sudo /greengrass/ggc/core/greengrassd start

Setting up greengrass daemon
Validating hardlink/softlink protection
Waiting for up to 1m10s for Daemon to start

Greengrass successfully started with PID: XXXX
```

次に、Lambdaのデプロイが失敗します。
`sls deploy` でAWSコンソールに Lambda 関数が登録され、`sls greengrass deploy` で Raspberry Pi 上の Greengrass Core に Lambda 関数がデプロイされます。

```zsh
(開発環境)
$ cd services/gg-functions
$ sls deploy
$ sls greengrass deploy
```
