import scrapy

from time import strptime

from utils.textCleaner import clean_html_text, remove_spaces
from utils.fileUtils import *
from utils.setup import *


class FamilySpider(scrapy.Spider):
    name = "family_spider"
    start_urls = ['https://www.facebook.com/']
    #scrap_urls = ['https://mbasic.facebook.com/' + USERNAME + '/about']
    #scrap_urls = ['https://mbasic.facebook.com/' + USER_ID]
    family_members_profile_url_array = []

    def __init__(self, user_id=None, *args, **kwargs):
        super(FamilySpider, self).__init__(*args, **kwargs)
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

        remove_file(FAMILY_MEMBERS_ABOUT_FILENAME)
        remove_file(FAMILY_MEMBERS_FULLNAME_FILENAME)
        remove_file(FAMILY_MEMBERS_BIRTH_DATE)

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
        yield scrapy.Request(url=href, callback=self.parse_family_members_fullname)

    def parse_family_members_fullname(self, response):

        xpath_selector_family_members_fullname = '//div[@id="family"]/div/div/div/div/h3/a/text()'
        xpath_selector_family_members_profile_url = '//div[@id="family"]/div/div/div/div/h3/a/@href'

        family_members_fullname = response.xpath(xpath_selector_family_members_fullname).getall()
        family_members_profile_url = response.xpath(xpath_selector_family_members_profile_url).getall()

        # Writing every name of each family members in './family_fullname.txt'
        for family_member_fullname in family_members_fullname:
            if family_member_fullname is not None:
                fullname = clean_html_text(family_member_fullname).split(" ")
                for name in fullname:
                    if name is not None:
                        write_to_file(FAMILY_MEMBERS_FULLNAME_FILENAME, name)

        # Add all family members profile url => We'll scan every profile page of each member
        for family_member_profile_url in family_members_profile_url:
            if family_member_profile_url is not None:
                self.family_members_profile_url_array.append(family_member_profile_url)
                href = response.urljoin('https://mbasic.facebook.com' + family_member_profile_url)
                yield scrapy.Request(url=href, callback=self.parse_family_members_about)

    def parse_family_members_about(self, response):
        self.logger.info("\n\nStarting to extract basic information of relatives...............\n")

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

        if birth_date_text is not None:
            self.logger.info("Extracting the birth date of relatives.................\n")
            # Birth date format: Month day, year (ex: March 3, 1960)

            # Remove the comma
            birth_date_text = birth_date_text.replace(',', '')

            # Split the date
            birth_date_split = birth_date_text.split(" ")

            # Save year of birth
            write_to_file(FAMILY_MEMBERS_BIRTH_DATE, birth_date_split[2])

            # Save month of birth
            month = str(strptime(birth_date_split[0], '%B').tm_mon)
            if len(month) < 2:
                month = '0' + month
            write_to_file(FAMILY_MEMBERS_BIRTH_DATE, month)

            # Save day of birth
            day = birth_date_split[1]
            if len(day) < 2:
                day = '0' + day
            write_to_file(FAMILY_MEMBERS_BIRTH_DATE, day)

        if work is not None:
            self.logger.info("Extracting work of relatives.................\n")
            write_to_file(FAMILY_MEMBERS_ABOUT_FILENAME, remove_spaces(clean_html_text(work)))

        if workplace is not None:
            self.logger.info("Extracting workplace of relatives.................\n")
            workplace = clean_html_text(workplace)
            write_several_words(FAMILY_MEMBERS_ABOUT_FILENAME, workplace)
            write_to_file(FAMILY_MEMBERS_ABOUT_FILENAME, remove_spaces(workplace))

        for education_place in education_places:
            if education_places is not None:
                self.logger.info("Extracting education place(s) of relatives.................\n")
                education_place = clean_html_text(education_place)
                write_several_words(FAMILY_MEMBERS_ABOUT_FILENAME, education_place)
                write_to_file(FAMILY_MEMBERS_ABOUT_FILENAME, remove_spaces(education_place))

        for town in current_and_hometown:
            # town format: TOWN, STATE
            if town is not None:
                self.logger.info("Extracting current and/or hometown + State or Country of relatives.................\n")
                write_to_file(FAMILY_MEMBERS_ABOUT_FILENAME, remove_spaces(clean_html_text(town.split(',')[0])))
                write_to_file(FAMILY_MEMBERS_ABOUT_FILENAME, remove_spaces(clean_html_text(town.split(", ")[1])))

        for town in moving_in_places:
            if town is not None:
                self.logger.info("Extracting recently moved in place(s) of relatives.................\n")
                write_to_file(FAMILY_MEMBERS_ABOUT_FILENAME, remove_spaces(clean_html_text(town)))

        for nickname in nicknames:
            if nickname is not None:
                self.logger.info("Extracting nickname(s) of relatives.................\n")
                write_to_file(FAMILY_MEMBERS_ABOUT_FILENAME, remove_spaces(clean_html_text(nickname)))

        for religion in religions:
            if religion is not None:
                self.logger.info("Extracting religion(s).................\n")
                religion = clean_html_text(religion)
                write_several_words(FAMILY_MEMBERS_ABOUT_FILENAME, religion)
                write_to_file(FAMILY_MEMBERS_ABOUT_FILENAME, remove_spaces(religion))

        for politic in politics:
            if politic is not None:
                self.logger.info("Extracting politic view(s).................\n")
                politic = clean_html_text(politic)
                write_several_words(FAMILY_MEMBERS_ABOUT_FILENAME, politic)
                write_to_file(FAMILY_MEMBERS_ABOUT_FILENAME, remove_spaces(politic))

        for skill in skills:
            if skill is not None:
                self.logger.info("Extracting professional skill(s) of relatives.................\n")
                write_to_file(FAMILY_MEMBERS_ABOUT_FILENAME, remove_spaces(clean_html_text(skill)))