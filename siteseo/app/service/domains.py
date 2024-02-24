import dns.resolver
import socket
import requests
from urllib.parse import urlsplit

def check_spf_record(url):
    domain = urlsplit(url).netloc
    try:
        # Perform a DNS query for SPF records
        answers = dns.resolver.resolve(domain, "TXT")
        # Check if any TXT record contains "v=spf1"
        for rdata in answers:
            for txt_string in rdata.strings:
                print(txt_string)
                if b"v=spf1" in txt_string:
                    return txt_string
                else:
                    return False

        print(f"No SPF record found for {domain}.")
        return False

    except dns.resolver.NXDOMAIN:
        print(f"Domain {domain} does not exist.")
        return False
    except dns.resolver.NoAnswer:
        print(f"No TXT records found for {domain}.")
        return False
    except dns.resolver.Timeout:
        print("DNS query timeout. Check your internet connection or DNS server.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
def resolve_to_same_url(url1):
    try:
        original_string = url1
        url2 = original_string.replace("https://", "https://www.")

        # Resolve IP addresses for both URLs
        ip_address_1 = socket.gethostbyname(url1)
        ip_address_2 = socket.gethostbyname(url2)

        # Check if the resolved IP addresses are the same
        if ip_address_1 == ip_address_2:
            return f"The URLs {url1} and {url2} resolve to the same IP address: {ip_address_1}"

        else:
            return f"The URLs {url1} and {url2} do not resolve to the same IP address. {url1} - {ip_address_1}, {url2} - {ip_address_2}"

    except socket.error as e:
        print(f"Error: {e}")
        return None
def has_redirect(url):
    try:
        response = requests.head(url, allow_redirects=False)
        # Check the status code for redirects
        if 300 <= response.status_code < 400:
            return response.headers["Location"]
        else:
            return None
    except requests.RequestException as e:
        print(f"Error {e}")