import scrapy


class TorCheckerSpider(scrapy.Spider):
    name = "torchecker"

    def start_requests(self):
        urls = [
            'https://check.torproject.org/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = 'torChecker.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
