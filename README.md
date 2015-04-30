# WWW_2 Lab second project
How to play with it?
```sh
git clone https://github.com/LogvinovLeon/WWW_2.git
cd WWW_2
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
```

In the case of problems with installing lxml:

Fast fix for debian-based systems: 
```sh
apt-get install libxml2-dev libxslt-dev
```
Or otherwise: [Instalation guide](http://lxml.de/installation.html)
```sh
./manage.py syncdb && ./manage.py crawl | tee log.txt
```
It will start crawling (takes a lot of time), but you can already start using the app. To do it, open another terminal and paste:
```sh
./manage.py runserver
```
It'll work, but database writes will be way too slow. You can stop crawlers and see, that after that it will be as fast as FFT.
