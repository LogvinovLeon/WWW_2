# WWW_2
WWW Lab second project

How to play with it?

git clone https://github.com/LogvinovLeon/WWW_2.git
cd WWW_2
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
In the case of problems with installing lxml:
Fast fix for debian-based systems: apt-get install libxml2-dev libxslt-dev
Or otherwise: http://lxml.de/installation.html
./manage.py syncdb && ./manage.py crawl | tee log.txt

It will start crawling (takes a lot of time), but you can already start using the app.
To do it, open another terminal and paste:
./manage.py runserver

It'll work, but database writes will be way too slow.
You can stop crawlers and see, that after that it will be as fast as FFT.
