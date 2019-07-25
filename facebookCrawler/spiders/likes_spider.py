import scrapy

from utils.textCleaner import clean_html_text, remove_spaces
from utils.fileUtils import *
from utils.setup import *


class LikeSpider(scrapy.Spider):
    name = "likes_spider"
    start_urls = ['https://www.facebook.com/']
    #scrap_urls = ['https://mbasic.facebook.com/' + USERNAME + '?v=likes']
    #scrap_urls = ['https://mbasic.facebook.com/' + USER_ID + '?v=likes']

    def __init__(self, user_id=None, *args, **kwargs):
        super(LikeSpider, self).__init__(*args, **kwargs)
        self.scrap_urls = ['https://mbasic.facebook.com/' + user_id + '?v=likes']

    def parse(self, response):

        self.logger.info("\n\nLogging in.................\n")

        legacy_return = response.xpath('//*[@name="legacy_return"]/@value').extract_first()
        trynum = response.xpath('//*[@name="trynum"]/@value').extract_first()
        timezone = response.xpath('//*[@name="timezone"]/@value').extract_first()
        lgndim = response.xpath('//*[@name="lgndim"]/@value').extract_first()
        lgnrnd = response.xpath('//*[@name="lgnrnd"]/@value').extract_first()
        lgnjs = response.xpath('//*[@name="lgnjs"]/@value').extract_first()

        return scrapy.FormRequest.from_response(
            response,
            formdata={
                'email': EMAIL,
                'pass': PASSWORD,
                'legacy_return': legacy_return,
                'trynum': trynum,
                'timezone': timezone,
                'lgndim': lgndim,
                'lgnrnd': lgnrnd,
                'lgnjs': lgnjs
            },
            callback=self.after_login
        )

    def after_login(self, response):

        """remove_file('response.html')
        file = open('response.html', mode='w')
        file.write(str(response.body))"""

        remove_file(LIKES_FILENAME)

        if COOKIES_ARE_NOT_ENABLED in response.body:
            self.logger.error("\n\nLogin Failed (Cookies are not enabled)...................\n")
            return

        elif WRONG_PASSWORD in str(response.body):
            self.logger.error("\n\nLogin Failed (Wrong email or password)...................\n")
            return

        elif ID_CONFIRMATION_NEEDED in response.body:
            self.logger.error("\n\nLogin Failed (Identity confirmation required)...................\n")
            return

        elif CONNECTION_FAILED in response.body:
            self.logger.error("\n\nLogin Failed (Unknown issue)...................\n")
            return

        elif ACCOUNT_SUSPENDED in response.body:
            self.logger.error("\n\nAccount Suspended (Suspicious activity)...................\n")
            return

        elif PHOTO_UPLOAD_NEEDED in response.body:
            self.logger.error("\n\nAccount Suspended (Identity confirmation with a photo needed)...................\n")
            return

        self.logger.info("\n\nLogin Successful........................\n")
        href = response.urljoin(self.scrap_urls[0])

        self.logger.info("\n\nStarting to extract liked pages...............\n")
        yield scrapy.Request(url=href, callback=self.parse_likes)

    def parse_likes(self, response):
        # Avoid storing 'load more' in txt likes file
        get_more_item_text = response.css('#m_more_item').xpath('a/span/text()').get()

        # Likes
        raw_likes = response.css('#objects_container')
        extracted_data = raw_likes.xpath('//span/text()').getall()

        # Load more links
        get_more_item_links = response.css('#m_more_item').xpath('a/@href').getall()

        if extracted_data is not None:
            # todo: add test => has to be string
            for data in extracted_data:
                if data != get_more_item_text and data is not None:
                    like = clean_html_text(data)
                    if like != "" and like != get_more_item_text:
                        # Split likes to add more entries in dictionary
                        # Ex: Roger Federer => roger, federer, rogerfederer
                        split_like = like.split(' ')
                        for word in split_like:
                            if len(split_like) > 1 and len(word) > 2:
                                write_to_file(LIKES_FILENAME, word)
                                yield {
                                    '..........content': word,
                                }
                        write_to_file(LIKES_FILENAME, remove_spaces(like))
                        yield {
                            '..........content': like,
                        }
                    else:
                        self.logger.info(".....................Empty data")

            """Loading more content"""
            for href in get_more_item_links:
                if href is not None:
                    yield scrapy.Request(url=response.urljoin(href), callback=self.parse_likes)

        else:
            self.logger.info(".....................Empty data")
