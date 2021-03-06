# wikiextractor

Wikipediaのダンプデータからページやリンクなどの情報をアレするスクリプト。  
python2.7系で動く。動くぞ。2.6系はダメだぞ。他は知らん。

This script partly consists of Wikipedia Extractor.  
<http://medialab.di.unipi.it/wiki/Wikipedia_Extractor>

## 使い方

1. dumpディレクトリにWikipediaのダンプデータを置く。  
ダンプデータは「jawiki-20141122-pages-articles.xml.bz2」とかいう形式だ。  
ダンプデータ: <https://dumps.wikimedia.org/jawiki>
2. build.shを実行。引数の指定の仕方は以下のとおり。  
`./build.sh jawiki-20141122 [0 or 1]`  
(1はスペース区切りありの言語、0は区切りなしの言語)

## 出力ファイル

text/以下に生成

* *page*: 各行ごとに「ページID、ページタイトル、ページの文字数」
* *link*: 各行ごとに「アンカーテキスト（正規化）、リンク先ページID、リンク元ページID、頻度」（リンク先ページIDはリダイレクト処理済）
* *term*: 語句の一覧（正規化、小文字、ページタイトルを列挙したもの）
* *text*: ページのテキストをつなげたファイル（正規化、区切り文字は「\u0002ページID\u0003」としている）
* *bonus-title*: 各行ごとに「ページタイトル（正規化、小文字）、ページID」、ESA用
* *bonus-link*: 各行ごとに「アンカーテキスト（正規化、小文字）、リンク元ページID、頻度」、ESA用

ここで正規化とは、ユニコード正規化処理（NFKC）を行っていることを指す。

ちなみに中間ファイルとして、ページ間リンクとカテゴリリンクを残したバージョンのtextもdoc/以下に生成される。

## カテゴリ同名ページ抽出（英語、日本語のみ対応）

build.shのかわりにbuildBP.shを使うと同名のカテゴリを持つページも抽出できる。

* *basepage*: pageのうち、同名のカテゴリを持つもの

括弧による表記揺れ（＋英語の場合は複数形による表記揺れ）処理済。  
なお、英語の複数形の処理には inflection (`pip install inflection`) が必要。

## Tips

英語のダンプデータとかだとサイズが大きいので丸1日ぐらいかかるんじゃないでしょうか。  
日本語（jawiki-20141122）だと3時間ぐらいでした。  
(Intel(R) Xeon(R) CPU E3-1220 V2 @ 3.10GHz)

## License

GNU General Public License, version 3
