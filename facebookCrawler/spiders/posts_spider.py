import scrapy

from utils.textCleaner import clean_html_text
from utils.setup import *
from utils.fileUtils import write_to_file, remove_file
from utils.facebookUrls import generate_posts_url


class PostSpider(scrapy.Spider):
    name = "posts_spider"
    start_urls = ['https://www.facebook.com/']
    #scrap_urls = [generate_posts_url(USER_ID)]

    def __init__(self, user_id=None, *args, **kwargs):
        super(PostSpider, self).__init__(*args, **kwargs)
        self.scrap_urls = [generate_posts_url(user_id)]

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

        remove_file(POSTS_FILENAME)

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
        yield scrapy.Request(url=href, callback=self.parse_posts)

    def parse_posts(self, response):
        self.logger.info("\n\nStarting to extract posts...............\n")
        posts_selector = '.bw'

        for post in response.css(posts_selector):

            content_selector = './/span/p'

            extracted_data = post.xpath(content_selector).extract_first()
            if extracted_data is not None:
                extracted_data = clean_html_text(extracted_data)
                if extracted_data != "":
                    self.logger.info("post content: " + extracted_data)
                    write_to_file('posts.csv', [extracted_data])
                    yield {
                        '..........content': extracted_data,
                    }

        """ ----- LOAD MORE POSTS ----- """
        see_more_pager_selector = '#see_more_pager'
        load_more_posts_selector = './/a/@href'

        href = response.css(see_more_pager_selector).xpath(load_more_posts_selector).extract_first()
        self.logger.info("\n\nLoading more posts..........................\n")

        if href is not None:
            yield scrapy.Request(url=response.urljoin(href), callback=self.parse_posts)

