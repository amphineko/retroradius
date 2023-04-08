PODMAN := $(shell which podman 2>/dev/null)

.PHONY: all

authorized_mpsks_c: utils/authorized_mpsks_c/compiler.py utils/authorized_mpsks_c/Containerfile utils/authorized_mpsks_c/template.j2
	$(PODMAN) build -t authorized_mpsks_c -f utils/authorized_mpsks_c/Containerfile utils/authorized_mpsks_c

authorized_mpsks: authorized_mpsks_c authorized_mpsks.json
	$(PODMAN) run --rm -i authorized_mpsks_c < ./authorized_mpsks.json > raddb/authorized_mpsks

all: authorized_mpsks