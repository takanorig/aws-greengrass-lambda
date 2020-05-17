# aws-greengrass-lambda
Example Lambda functions for AWS Greengrass.

## Pre-conditions for Raspberry Pi

* Raspberry Pi 3 Model B+
* Python 3.7.x (Greengrass is not supported Python3.8)

### Setup Greengrass

* Install Greengrass Core
    * https://docs.aws.amazon.com/ja_jp/greengrass/latest/developerguide/install-ggc.html
    * https://docs.aws.amazon.com/ja_jp/greengrass/latest/developerguide/gg-core.html
* Setup Greengrass Group
    * https://docs.aws.amazon.com/ja_jp/greengrass/latest/developerguide/quick-start.html


### Install default modules in Raspberry Pi

Install `greengrasssdk` with `sudo`.

```
sudo pip install greengrasssdk
```


Check the required modules are installed.

* python3-gpiozero
* python3-psutil

```
$ sudo apt search python3-gpiozero
python3-gpiozero/testing,now 1.5.1 all [インストール済み]

$ sudo apt search python3-psutil
python3-psutil/stable,now 5.5.1-1 armhf [インストール済み、自動]
```

## Deploy to AWS with Serverless Framework

### Install or Update serverless

```
npm install -g serverless
npm update -g serverless
```

### Deploy lambda functions with serverless

You have to set up aws profile before deploy,
and the modify the `customs/dev.yml`.

```yaml
# provider
deployRegion: {your aws region}
profile: {your aws profile}
```

After setting up your profile, can deploy it.

```
$ cd functions
$ sls deploy
```

