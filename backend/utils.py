import re
from django.core.exceptions import ValidationError
from lxml.html.clean import Cleaner
import html

def remove_html_tags(html_text):
	clean = re.compile('<.*?>') # remove regex html
	return re.sub(clean, '', html_text)



NON_SAFE_OS_PATH_CHARS = ["<", ">", ":", "/", "\\", "|", "?", "*"]

def contains_chars(string, chars):
	for char in chars:
		if char in string:
			return True
	return False


def validate_no_at_symbol(value):
    
    if contains_chars(value, NON_SAFE_OS_PATH_CHARS):
        raise ValidationError(f'This field cannot contain the symbols like: {" ".join(NON_SAFE_OS_PATH_CHARS)}.')



def capitalize_first_character(string):
	string = string.strip()
	return string[0].upper() + string[1:]



def sanitize_html(dirty_html):
	cleaner = Cleaner(
		javascript=True,
		scripts=True,
		comments=True,
		style=True,
		inline_style=True,
		meta=True,
		embedded=True,
		frames=True,
		forms=True,
		add_nofollow=True,
		safe_attrs_only=False,
		annoying_tags=True,
	)
	cleaned_html = html.unescape(cleaner.clean_html(html.unescape(dirty_html)))
	return cleaned_html


emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # Chinese/Japanese/Korean characters
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u200d"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\u3030"
                               u"\ufe0f"
                               "]+", flags=re.UNICODE)

from bs4 import BeautifulSoup
def remove_emoji_img_tags(html):
	soup = BeautifulSoup(html, 'html.parser')
	img_tags = soup.find_all('img')

	for img_tag in img_tags:
		src = img_tag.get('src')
		if src and '' in src:
			img_tag.extract()  # Remove the img tag from the soup
	# Return the modified HTML
	return str(soup)