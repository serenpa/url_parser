"""
	URL parser

	Author: Ashley Williams
"""

import codecs

TLD_FILE = "/home/cosc/student/awi111/Dropbox/PhD/PhD Share - Ash and Austen/Citations Replication/code/Deduplication/url_parser/tlds.txt"

def get_protocol(url, default="http"):
	"""
		Extracts the protocol, or returns value of default param (defaults to http)
	"""
	double_slash = url.find("//")

	if double_slash == -1:
		protocol = default
	else:
		protocol = url[:url.find('//')]
		if protocol.endswith(':'):
			protocol = protocol[:-1]

		if protocol == "":
			protocol = default

	return protocol



def get_all_tlds():
	"""
		Returns a list of TLDs from file
	"""
	tlds = []

	ifile = codecs.open(TLD_FILE, encoding="utf-8")

	for line in ifile:
		line = str(line)
		line = line.strip()
		if line != "" and line[0] not in ["/","\n"]:
			tlds.append(line)
	return tlds



def get_tld(url):
	"""
		Extracts the TLD from the URL
	"""
	tlds = get_all_tlds()

	max_tld_length = len(tlds[0])

	for tld in tlds:
		if len(tld) > max_tld_length:
			max_tld_length = len(tld)


	if url.find("//") != -1:
		url = url[url.find("//")+2:]

	url = url[:url.find("/")]

	candidates = []
	max_pos = -1

	for i in range(max_tld_length,0,-1):
		flag = False

		for tld in tlds:
			if len(tld) == i:
				pos = url.find("." + tld)
				if  pos > -1:
					candidates.append(tld)
					if pos > max_pos:
						max_pos = pos
					flag = True
		if flag:
			break

	for candidate in candidates:
		pos = url.find("." + candidate)

		if pos == max_pos:
			return candidate

	# if still no tld found
	raise Exception("No TLD found for: " + url)



def get_domain(url):
	"""
		Extracts the domain from the URL
	"""
	if url.find("//") != -1:
		url = url[url.find("//")+2:]

	url = url[:url.find(get_tld(url))]

	if url.endswith("."):
		url = url[:-1]

	parts = url.split(".")

	if len(parts) >= 2:
		return parts[-1]
	elif len(parts) == 1:
		return parts[0]
	else:
		raise Exception("Domain couldn't be extracted, is the URL empty?")



def get_subdomain(url, default="www"):
	"""
		Extracts the subdomain, or returns value of default param (defaults to www)
	"""
	if url.find("//") != -1:
		url = url[url.find("//")+2:]

	url = url[:url.find(get_domain(url))]

	if url.endswith("."):
		url = url[:-1]

	if url == "":
		return default
	else:
		return url



def get_path(url):
	"""
		Extracts the path from the URL
	"""
	if url.find("//") != -1:
		url = url[url.find("//")+2:]

	if url.find("/") != -1:
		path = url[url.find("/")+1:]
	else:
		return ""

	clean_path = ""

	if get_bookmark(path) == "" and get_query_parameters(path) == "":
		clean_path = path
	elif get_bookmark(path) != "" and get_query_parameters(path) == "":
		path = path.split("#")
		clean_path = path[0]
	elif get_bookmark(path) == "" and get_query_parameters(path) != "":
		path = path.split("?")
		clean_path = path[0]
	elif get_bookmark(path) != "" and get_query_parameters(path) != "":
		hash_pos = path.find("#")
		query_pos = path.find("?")
		clean_path = path[:min(hash_pos, query_pos)]

	if clean_path.endswith("/"):
		clean_path = clean_path[:-1]

	return clean_path



def get_port(url, default="80"):
	"""
		Extracts the port, or returns value of default param (defaults to 80)
	"""
	if url.find("//") != -1:
		url = url[url.find("//")+2:url.find("/",url.find("//")+2)]

	parts = url.split(":")

	if len(parts) == 2:
		port = parts[1]

		extracted_port = ""

		for i in range(0, len(port)):
			if port[i] in [0,1,2,3,4,5,6,7,8,9]:
				extracted_port += port[i]
			else:
				if extracted_port != "":
					return extracted_port
				else:
					return default

	elif len(parts) == 1:
		return default
	else:
		raise Exception("More than one : was found in the URL, or the URL is empty: " + url)



def get_query_parameters(url):
	"""
		Extracts the query parameters from the URL
	"""
	parts = url.split("?")

	res = []

	if len(parts) == 2:
		query_params = parts[1]

		contains_hash = query_params.find("#")
		contains_slash = query_params.find("/")

		if contains_hash == -1 and contains_slash == -1:
			query_params = query_params
		elif contains_hash == -1 and contains_slash > 0:
			query_params = query_params[:contains_slash]
		elif contains_hash > 0 and contains_slash == -1:
			query_params = query_params[:contains_hash]
		elif contains_hash > 0 and contains_slash > 0:
			query_params = query_params[:min(contains_hash, contians_slash)]


		for i in [";",","]:
			query_params = query_params.replace(i, "&")

		items = query_params.split("&")

		for i in items:
			try:
				item_parts = i.split("=")

				if len(item_parts) == 1:
					item_parts.append("")

				res.append({
					"param": item_parts[0],
					"value": item_parts[1]
				})
			except Exception as e:
				raise Exception("Error parsing: " + i)


		return res


	elif len(parts) == 1:
		return res
	else:
		raise Exception("More than one ? was found in the URL, or the URL is empty")



def get_bookmark(url):
	"""
		Extracts the bookmark from the URL
	"""
	if url.find("#!") == -1:
		parts = url.split("#")
	else:
		path_parts = url.split("#!")
		parts = path_parts[-1].split("#")

	if len(parts) == 2:
		return parts[1]
	elif len(parts) == 1:
		return ""
	else:
		raise Exception("More than one # was found in the URL, or the URL is empty")




def get_base_url(url):
	"""
		Returns the extracted base_url
		(subdomain + domain + tld + path)
	"""
	subdomain = get_subdomain(url)
	domain = get_domain(url)
	path = get_path(url)
	tld = get_tld(url)

	return "{0}.{1}.{2}/{3}/".format(subdomain, domain, tld, path)



def get_base_url_with_query_params(url):
	"""
		Returns the extracted base_url with query parameters
		(subdomain + domain + tld + path + query_params)
	"""
	subdomain = get_subdomain(url)
	domain = get_domain(url)
	path = get_path(url)
	tld = get_tld(url)

	query_params = get_query_parameters(url)

	qp_string = "?"

	for param in query_params:
		qp_string += param["param"] + "=" + param["value"] + "&"

	return "{0}.{1}.{2}/{3}{4}".format(subdomain, domain, tld, path, qp_string)



def get_full_domain(url):
	"""
		Returns the extracted domain
		(subdomain + domain + tld)
	"""
	subdomain = get_subdomain(url)
	domain = get_domain(url)
	tld = get_tld(url)

	return "{0}.{1}.{2}".format(subdomain, domain, tld)



def parse_url(url):
	"""
		Returns a JSON object with the parsed url parts
	"""
	protocol = get_protocol(url)
	subdomain = get_subdomain(url)
	domain = get_domain(url)
	port = get_port(url)
	path = get_path(url)
	query_params = get_query_parameters(url)
	bookmark = get_bookmark(url)
	tld = get_tld(url)

	base_url = get_base_url(url)
	base_url_with_query_params = get_base_url_with_query_params(url)
	full_domain = get_full_domain(url)


	res = {
		"url": url,
		"protocol": protocol,
		"subdomain": subdomain,
		"domain": domain,
		"port": port,
		"path": path,
		"query_params": query_params,
		"bookmark": bookmark,
		"base_url": base_url,
		"full_domain": full_domain,
		"base_url_with_query_params": base_url_with_query_params,
		"tld": tld
	}

	return res
