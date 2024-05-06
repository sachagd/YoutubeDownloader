YoutubeDownloader is a firefox extension that allows anybody to donwload youtube video in any chosen format

To access the parameters of the extension, open a new firefox tab, tap "about:addons", click on the extension and finally on options

Error you might encounter that aren't my fault : 

'__init__': could not find match for ^\w+\W -> in the file cypher.py of the pytube module, replace the line 30 "var_regex = re.compile(r"^\w+\W")" by "var_regex = re.compile(r"^\$*\w+\W")"

source : https://stackoverflow.com/questions/70776558/pytube-exceptions-regexmatcherror-init-could-not-find-match-for-w-w
