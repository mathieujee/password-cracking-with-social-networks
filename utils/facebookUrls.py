import base64


# Generate url to list every public posts of a user
# src: https://gist.github.com/nemec/2ba8afa589032f20e2d6509512381114
def generate_posts_url(user_id):
    url = 'https://mbasic.facebook.com/search/posts/?q=*&epa=FILTERS&filters='

    json_arg = '{"rp_author":"{\\"name\\":\\"author\\",\\"args\\":\\"' + user_id + '\\"}"}'

    json_arg_b64 = base64.b64encode(json_arg.encode('ascii'))

    return url + json_arg_b64.decode('ascii')
