# Python ILI9163

RaspberryPiに装着したILI9163 TFT液晶ディスプレイを制御するためのPythonライブラリです。カーネルモジュールをインストールすることなく、ディスプレイ上に簡単な描画を行うことができます。

[秋月電子通商の1.77インチ カラーグラフィックTFT LCD(128x(RGB)x160ドット) 評価キット](http://akizukidenshi.com/catalog/g/gK-14032/)などILI9163 ベースの 160x80 ピクセル TFT SPI ディスプレイ用で使えます。

![SS](https://github.com/YoutechA320U/ili9163-python/blob/master/example.gif "example")

# インストール方法

まず以下のコマンドで必要なパッケージをインストールします

````

sudo apt-get install python3-rpi.gpio python3-spidev python3-pip python3-numpy

sudo pip3 install pillow

````

次に`ILI9163`フォルダを中身ごと`/usr/local/lib/python3.7/dist-packages/`などライブラリとして認識できる場所にコピーします。

使い方は`example`フォルダのサンプルを参考にしてください。

# 配線
※[1.77インチ カラーグラフィックTFT LCD(128x(RGB)x160ドット) 評価キット](http://akizukidenshi.com/catalog/g/gK-14032/)とRaspberryPiの場合

|液晶ピン番号|役割|RaspberryPiピン番号|
|:---|:--:|---:|
|1|NC||
|2|NC||
|3|NC||
|4|NC||
|5|A(バックライトLEDアノード)|※抵抗220Ω程度を挟んで液晶VCCへ|
|6|NC||
|7|NC||
|8|GND|6,9,14,20,25,30,34,39(GND)のどれか|
|9|VCC|1か17(3.3V)|
|10|SDA(MOSI)|19(GPIO10)|
|11|SCK(SCLK)|23(GPIO11)|
|12|A0(DC)|32(GPIO12)※サンプルの初期設定|
|13|RESET(RES)|22(GPIO25)※サンプルの初期設定|
|14|K(バックライトLEDカソード)|GNDへ|
|15|CS(CE)|24(GPIO8)|

# ライセンスと履歴

このライブラリは、Tony DiCola氏がAdafruit Industriesのために書いたコードを修正したもので、Clement Skau氏がST7735で動作するように修正したものです。

Pimoroniによって修正され、同社の160x80 SPI LCDブレークアウトをサポートし、他のST7735搭載ディスプレイをサポートするように一般化されています。

そこから更にYoutechA320Uによって修正され、ILI9163の動作が可能になりました。

## 修正内容

* 初期化コマンド(`begin()`)がILI9163向けに変更されました。ST7735でも動作はしますが余白が発生する場合があります。

Pimoroni invests time and resources forking and modifying this open source code, please support Pimoroni and open-source software by purchasing products from us, too!

Adafruit invests time and resources providing this open source code, please support Adafruit and open-source hardware by purchasing products from Adafruit!

Modified from 'Modified from 'Adafruit Python ILI9341' written by Tony DiCola for Adafruit Industries.' written by Clement Skau.

MIT license, all text above must be included in any redistribution

