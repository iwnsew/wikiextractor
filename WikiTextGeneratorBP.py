#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs
import re
import sys
import unicodedata

argvs = sys.argv
if len(argvs) != 3 and len(argvs) != 4:
  sys.stderr.write('usage:\n')
  sys.stderr.write('python WikiTextGenerator.py [input] [output] [isword(1 or else)]\n')
  sys.exit()
wiki = argvs[1]
out = argvs[2]
isword = 0
if len(argvs) == 4 and argvs[3] == '1':
  isword = 1
isenglish = 0
if wiki.find('enwiki') != -1:
  import inflection
  isenglish = 1
  sys.stderr.write('Input is English.\n')

titletoid = {}
titletortitle = {}
fw = codecs.open(wiki, 'r', 'utf-8')
for line in fw:
  if len(line) > 7 and line[0:8] == '<doc id=':
    ts = line.split('"')
    title = ts[5].replace('&lt;', '<')
    title = title.replace('&gt;', '>')
    title = title.replace('&amp;', '&')
    title = title.replace('&quot;', '"')
    if title.find('Category:', 0, 9) != -1:
      continue
    if not len(ts) > 7:
      titletoid[title.lower()] = ts[1]
      print title.encode('utf-8') + ' -> ' + ts[1].encode('utf-8')
    else:
      titletortitle[title.lower()] = ts[7]
      print title.encode('utf-8') + ' -> ' + ts[7].encode('utf-8') + ' [redirect]'

fw.close()

fw = codecs.open(wiki, 'r', 'utf-8')
ft = codecs.open(out + '/text', 'w', 'utf-8')
ftm = codecs.open(out + '/term', 'w', 'utf-8')
fp = codecs.open(out + '/page', 'w', 'utf-8')
fbp = codecs.open(out + '/basepage', 'w', 'utf-8')
fbt = codecs.open(out + '/bonus-title', 'w', 'utf-8')
fbl = codecs.open(out + '/bonus-link', 'w', 'utf-8')
fl = codecs.open(out + '/link', 'w', 'utf-8')

pid = ''
page = ''
text = ''
redirect = ''
links = {}
linkstopages = {}
categories = set([])
r = re.compile("[ \t\n\v\f\r`~\\-!@#\\$%\\^&\\*\\(\\)_=\\+\\|\\[;\\]\\{\\},\\.\\/\\?<>:'’‘\\\\\"]+")
reglink = re.compile('<a href="(.+?)">(.+?)</a>')
for line in fw:
  if len(line) > 7 and line[0:8] == '<doc id=':
    ts = line.split('"')
    pid = ts[1]
    page = ts[5].replace('&lt;', '<')
    page = page.replace('&gt;', '>')
    page = page.replace('&amp;', '&')
    page = page.replace('&quot;', '"')
    npage = unicodedata.normalize('NFKC', page)
    #npage = re.sub(r'[_ ]\(.*?\)$', '', npage)
    npage = npage.lower()
    if isword == 1:
      npages = r.split(npage)
      npage = ' '.join(npages)
      if len(npage) > 0 and npage[0] == ' ':
        if len(npage) > 1:
          npage = npage[1:]
        else:
          npage = ''
    if len(ts) > 7:
      redirect = ts[7]
      if len(npage) > 0 and titletoid.has_key(redirect.lower()):
        fbt.write(npage + '\t' + titletoid[redirect.lower()] + '\n')
        ftm.write(npage + '\n')
    else:
      redirect = ''
      if len(npage) > 0:
        fbt.write(npage + '\t' + pid + '\n')
        ftm.write(npage + '\n')
  elif len(line) > 4 and line[0:5] == '</doc':
    if page.find('Category:', 0, 9) != -1:
      continue
    if len(text) > 0:
      fp.write(pid + '\t' + page + '\t' + str(len(text)) + '\n')
      ft.write(u'\u0002' + pid + u'\u0003\n' + text)
    if len(links) > 0:
      for k, v in links.items():
        fbl.write(k + '\t' + pid + '\t' + str(v) + '\n')
      for k, v in linkstopages.items():
        fl.write(k + '\t' + pid + '\t' + str(v) + '\n')

    #explicit dimension reduction
    pagename = page.lower();
    if pagename in categories:
      fbp.write(pid + '\t' + page + '\t' + str(len(text)) + '\n')
    else:
      p = pagename.split(' ')
      if len(p) > 1 and p[len(p)-1].find('(') != -1:
        p.pop()
        pagename = ' '.join(p)
      if pagename in categories:
        fbp.write(pid + '\t' + page + '\t' + str(len(text)) + '\n')
      elif isenglish == 1:
        p[len(p)-1] = inflection.pluralize(p[len(p)-1])
        pagename = ' '.join(p)
        if pagename in categories:
          fbp.write(pid + '\t' + page + '\t' + str(len(text)) + '\n')

    links.clear()
    linkstopages.clear()
    categories.clear()
    text = ''
    print page.encode('utf-8') + ' done!'
  elif redirect == '' and page.find('Category:', 0, 9) == -1:
    matches = reglink.findall(line)
    for match in matches:
      if match[0][0] == ':':
        continue
      if match[0].find('Category:', 0, 9) != -1:
        categories.add(match[0][9:].lower())
        c = match[0][9:].lower().split(' ')
        if len(c) > 1 and c[len(c)-1].find('(') != -1:
          c.pop()
          categories.add(' '.join(c))
        continue
      anchortext = unicodedata.normalize('NFKC', match[1])
      toid = 0
      totitle = match[0]
      if '#' in totitle:
        ts = totitle.split('#')
        totitle = ts[0]
        #print totitle, "+", ts[1]

      if titletortitle.has_key(totitle.lower()):
        totitle = titletortitle[totitle.lower()]
      if titletoid.has_key(totitle.lower()):
        toid = titletoid[totitle.lower()]
      ltp = anchortext + '\t' + str(toid)
      if ltp not in linkstopages.keys():
        linkstopages[ltp] = 0
      linkstopages[ltp] += 1
      tset = set([])
      for link in match:
        term = re.sub(r'[_ ]\(.*?\)$', '', link)
        term = unicodedata.normalize('NFKC', term)
        term = term.lower()
        #if term.find('#') != -1:
        if '#' in term:
          ts = term.split('#')
          for t in ts:
            tset.add(t)
            #print t
        else:
          tset.add(term)
      for t in tset:
        if isword == 1:
          ts = r.split(t)
          t = ' '.join(ts)
          if len(t) > 0 and t[0] == ' ':
            if len(t) > 1:
              t = t[1:]
            else:
              t = ''
        if len(t) < 1:
          continue
        if t not in links.keys():
          links[t] = 0
        links[t] += 1
    if line.find('<a href="Category:', 0, 18) == -1:
      line = re.sub(r'</?a.*?>', '', line)
      text += unicodedata.normalize('NFKC', line)

fw.close()
ft.close()
ftm.close()
fp.close()
fbp.close()
fbt.close()
fbl.close()
fl.close()

