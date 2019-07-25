# !/usr/bin/env python

import sys
import os.path

from tqdm import tqdm
from twisted.internet import reactor, defer
from facebookCrawler.spiders import about_spider, family_spider, likes_spider, posts_spider
from utils.setup import *
from utils.hashcatUtils import *
from utils.fileUtils import remove_duplicate_lines_from_file

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
# src: https://stackoverflow.com/questions/47427271/scrapy-running-multiple-spiders-from-the-same-python-process-via-cmdline-fails


if len(sys.argv) > 1:

    configure_logging()
    runner = CrawlerRunner()

    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(about_spider.AboutSpider, user_id=sys.argv[1])
        yield runner.crawl(likes_spider.LikeSpider, user_id=sys.argv[1])
        yield runner.crawl(family_spider.FamilySpider, user_id=sys.argv[1])
        #yield runner.crawl(posts_spider.PostSpider, user_id=sys.argv[1])
        reactor.stop()

    crawl()
    reactor.run()

    # Example of hashcat complete command:
    # hashcat --force -m 0 hash.txt wordlists/birth_date.txt -r rules/birth_date_rules.rule -o cracked.txt

    # attack with rockyou.txt and best64.rule
    run_hashcat_rule_attack(HASH_FILENAME, HASH_TYPE, ROCKYOU, BEST_64_RULES, CRACKED_HASHES)

    with tqdm(total=100) as pbar:

        # Running hashcat with different wordlists sorted by priorities
        if os.path.isfile(BIRTH_DATE_FILENAME):
            # remove duplicate
            remove_duplicate_lines_from_file(BIRTH_DATE_FILENAME)

            # target's birth date
            run_hashcat_rule_attack(HASH_FILENAME, HASH_TYPE, BIRTH_DATE_FILENAME, BIRTH_DATE_RULES, CRACKED_HASHES,
                                    progress_bar=pbar)

            # generate extended birth date wordlist
            generate_extended_wordlist(BIRTH_DATE_FILENAME, EXTENDED_BIRTH_DATE_FILENAME, BIRTH_DATE_RULES,
                                       progress_bar=pbar)

            # attack with same dictionaries
            run_hashcat_combinator2_attack(HASH_FILENAME, HASH_TYPE, EXTENDED_BIRTH_DATE_FILENAME,
                                           EXTENDED_BIRTH_DATE_FILENAME, CRACKED_HASHES, progress_bar=pbar)

        pbar.update(10)

        if os.path.isfile(FULLNAME_FILENAME):
            # remove duplicate
            remove_duplicate_lines_from_file(FULLNAME_FILENAME)

            # target's fullname
            run_hashcat_rule_attack(HASH_FILENAME, HASH_TYPE, FULLNAME_FILENAME, CUSTOM_BASIC_RULES, CRACKED_HASHES,
                                    progress_bar=pbar)

            # generate extended fullname wordlist
            generate_extended_wordlist(FULLNAME_FILENAME, EXTENDED_FULLNAME_FILENAME, CUSTOM_BASIC_RULES,
                                       progress_bar=pbar)

            # attack with same dictionaries
            run_hashcat_combinator2_attack(HASH_FILENAME, HASH_TYPE, EXTENDED_FULLNAME_FILENAME,
                                           EXTENDED_FULLNAME_FILENAME, CRACKED_HASHES, progress_bar=pbar)

            # attack with same dictionaries + special char
            for c in SPECIAL_CHARSET:
                run_hashcat_special_char_combinator_attack(HASH_FILENAME, HASH_TYPE, EXTENDED_FULLNAME_FILENAME,
                                                           c, CRACKED_HASHES, progress_bar=pbar)

        pbar.update(10)

        if os.path.isfile(BIRTH_DATE_FILENAME) and os.path.isfile(FULLNAME_FILENAME):
            # target's birth date + fullname (runs 2 combinator attacks, one on each side:  word1word2 <=> word2word1
            run_hashcat_combinator2_attack(HASH_FILENAME, HASH_TYPE, EXTENDED_FULLNAME_FILENAME,
                                           EXTENDED_BIRTH_DATE_FILENAME, CRACKED_HASHES, progress_bar=pbar)

            # Adding special char attacks
            for c in SPECIAL_CHARSET:
                run_hashcat_special_char_combinator2_attack(HASH_FILENAME, HASH_TYPE, EXTENDED_BIRTH_DATE_FILENAME,
                                                            EXTENDED_FULLNAME_FILENAME, c, CRACKED_HASHES,
                                                            progress_bar=pbar)

        pbar.update(10)

        if os.path.isfile(ABOUT_FILENAME):
            # remove duplicate
            remove_duplicate_lines_from_file(ABOUT_FILENAME)

            # target's 'about' information
            run_hashcat_rule_attack(HASH_FILENAME, HASH_TYPE, ABOUT_FILENAME, CUSTOM_BASIC_RULES, CRACKED_HASHES,
                                    progress_bar=pbar)

            # generate extended about wordlist
            generate_extended_wordlist(ABOUT_FILENAME, EXTENDED_ABOUT_FILENAME, CUSTOM_BASIC_RULES, progress_bar=pbar)

            # attack with same dictionaries
            run_hashcat_combinator2_attack(HASH_FILENAME, HASH_TYPE, EXTENDED_ABOUT_FILENAME, EXTENDED_ABOUT_FILENAME,
                                           CRACKED_HASHES, progress_bar=pbar)

            # attack with same dictionaries + special char
            for c in SPECIAL_CHARSET:
                run_hashcat_special_char_combinator_attack(HASH_FILENAME, HASH_TYPE, EXTENDED_ABOUT_FILENAME,
                                                           c, CRACKED_HASHES, progress_bar=pbar)

        pbar.update(10)

        if os.path.isfile(ABOUT_FILENAME) and os.path.isfile(BIRTH_DATE_FILENAME):
            # target's 'about' information + birth date
            run_hashcat_combinator2_attack(HASH_FILENAME, HASH_TYPE, EXTENDED_ABOUT_FILENAME,
                                           EXTENDED_BIRTH_DATE_FILENAME, CRACKED_HASHES, progress_bar=pbar)

            # Adding special char attacks
            for c in SPECIAL_CHARSET:
                run_hashcat_special_char_combinator2_attack(HASH_FILENAME, HASH_TYPE, EXTENDED_ABOUT_FILENAME,
                                                            EXTENDED_BIRTH_DATE_FILENAME, c, CRACKED_HASHES,
                                                            progress_bar=pbar)
        pbar.update(10)

        if os.path.isfile(ABOUT_FILENAME) and os.path.isfile(FULLNAME_FILENAME):
            # target's 'about' information + fullname
            run_hashcat_combinator2_attack(HASH_FILENAME, HASH_TYPE, EXTENDED_ABOUT_FILENAME,
                                           EXTENDED_FULLNAME_FILENAME, CRACKED_HASHES, progress_bar=pbar)

            # Adding special char attacks
            for c in SPECIAL_CHARSET:
                run_hashcat_special_char_combinator2_attack(HASH_FILENAME, HASH_TYPE, EXTENDED_ABOUT_FILENAME,
                                                            EXTENDED_FULLNAME_FILENAME, c, CRACKED_HASHES,
                                                            progress_bar=pbar)

        pbar.update(10)

        if os.path.isfile(LIKES_FILENAME):
            # remove duplicate
            remove_duplicate_lines_from_file(LIKES_FILENAME)

            # target's 'likes'
            run_hashcat_rule_attack(HASH_FILENAME, HASH_TYPE, LIKES_FILENAME, CUSTOM_BASIC_RULES, CRACKED_HASHES,
                                    progress_bar=pbar)

            # generate extended likes wordlist
            generate_extended_wordlist(LIKES_FILENAME, EXTENDED_LIKES_FILENAME, CUSTOM_BASIC_RULES, progress_bar=pbar)

            # attack with same dictionaries
            run_hashcat_combinator2_attack(HASH_FILENAME, HASH_TYPE, EXTENDED_LIKES_FILENAME, EXTENDED_LIKES_FILENAME,
                                           CRACKED_HASHES,progress_bar=pbar)

            # attack with same dictionaries + special char
            for c in SPECIAL_CHARSET:
                run_hashcat_special_char_combinator_attack(HASH_FILENAME, HASH_TYPE, EXTENDED_LIKES_FILENAME,
                                                           c, CRACKED_HASHES, progress_bar=pbar)

        pbar.update(10)

        if os.path.isfile(LIKES_FILENAME) and os.path.isfile(BIRTH_DATE_FILENAME):
            # target's 'likes' + birth date
            run_hashcat_combinator2_attack(HASH_FILENAME, HASH_TYPE, EXTENDED_LIKES_FILENAME,
                                           EXTENDED_BIRTH_DATE_FILENAME, CRACKED_HASHES,progress_bar=pbar)

            # Adding special char attacks
            for c in SPECIAL_CHARSET:
                run_hashcat_special_char_combinator2_attack(HASH_FILENAME, HASH_TYPE, EXTENDED_LIKES_FILENAME,
                                                            EXTENDED_BIRTH_DATE_FILENAME, c, CRACKED_HASHES,
                                                            progress_bar=pbar)

        pbar.update(10)

        if os.path.isfile(LIKES_FILENAME) and os.path.isfile(FULLNAME_FILENAME):
            # target's 'likes' + fullname
            run_hashcat_combinator2_attack(HASH_FILENAME, HASH_TYPE, EXTENDED_LIKES_FILENAME,
                                           EXTENDED_FULLNAME_FILENAME, CRACKED_HASHES, progress_bar=pbar)

            # Adding special char attacks
            for c in SPECIAL_CHARSET:
                run_hashcat_special_char_combinator2_attack(HASH_FILENAME, HASH_TYPE, EXTENDED_LIKES_FILENAME,
                                                            EXTENDED_FULLNAME_FILENAME, c, CRACKED_HASHES,
                                                            progress_bar=pbar)
        pbar.update(10)

        if os.path.isfile(LIKES_FILENAME) and os.path.isfile(ABOUT_FILENAME):
            # target's 'likes' + 'about' information
            run_hashcat_combinator2_attack(HASH_FILENAME, HASH_TYPE, EXTENDED_LIKES_FILENAME, EXTENDED_ABOUT_FILENAME,
                                           CRACKED_HASHES, progress_bar=pbar)

            # Adding special char attacks
            for c in SPECIAL_CHARSET:
                run_hashcat_special_char_combinator2_attack(HASH_FILENAME, HASH_TYPE, EXTENDED_LIKES_FILENAME,
                                                            EXTENDED_ABOUT_FILENAME, c, CRACKED_HASHES,
                                                            progress_bar=pbar)

        pbar.update(10)

        # TODO: ADD FAMILY_BIRTH_DATE, FAMILY_FULLNAME and FAMILY_ABOUT dictionaries

    pbar.close()

else:
    print("\nAt least one argument is required: Facebook target's ID.")
