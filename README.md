# wikiextractor

Wikipediaのダンプデータからページやリンクなどの情報をアレするスクリプト。  
python2.7系で動く。動くぞ。2.6系はダメだぞ。他は知らん。

Powered by Wikipedia Extractor  
<http://medialab.di.unipi.it/wiki/Wikipedia_Extractor>

## 使い方

1. wikiextractor/dumpディレクトリにWikipediaのダンプデータを置く。  
ダンプデータは「jawiki-20141122-pages-articles.xml.bz2」とかいう形式だ。  
ダンプデータ: <https://dumps.wikimedia.org/jawiki>
2. build.shを実行。引数の指定の仕方は以下のとおり。  
`./build.sh jawiki-20141122 [0 or 1]`  
(1はスペース区切りありの言語、0は区切りなしの言語)

## 出力ファイル

* page: 各行ごとに「ページID、ページタイトル、ページの文字数」
* basepage（英語のみ）: pageのうち、同名のカテゴリを持つもの
* link: 各行ごとに「アンカーテキスト（正規化）、リンク先ページID、リンク元ページID、頻度」
* term: 語句の一覧（正規化、ページタイトルとアンカーテキストから抽出）
* text: ページのテキストをつなげたファイル（テキスト部分は正規化）
* bonus-title: 各行ごとに「ページタイトル（正規化）、ページID」、ESA用
* bonus-link: 各行ごとに「アンカーテキスト（正規化）、リンク元ページID、頻度」、ESA用

なお、正規化とは、ユニコード正規化処理（NFKC）を行っていることを指す。

## Tips

英語のダンプデータとかだとサイズが大きいので

## License

GNU General Public License, version 3
