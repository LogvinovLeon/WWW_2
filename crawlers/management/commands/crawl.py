# coding=utf-8
import urllib
from lxml import html

from django.core.management import BaseCommand

from crawlers.models import Voivodeship, Powiat, Gmina, Constituency


class Etree(html.HtmlElement):
    def xpath_str(self, path, *args, **kwargs):
        element = super(Etree, self).xpath(path, *args, **kwargs)[0]
        if hasattr(element, "text_content"):
            return element.text_content()
        return element


class Command(BaseCommand):
    INIT_URL = "http://prezydent2010.pkw.gov.pl/PZT/PL/WYN/W/"

    def __init__(self):
        super(Command, self).__init__()

    def handle(self, *args, **options):
        self.crawl_voivodeships(self.INIT_URL + "index.htm")

    def crawl_voivodeships(self, url):
        entries = map(lambda e: Etree(e), self.fetch_url(url).xpath("//*[@id='s0']/tbody[1]/tr"))
        for entry in entries:
            voivodeship = Voivodeship(name=entry.xpath_str("//td[2]/a/text()"),
                                      url=self.INIT_URL + entry.xpath_str("//td[2]/a/@href"))
            voivodeship.save()
            print voivodeship
            self.crawl_powiats(voivodeship)

    def crawl_powiats(self, parent):
        entries = map(lambda e: Etree(e), self.fetch_url(parent.url).xpath("//*[@id='s0']/tbody[1]/tr"))
        for entry in entries:
            powiat = Powiat(name=entry.xpath_str("//td[2]/a/text()"),
                            url=self.INIT_URL + entry.xpath_str("//td[2]/a/@href"),
                            voivodeship=parent)
            powiat.save()
            print powiat
            if powiat.name[-2:] != u"m." and powiat.name != u"Statki - Gdańsk":
                self.crawl_gminas(powiat)
            else:
                gmina = Gmina(name=powiat.name, url=powiat.url, powiat=powiat)
                gmina.save()
                print gmina
                self.crawl_constituencies(gmina)

    def crawl_gminas(self, parent):
        if parent.name == "Zagranica":
            entries = map(lambda e: Etree(e),
                          self.fetch_url(parent.url).xpath("//*[@id='s0']/tbody[1]/tr"))
            last_gmina = None
            for entry in reversed(entries):
                if u"Σ" in entry.xpath_str("//td[2]"):
                    last_gmina = Gmina(name=entry.xpath_str("//td[2]/text()")[2:],
                                       url=None,
                                       powiat=parent)
                    last_gmina.save()
                    print last_gmina
                else:
                    constituency = Constituency(name=entry.xpath_str("//td[2]/a/text()"),
                                                url=self.INIT_URL + entry.xpath_str("//td[2]/a/@href"),
                                                gmina=last_gmina)
                    constituency.save()
                    print constituency
            return
        entries = map(lambda e: Etree(e), self.fetch_url(parent.url).xpath("//*[@id='s0']/tbody[1]/tr"))
        for entry in entries:
            gmina = Gmina(name=entry.xpath_str("//td[2]/a/text()"),
                          url=self.INIT_URL + entry.xpath_str("//td[2]/a/@href"),
                          powiat=parent)
            gmina.save()
            print gmina
            self.crawl_constituencies(gmina)

    def crawl_constituencies(self, parent):
        entries = map(lambda e: Etree(e), self.fetch_url(parent.url).xpath("//*[@id='s0']/tbody[1]/tr"))
        constituencies = []
        for entry in entries:
            constituency = Constituency(name=entry.xpath_str("//td[2]/a/text()"),
                                        url=self.INIT_URL + entry.xpath_str("//td[2]/a/@href"),
                                        gmina=parent)
            constituencies.append(constituency)
            print constituency
        Constituency.objects.bulk_create(constituencies)

    @staticmethod
    def fetch_url(url):
        return Etree(html.fromstring(urllib.urlopen(url).read()))