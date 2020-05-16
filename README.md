# Python ILI9163

ILI9163 TFT液晶ディスプレイを制御するためのPythonライブラリです。カーネルモジュールをインストールすることなく、ディスプレイ上に簡単な描画を行うことができます。

ILI9163 ベースの 160x80 ピクセル TFT SPI ディスプレイ用に特別に設計されています。(具体的には[秋月電子通商](http://akizukidenshi.com/catalog/top.aspx)の[1.77インチ カラーグラフィックTFT LCD(１２８x(RGB)x160ドット) 評価キット](http://akizukidenshi.com/catalog/g/gK-14032/))。

以下の依存関係があることを確認してください。

````

python3-rpi.gpio python3-spidev python3-pip python3-imaging python3-numpy

````

# ライセンスと履歴

このライブラリは、Tony DiCola氏がAdafruit Industriesのために書いたコードを修正したもので、Clement Skau氏がST7735で動作するように修正したものです。

Pimoroniによって修正され、同社の160x80 SPI LCDブレークアウトをサポートし、他のST7735搭載ディスプレイをサポートするように一般化されています。

YoutechA320Uによって修正され、秋月電子通商の1.77インチ カラーグラフィックTFT LCD(１２８x(RGB)x160ドット) 評価キットのサポートが追加されました。

## 修正内容は以下の通りです。

* 初期化コマンド(.begin())がILI9163向けに変更されました。ST7735でも動作はしますが余白が発生する場合があります。

Pimoroni invests time and resources forking and modifying this open source code, please support Pimoroni and open-source software by purchasing products from us, too!

Adafruit invests time and resources providing this open source code, please support Adafruit and open-source hardware by purchasing products from Adafruit!

Modified from 'Modified from 'Adafruit Python ILI9341' written by Tony DiCola for Adafruit Industries.' written by Clement Skau.

MIT license, all text above must be included in any redistribution

