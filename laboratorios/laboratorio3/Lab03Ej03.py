import dns.resolver

domain = "www.friv.com"

result = dns.resolver.resolve(domain, 'A')

 

for ip in result:
    print(f"IP Address: {ip}")