## Create 
DISTRO=AlmaLinux
ARCH=$(shell /bin/arch)

ifeq ($(VERSION.MAJOR), 9)
VERSION=9.4
PKGS=Packages
BASEOSPATH=$(BASENAME)/$(VERSION)/BaseOS/$(ARCH)/os/$(PKGS)/
APPSTREAMPATH=$(BASENAME)/$(VERSION)/AppStream/$(ARCH)/os/$(PKGS)/
DEVELPATH=$(BASENAME)/$(VERSION)/devel/$(ARCH)/os/$(PKGS)/
EXTRASPATH=$(BASENAME)/$(VERSION)/extras/$(ARCH)/os/$(PKGS)/
CRBPATH=$(BASENAME)/$(VERSION)/CRB/$(ARCH)/os/$(PKGS)/
EPELPATH=$(EPELNAME)/$(VERSION.MAJOR)/Everything/$(ARCH)/$(PKGS)/
endif

MIRRORURL=https://repo.almalinux.org
EPELMIRRORURL=http://mirror1.hs-esslingen.de/Mirrors
BASENAME=almalinux
EPELNAME=epel
