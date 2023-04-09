CFSSL = podman run --rm -v $(PWD):/data -w /data --entrypoint sh docker.io/cfssl/cfssl
OPENSSL = openssl

.PHONY: all

ca-key.pem ca.pem: ca.json
	mkdir -p ca
	[ -f ca/ca-key.pem ] || $(CFSSL) -c 'cfssl gencert -initca ca.json | cfssljson -bare ca/ca'

server-key.pem server.pem: ca.pem ca-key.pem server.json profiles.json
	mkdir -p server
	$(CFSSL) -c 'cfssl gencert -ca ca/ca.pem -ca-key ca/ca-key.pem -config profiles.json -profile server server.json | cfssljson -bare server/server'

client-%.pem client-%-key.pem: ca.pem ca-key.pem client.json profiles.json
	mkdir -p clients
	sed 's/{{COMMON_NAME}}/$*/' client.json > clients/client-$*.json
	$(CFSSL) -c 'cfssl gencert -ca ca/ca.pem -ca-key ca/ca-key.pem -config profiles.json -profile client clients/client-$*.json | cfssljson -bare clients/client-$*'

client-%.pfx: client-%-key.pem client-%.pem
	$(OPENSSL) pkcs12 -export -inkey clients/client-$*-key.pem -in clients/client-$*.pem -out clients/client-$*.pfx -passout pass:nekomimi

all: ca.pem ca-key.pem server.pem server-key.pem