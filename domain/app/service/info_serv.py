from urllib.parse import urlsplit
import dns.resolver

def check_spf_record(url):
    domain = urlsplit(url).netloc
    ip_v4 = None
    ipv6_addresses = None
    txt_values = None
    cname_values = None
    try:
        a_records = dns.resolver.resolve(domain, 'A')
        ip_v4 = [str(record) for record in a_records]

        aaaa_records = dns.resolver.resolve(domain, 'AAAA')
        ipv6_addresses = [str(record) for record in aaaa_records]

        txt_records = dns.resolver.resolve(domain, 'TXT')
        txt_values = [str(record) for record in txt_records]

        # cname_records = dns.resolver.resolve(domain, 'CNAME')
        # cname_values = [str(record) for record in cname_records]

        ns_records = dns.resolver.resolve(domain, 'NS')
        nameservers = [str(record.target) for record in ns_records]

        return {
            "IPv4 Addresses (A records)": ip_v4,
            "IPv6 Addresses (AAAA records)": ipv6_addresses,
            "TXT Records": txt_values,
            "CNAME Records": cname_values,
            "Nameservers (NS records)": nameservers
        }

    except dns.resolver.NXDOMAIN:
        print(f"Domain {domain} does not exist.")
        return False
    except dns.resolver.NoAnswer:
        print(f"No records found for {domain}.")
        return False
    except dns.resolver.Timeout:
        print("DNS query timeout. Check your internet connection or DNS server.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False