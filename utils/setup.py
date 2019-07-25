# Email used to login on the Facebook account
EMAIL = 'raymondguimond@yandex.com'

# Password used to login on the Facebook account
PASSWORD = '342ru80djio3532r'

# TARGET ID (USED TO LIST PUBLIC POSTS)
# USER_ID = '100002889939996'  # Sean
# USER_ID = '1180157665'
# USER_ID = '100039761583594'  # Jean Dupond

# MODIFY TARGET USERNAME
# USERNAME = 'sean.michel.18'
# USERNAME = 'noemie.schurch'

##
# user_id = '1223834491'  # loic.schurch
# user_id = '100034444458552'  # lome.suspect
# user_id = '100034550621457'  # takeme.toschurch
# user_id = '1180157665'  # noemie.schurch
# user_id = '100002889939996'  # sean.michel.18

# DEFAULT WORDLISTS FILENAMES
TARGET_USERNAME = 'basic_wordlists/target_username.txt'
POSTS_FILENAME = 'basic_wordlists/posts.txt'
LIKES_FILENAME = 'basic_wordlists/likes.txt'
BIRTH_DATE_FILENAME = 'basic_wordlists/birth_date.txt'
ABOUT_FILENAME = 'basic_wordlists/about.txt'
FULLNAME_FILENAME = 'basic_wordlists/fullname.txt'
FAMILY_MEMBERS_FULLNAME_FILENAME = 'basic_wordlists/family_fullname.txt'
FAMILY_MEMBERS_ABOUT_FILENAME = 'basic_wordlists/family_about.txt'
FAMILY_MEMBERS_BIRTH_DATE = 'basic_wordlists/family_birth_date.txt'

# EXTENDED WORDLISTS
EXTENDED_BIRTH_DATE_FILENAME = 'extended_wordlists/ext_birth_date.txt'
EXTENDED_FULLNAME_FILENAME = 'extended_wordlists/ext_fullname.txt'
EXTENDED_ABOUT_FILENAME = 'extended_wordlists/ext_about.txt'
EXTENDED_LIKES_FILENAME = 'extended_wordlists/ext_likes.txt'
ROCKYOU = 'extended_wordlists/rockyou.txt'

# LOGIN RESPONSE (DO NOT MODIFY)
COOKIES_ARE_NOT_ENABLED = b"Cookies are not enabled on your browser. Please enable cookies in your browser " \
                          b"preferences to continue."
WRONG_PASSWORD = "The password you've entered is incorrect."
ID_CONFIRMATION_NEEDED = b"We Need to Confirm Your Identity"
CONNECTION_FAILED = b"join Facebook today."
ACCOUNT_SUSPENDED = b"We noticed suspicious activity on your account. To get back on Facebook, " \
                    b"we need you to provide some additional info."
PHOTO_UPLOAD_NEEDED = b"To get back on Facebook, upload a photo that clearly shows your face."


# DEFAULT HASHCAT RULES FILENAMES
BIRTH_DATE_RULES = 'rules/birth_date_rules.rule'
CUSTOM_BASIC_RULES = 'rules/custom_rules.rule'
BEST_64_RULES = 'rules/best64.rule'

# DEFAULT HASH FILENAME
HASH_FILENAME = 'dupond_hashes.hash2'

# DEFAULT CRACKED HASHES FILENAMES
CRACKED_HASHES = 'cracked.txt'

# HASHCAT SETUP
HASH_TYPE = '0'  # MD5

# HASHCAT COMMANDS
"""
HASHCAT_BASE_COMMAND = ['hashcat', '--force', '--potfile-disable', '-m', HASH_TYPE, HASH_FILENAME]
HASHCAT_BIRTH_DATE_COMMAND = [BIRTH_DATE_FILENAME, '-r', BIRTH_DATE_RULES, '-o', CRACKED_HASHES]
HASHCAT_FULLNAME_COMMAND = [FULLNAME_FILENAME, '-r', CUSTOM_BASIC_RULES, '-o', CRACKED_HASHES]
HASHCAT_ABOUT_COMMAND = [ABOUT_FILENAME, '-r', CUSTOM_BASIC_RULES, '-o', CRACKED_HASHES]
HASHCAT_LIKES_COMMAND = [LIKES_FILENAME, '-r', CUSTOM_BASIC_RULES, '-o', CRACKED_HASHES]
HASHCAT_FAMILY_FULLNAME_COMMAND = [FAMILY_MEMBERS_FULLNAME_FILENAME, '-r', CUSTOM_BASIC_RULES, '-o', CRACKED_HASHES]
HASHCAT_FAMILY_ABOUT_COMMAND = [FAMILY_MEMBERS_ABOUT_FILENAME, '-r', CUSTOM_BASIC_RULES, '-o', CRACKED_HASHES]
HASHCAT_BIRTH_DATE_AND_FULLNAME_COMMAND = []
HASHCAT_BIRTH_DATE_AND_ABOUT_COMMAND = []
HASHCAT_BIRTH_DATE_AND_LIKES_COMMAND = []
HASHCAT_BIRTH_DATE_AND_FAMILY_FULLNAME_COMMAND = []
HASHCAT_BIRTH_DATE_AND_FAMILY_ABOUT_COMMAND = []
HASHCAT_ABOUT_AND_FULLNAME_COMMAND = []
HASHCAT_ABOUT_AND_LIKES_COMMAND = []
HASHCAT_ABOUT_AND_FAMILY_FULLNAME_COMMAND = []
HASHCAT_ABOUT_AND_FAMILY_ABOUT_COMMAND = []
HASHCAT_FULLNAME_AND_LIKES_COMMAND = []
HASHCAT_FULLNAME_AND_FAMILY_FULLNAME_COMMAND = []
HASHCAT_FULLNAME_AND_FAMILY_ABOUT_COMMAND = []
HASHCAT_LIKES_AND_FAMILY_FULLNAME_COMMAND = []
HASHCAT_LIKES_AND_FAMILY_ABOUT_COMMAND = []
HASHCAT_FAMILY_FULLNAME_AND_FAMILY_ABOUT_COMMAND = []
HASHCAT_GENERATE_BIRTH_DATE_WORD_LIST_COMMAND = ['hashcat', '--force', '--stdout', BIRTH_DATE_FILENAME, '-r',
                                                 BIRTH_DATE_RULES]
HASHCAT_GENERATE_FULLNAME_WORD_LIST_COMMAND = ['hashcat', '--force', '--stdout', FULLNAME_FILENAME, '-r',
                                               CUSTOM_BASIC_RULES]"""

# SPECIAL CHARSET
SPECIAL_CHARSET = ['.', ':', ',', ';', '-', '_', '+', '@', '*', '#', '%', '&', '/', '=', '?', '$', '!', '\\']
