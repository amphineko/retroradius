PODMAN := $(shell which podman 2>/dev/null)

TEMPLATES = $(wildcard utils/authorized_c/*.j2)

.PHONY: all

authorized_c: utils/authorized_c/compiler.py utils/authorized_c/Containerfile $(TEMPLATES)
	$(PODMAN) build -t authorized_c -f utils/authorized_c/Containerfile utils/authorized_c

authorized_mpsks: authorized_c authorized_mpsks.json
	$(PODMAN) run --rm -i authorized_c -- authorized_mpsks < ./authorized_mpsks.json > raddb/authorized_mpsks

authorized_users: authorized_c authorized_users.json
	$(PODMAN) run --rm -i authorized_c -- authorized_users < ./authorized_users.json > raddb/authorized_users

update_user_hash: authorized_c authorized_users.json FORCE
	$(PODMAN) run --rm -i -v ./authorized_users.json:/authorized_users.json:rw,z authorized_c -- update_user_hash

FORCE:

all: authorized_mpsks