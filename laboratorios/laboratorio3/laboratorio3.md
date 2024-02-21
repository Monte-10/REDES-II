# 1. Introducción a DNS
;; Got recursion not available from 150.244.64.23, trying next server
Server:		150.244.214.200
Address:	150.244.214.200#53

Non-authoritative answer:
Name:	google.com
Address: 216.58.209.78
;; Got recursion not available from 150.244.64.23, trying next server
Name:	google.com
Address: 2a00:1450:4003:801::200e

# 2. Estructura de una Consulta DNS
; <<>> DiG 9.18.18-0ubuntu0.22.04.1-Ubuntu <<>> google.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: REFUSED, id: 60910
;; flags: qr rd; QUERY: 1, ANSWER: 0, AUTHORITY: 0, ADDITIONAL: 1
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
; COOKIE: 74d427484f985c4f4474fa6c65d5c369a08fa08428a87b90 (good)
;; QUESTION SECTION:
;google.com.			IN	A

;; Query time: 0 msec
;; SERVER: 150.244.64.23#53(150.244.64.23) (UDP)
;; WHEN: Wed Feb 21 10:33:29 CET 2024
;; MSG SIZE  rcvd: 67

# 3. Programación en Python con DNS
Script subido por separado
Resultado:
  e420674@1-21-1-21:~$ python3 Lab03Ej03.py 
  IP Address: 207.244.69.244
  IP Address: 207.244.86.26
  IP Address: 23.105.171.82
  IP Address: 23.105.171.94
  IP Address: 23.105.171.150
  IP Address: 192.96.201.39
  IP Address: 198.7.62.130

