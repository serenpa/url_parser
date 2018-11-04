import url_parser

urls = ['http://www.foo.com/bar?a=b&c=d',
	'http://www.foo.com:80/bar?c=d;a=b',
	'http://www.foo.com/bar/?c=d',
	'http://www.foo.com:80/bar?c=d#comments',
	'http://www.foo.com:80/bar/?c=d#comments',
	'http://foo.com:80/bar?c=d',
	'https://foo.com/bar/',
	'//foo.com/bar',
	'foo.com/bar'
]
	
def main():

	base_urls = []
	domains = []

	for url in urls:
		parsed_url = url_parser.parse_url(url)
		
		if parsed_url["base_url"] not in base_urls:
			base_urls.append(parsed_url["base_url"])
			
		
		if parsed_url["full_domain"] not in domains:
			domains.append(parsed_url["full_domain"])
	
	print(base_urls, domains)
	

if __name__ == '__main__':
	main()