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


### Install default modules

```
sudo apt install python3-gpiozero

pip install greengrasssdk
pip install psutil
```
