# usage:
# ./build.sh jawiki-20131005 [0 or 1]
# 1 for handling word type languages like English 

bzcat dump/$1-pages-articles.xml.bz2 | python WikiExtractor.py -l -s -o doc/$1-tmp
cat doc/$1-tmp/*/* > doc/$1
rm -rf doc/$1-tmp
mkdir text/$1
python WikiTextGeneratorBP.py doc/$1 text/$1 $2
