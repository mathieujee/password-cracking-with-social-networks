# Email used to login on the Facebook account
EMAIL = 'raymondguimond@yandex.com'

# Password used to login on the Facebook account
PASSWORD = '342ru80djio3532r'

# TARGET ID
# USER_ID = '100039761583594'  # Jean Dupond

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
HASH_FILENAME = 'hash.txt'

# DEFAULT CRACKED HASHES FILENAMES
CRACKED_HASHES = 'cracked.txt'

# HASHCAT SETUP
HASH_TYPE = '0'  # MD5

# SPECIAL CHARSET
SPECIAL_CHARSET = ['.', ':', ',', ';', '-', '_', '+', '@', '*', '#', '%', '&', '/', '=', '?', '$', '!', '\\']
