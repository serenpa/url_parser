# URL Parser

A basic parser for comparing URLs.

## Example 1
Take the following sample data:

```python
urls = [
    'http://www.foo.com/bar?a=b&c=d',
	'http://www.foo.com:80/bar?c=d;a=b',
	'http://www.foo.com/bar/?c=d',
	'http://www.foo.com:80/bar?c=d#comments',
	'http://www.foo.com:80/bar/?c=d#comments',
	'http://foo.com:80/bar?c=d',
	'https://foo.com/bar/',
	'//foo.com/bar',
	'foo.com/bar'
]
```

Using the parser, they are all detected as accessing the same resource:

```python
    base_urls = []
	domains = []

	for url in urls:
		parsed_url = url_parser.parse_url(url)
		
		if parsed_url["base_url"] not in base_urls:
			base_urls.append(parsed_url["base_url"])
			
		if parsed_url["full_domain"] not in domains:
			domains.append(parsed_url["full_domain"])
	
	print(base_urls, domains)
```

The results:

```sh
['www.foo.com/bar/'] ['www.foo.com']
```

## Example 2
Running the following:
```python
import url_parser
url_parser.parse_url("http://www.foo.com:80/bar?c=d#comments'")
```
Returns the following JSON object:
```JSON
{
    'url': 'http://www.foo.com:80/bar?c=d#comments', 
    'protocol': 'http', 
    'subdomain': 'www', 
    'domain': 'foo', 
    'port': '80', 
    'path': 'bar', 
    'query_params': [
        {
            'param': 'c', 
            'value': 'd'
        }
    ], 
    'bookmark': 'comments', 
    'base_url': 'www.foo.com/bar/',
    'full_domain': 'www.foo.com', 
    'tld': 'com'
}
```

## Functions

| Function | Explaination |
| ------ | ------ |
| parse_url(url) | Returns a JSON object with the parsed url parts |
| get_full_domain(url) | Returns the extracted domain (subdomain + domain + tld) |
| get_base_url(url) | Returns the extracted base_url (subdomain + domain + tld + path) |
| get_bookmark(url) | Extracts the bookmark from the URL |
| get_query_parameters(url) | Extracts the query parameters from the URL |
| get_port(url, default="80") | Extracts the port, or returns value of default param (defaults to 80) |
| get_path(url) | Extracts the path from the URL |
| get_subdomain(url, default="www") | Extracts the subdomain, or returns value of default param (defaults to www) |
| get_domain(url) | Extracts the domain from the URL |
| get_tld(url) | Extracts the TLD from the URL |
| get_all_tlds() | Returns a list of TLDs from file |
| get_protocol(url, default="http") | Extracts the protocol, or returns value of default param (defaults to http) |




## License
MIT


