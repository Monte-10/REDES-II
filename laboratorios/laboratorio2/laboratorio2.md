# 1. Introduccion a HTTP
## ¿Que significa el codigo de respuesta? Sigue enviando respuestas hasta que consigas el codigo HTML de la pagina indice de la universidad.
HTTP/1.1 302 Found
Date: Wed, 21 Feb 2024 09:22:04 GMT
Referrer-Policy: same-origin
X-Content-Type-Options: nosniff
Location: https://www.uam.es/uam/inicio
Content-Length: 213
Content-Type: text/html; charset=iso-8859-1
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>302 Found</title>
</head><body>
<h1>Found</h1>
<p>The document has moved <a href="https://www.uam.es/uam/inicio">here</a>.</p>
</body></html>

## Haz ahora una petición a una URL inexistente del mismo servidor, y observa la respuesta.
HTTP/1.1 404 Not Found
Date: Wed, 21 Feb 2024 09:24:11 GMT
Referrer-Policy: same-origin
X-Content-Type-Options: nosniff
Last-Modified: Thu, 08 Apr 2021 08:36:50 GMT
ETag: "a8b-5bf71f2d7ece3"
Accept-Ranges: bytes
Content-Length: 2699
X-XSS-Protection: 1; mode=block
X-Frame-Options: SAMEORIGIN
Content-Type: text/html

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="es" xml:lang="es">
	<head>
		<title>Universidad Autónoma de Madrid</title>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<meta name="Keywords" content="xxx" />
		<meta name="Description" content="xxx" />
		<meta name="Autor" content="Indra Sistemas S.A" />
		<meta name="Copyright" content="Universidad Autónoma de Madrid" />
		<meta name="Robots" content="all" />
		<script type="text/javascript"> 
			function FuncionalidadAtras() { 
				var atraserr = document.getElementById('atraserror'); 
				atraserr.style.display="block";
				if(!atraserr ) return; 
				atraserr.onclick = atraserr.onkeypress = function(){
					history.back();
					return false;
				}; 
			};
			window.onload = FuncionalidadAtras; 
		</script> 
		<style type="text/css">
			html{font-size:100%}
			body{font:62.5% Arial, Verdana, Helvetica, sans-serif; color:#555; text-align:center;}
			#contenido{margin:0 auto; width:98.4em; text-align:left; padding:0 .5em 0 1.5em;}
			.pantallaerror{background:url(/images/bg_pantallarror.gif) no-repeat top left; width:86em; height:51.3em; text-align:center; margin:8em auto; padding:3.9em 0 0 0;}
			.pantallaerror div {text-align:left; padding-left:4em; font-size:1.7em; color:#333; padding-top:2em;}
				.pantallaerror div img {float:left; margin:1em .5em 1.5em 0;}
				.pantallaerror div h2 {color:#02812d; font-size:1.4em; text-transform:uppercase; margin:.5em 0 0 0;}
				.pantallaerror div a {color:#02812d; font-weight:bold; font-size:.7em; text-align:center; text-decoration:none; display:block; clear:both;}
				.pantallaerror div a:hover {text-decoration:underline;}
				#atraserror{display:none;}
		</style>
<meta http-equiv="refresh"  content="5; url=/uam/inicio">
	</head>
	<body>
		<div id="cuerpo">
			<div id="contenido" class="clear">
				<div class="pantallaerror">
					<h1><img src="/images/logoerror.jpg" alt="Universidad Autónoma de Madrid" /></h1>
					<div>
						<img src="/images/alertaerror.jpg" alt="" />
						<h2>Atención:</h2>
						La página solicitada no se ha encontrado o el vínculo seguido es erróneo.<br />
						Por favor, disculpe la molestia.
						<h2>Warning:</h2>
						The requested object does not exist on this server. The link you followed is <br />either outdated, inaccurate.
						Please, excuse the inconvenience.
						<!-- <a href="#" id="atraserror">Volver a la página anterior / Back</a>-->
					<br><h4 align="center">Redirigiendo a página principal </h4>
					</div>	
				</div>	
			</div>
		</div>
	</body>
</html>

## ¿Cuál es la respuesta? ¿En qué momento sí devuelve el recurso? Prueba los comandos anteriores añadiendo el flag '-v', para observar también la petición, y no solo las respuestas.
curl -i -H "If-Modified-Since: Sat, 12 Feb 2022 12:00:00 GMT" https://uam.es
HTTP/1.1 302 Found
Date: Wed, 21 Feb 2024 09:25:49 GMT
Referrer-Policy: same-origin
X-Content-Type-Options: nosniff
Location: https://www.uam.es/uam/inicio
Content-Length: 213
Content-Type: text/html; charset=iso-8859-1
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>302 Found</title>
</head><body>
<h1>Found</h1>
<p>The document has moved <a href="https://www.uam.es/uam/inicio">here</a>.</p>

curl -v -i -H "If-Modified-Since: Sat, 12 Feb 2022 12:00:00 GMT" https://uam.es
* Host uam.es:443 was resolved.
* IPv6: (none)
* IPv4: 150.244.214.237
*   Trying 150.244.214.237:443...
* Connected to uam.es (150.244.214.237) port 443
* ALPN: curl offers h2,http/1.1
* TLSv1.3 (OUT), TLS handshake, Client hello (1):
*  CAfile: /opt/anaconda3/ssl/cacert.pem
*  CApath: none
* TLSv1.3 (IN), TLS handshake, Server hello (2):
* TLSv1.3 (IN), TLS handshake, Encrypted Extensions (8):
* TLSv1.3 (IN), TLS handshake, Certificate (11):
* TLSv1.3 (IN), TLS handshake, CERT verify (15):
* TLSv1.3 (IN), TLS handshake, Finished (20):
* TLSv1.3 (OUT), TLS change cipher, Change cipher spec (1):
* TLSv1.3 (OUT), TLS handshake, Finished (20):
* SSL connection using TLSv1.3 / TLS_AES_256_GCM_SHA384 / X25519 / RSASSA-PSS
* ALPN: server accepted http/1.1
* Server certificate:
*  subject: C=ES; ST=Madrid; O=Universidad Aut�noma de Madrid; CN=*.uam.es
*  start date: Jan  3 00:00:00 2024 GMT
*  expire date: Jan  2 23:59:59 2025 GMT
*  subjectAltName: host "uam.es" matched cert's "uam.es"
*  issuer: C=NL; O=GEANT Vereniging; CN=GEANT OV RSA CA 4
*  SSL certificate verify ok.
*   Certificate level 0: Public key type RSA (2048/112 Bits/secBits), signed using sha384WithRSAEncryption
*   Certificate level 1: Public key type RSA (4096/152 Bits/secBits), signed using sha384WithRSAEncryption
*   Certificate level 2: Public key type RSA (4096/152 Bits/secBits), signed using sha384WithRSAEncryption
* using HTTP/1.x
> GET / HTTP/1.1
> Host: uam.es
> User-Agent: curl/8.5.0
> Accept: */*
> If-Modified-Since: Sat, 12 Feb 2022 12:00:00 GMT
> 
* TLSv1.3 (IN), TLS handshake, Newsession Ticket (4):
* TLSv1.3 (IN), TLS handshake, Newsession Ticket (4):
* old SSL session ID is stale, removing
< HTTP/1.1 302 Found
HTTP/1.1 302 Found
< Date: Wed, 21 Feb 2024 09:26:08 GMT
Date: Wed, 21 Feb 2024 09:26:08 GMT
< Referrer-Policy: same-origin
Referrer-Policy: same-origin
< X-Content-Type-Options: nosniff
X-Content-Type-Options: nosniff
< Location: https://www.uam.es/uam/inicio
Location: https://www.uam.es/uam/inicio
< Content-Length: 213
Content-Length: 213
< Content-Type: text/html; charset=iso-8859-1
Content-Type: text/html; charset=iso-8859-1

< 
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>302 Found</title>
</head><body>
<h1>Found</h1>
<p>The document has moved <a href="https://www.uam.es/uam/inicio">here</a>.</p>
</body></html>
* Connection #0 to host uam.es left intact

# 2. Gestión de cookies
## ¿Cuál es el dominio para el que la establece?
## ¿Qué diferencias observas?
## ¿Qué ocurre? ¿Por qué?
## ¿Cómo se comporta el navegador si un servidor intenta establecer una cookie sin parámetro de 'Domain'?
## Investiga sobre qué diferencias hay entre una cookie "primaria" o normal, y una cookie terciaria. (first-party cookie vs third-party cookie)

# 3. Tokens JWT
# 4. Programación
