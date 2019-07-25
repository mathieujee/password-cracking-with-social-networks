from utils.facebookUrls import *


def test_generate_facebook_posts_url():
    expected_url1 = 'https://mbasic.facebook.com/search/posts/?q=*&epa=FILTERS&filters=eyJycF9hdXRob3IiOiJ7XCJuYW1lXCI6XCJhdXRob3JcIixcImFyZ3NcIjpcIjEyMjM4MzQ0OTFcIn0ifQ=='
    user_id1 = '1223834491'

    expected_url2 = 'https://mbasic.facebook.com/search/posts/?q=*&epa=FILTERS&filters=eyJycF9hdXRob3IiOiJ7XCJuYW1lXCI6XCJhdXRob3JcIixcImFyZ3NcIjpcIjExODAxNTc2NjVcIn0ifQ=='
    user_id2 = '1180157665'

    assert generate_posts_url(user_id1) == expected_url1
    assert generate_posts_url(user_id2) == expected_url2
