import scrapy
import sys

from time import strptime

from utils.textCleaner import clean_html_text, remove_spaces
from utils.fileUtils import *
from utils.setup import *


class AboutSpider(scrapy.Spider):
    name = "about_spider"
    start_urls = ['https://www.facebook.com/']

    def __init__(self, user_id=None, *args, **kwargs):
        super(AboutSpider, self).__init__(*args, **kwargs)
        self.scrap_urls = ['https://mbasic.facebook.com/' + user_id + '?v=info']

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

        remove_file(BIRTH_DATE_FILENAME)
        remove_file(ABOUT_FILENAME)
        remove_file(FULLNAME_FILENAME)

        if COOKIES_ARE_NOT_ENABLED in response.body:
            self.logger.error("\n\nLogin Failed (Cookies are not enabled)...................\n")
            sys.exit("Login Failed (Cookies are not enabled)")

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
        yield scrapy.Request(url=href, callback=self.parse_about)

    def parse_about(self, response):
        self.logger.info("\n\nStarting to extract basic information...............\n")

        xpath_selector_fullname = '//div[@id="root"]/div/div/div/div/span/div/span/strong/text()'
        xpath_selector_birth_date = '//div[@title="Birthday"]/table/tr/td/div/text()'
        xpath_selector_work = '//div[@id="work"]/div/div/div/div/div/div/span/a/text()'
        xpath_selector_workplace = '//div[@id="work"]/div/div/div/div/div/div[3]/span/text()'
        xpath_selector_education_places = '//div[@id="education"]/div/div/div/div/div/div/div/span/a/text()'
        xpath_selector_current_and_hometown = '//div[@id="living"]/div/div/div/div/table/tr/td/div/a/text()'
        xpath_selector_moving_in_places = '//div[@id="living"]/div/div/div/table/tr/td/div/a/text()'
        xpath_selector_nicknames = '//div[@id="nicknames"]/div/div/div/table/tr/td/div/text()'
        xpath_selector_religions = '//div[@id="religion"]/div/div/div/a/text()'
        xpath_selector_politics = '//div[@id="politics"]/div/div/div/a/text()'
        xpath_selector_skills = '//div[@id="skills"]/div/div/div/span/text()'
        xpath_selector_instagram_account_names = '//div[@title="Instagram"]/table/tbody/tr/td[2]/div/text()'
        xpath_selector_quotes = '//div[@id="quote"]/div/div/div/text()'

        fullname = response.xpath(xpath_selector_fullname).get()
        birth_date_text = response.xpath(xpath_selector_birth_date).get()
        work = response.xpath(xpath_selector_work).get()
        workplace = response.xpath(xpath_selector_workplace).get()
        education_places = response.xpath(xpath_selector_education_places).getall()
        current_and_hometown = response.xpath(xpath_selector_current_and_hometown).getall()
        moving_in_places = response.xpath(xpath_selector_moving_in_places).getall()
        nicknames = response.xpath(xpath_selector_nicknames).getall()
        religions = response.xpath(xpath_selector_religions).getall()
        politics = response.xpath(xpath_selector_politics).getall()
        skills = response.xpath(xpath_selector_skills).getall()
        instagram_account_names = response.xpath(xpath_selector_instagram_account_names).getall()
        quotes = response.xpath(xpath_selector_quotes).getall()

        if fullname is not None:
            self.logger.info("Extracting the fullname................\n")
            fullname = clean_html_text(fullname).split(" ")

            for name in fullname:
                if name is not None:
                    write_to_file(FULLNAME_FILENAME, name)

        if birth_date_text is not None:
            self.logger.info("Extracting the birth date.................\n")
            # Birth date format: Month day, year (ex: March 3, 1960)

            # Remove the comma
            birth_date_text = birth_date_text.replace(',', '')

            # Split the date
            birth_date_split = birth_date_text.split(" ")

            # Save year of birth
            year = birth_date_split[2]

            # Save month of birth
            month = str(strptime(birth_date_split[0], '%B').tm_mon)
            if len(month) < 2:
                month = '0' + month

            # Save day of birth
            day = birth_date_split[1]
            if len(day) < 2:
                day = '0' + day

            write_to_file(BIRTH_DATE_FILENAME, year + month + day)
            write_to_file(BIRTH_DATE_FILENAME, year + day + month)

        if work is not None:
            self.logger.info("Extracting work.................\n")
            work = clean_html_text(work)
            write_several_words(ABOUT_FILENAME, work)
            write_to_file(ABOUT_FILENAME, remove_spaces(work))

        if workplace is not None:
            self.logger.info("Extracting workplace.................\n")
            workplace = clean_html_text(workplace)
            write_several_words(ABOUT_FILENAME, workplace)
            write_to_file(ABOUT_FILENAME, remove_spaces(workplace))

        for education_place in education_places:
            if education_place is not None:
                self.logger.info("Extracting education place(s).................\n")
                education_place = clean_html_text(education_place)
                write_several_words(ABOUT_FILENAME, education_place)
                write_to_file(ABOUT_FILENAME, remove_spaces(education_place))

        for town in current_and_hometown:
            # town format: TOWN, STATE
            if town is not None:
                self.logger.info("Extracting current and/or hometown + State or Country.................\n")
                write_to_file(ABOUT_FILENAME, remove_spaces(clean_html_text(town.split(',')[0])))
                write_to_file(ABOUT_FILENAME, remove_spaces(clean_html_text(town.split(", ")[1])))

        for town in moving_in_places:
            if town is not None:
                self.logger.info("Extracting recently moved in place(s).................\n")
                write_to_file(ABOUT_FILENAME, remove_spaces(clean_html_text(town)))

        for nickname in nicknames:
            if nickname is not None:
                self.logger.info("Extracting nickname(s).................\n")
                write_to_file(ABOUT_FILENAME, remove_spaces(clean_html_text(nickname)))

        for religion in religions:
            if religion is not None:
                self.logger.info("Extracting religion(s).................\n")
                religion = clean_html_text(religion)
                write_several_words(ABOUT_FILENAME, religion)
                write_to_file(ABOUT_FILENAME, remove_spaces(religion))

        for politic in politics:
            if politic is not None:
                self.logger.info("Extracting politic view(s).................\n")
                politic = clean_html_text(politic)
                write_several_words(ABOUT_FILENAME, politic)
                write_to_file(ABOUT_FILENAME, remove_spaces(politic))

        for skill in skills:
            if skill is not None:
                self.logger.info("Extracting skill(s).................\n")
                write_to_file(ABOUT_FILENAME, remove_spaces(clean_html_text(skill)))

        for account_name in instagram_account_names:
            if account_name is not None:
                self.logger.info("Extracting Instagram account name(s).................\n")
                write_to_file(ABOUT_FILENAME, remove_spaces(clean_html_text(account_name)))

        for quote in quotes:
            if quote is not None:
                self.logger.info("Extracting favorite quote(s).................\n")
                write_to_file(ABOUT_FILENAME, remove_spaces(clean_html_text(quote)))
