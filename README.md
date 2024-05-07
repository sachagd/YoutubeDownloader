YoutubeDownloader is a firefox extension that allows anybody to donwload youtube video in any chosen format

Before utilising it you need to download few dependencies. To do that, execute init.bat in administrator mode.
List of things done by init.bat : 
  - Installing pip if it's not already the case
  - Installing python libraries : Tkinter, Beautifulsoup, requests and pytube
  - Installing ffmpeg if it's not already the case and adding the file path to the PATH environment variable
  - Adding a registery key

To access the parameters of the extension, open a new firefox tab, tap "about:addons", click on the extension and finally on options

Error you might encounter that aren't my fault : 

\_\_init\_\_: could not find match for ^\w+\W -> in the file cypher.py of the pytube module, replace the line 30 "var_regex = re.compile(r"^\w+\W")" by "var_regex = re.compile(r"^\$*\w+\W")"

source : https://stackoverflow.com/questions/70776558/pytube-exceptions-regexmatcherror-init-could-not-find-match-for-w-w
