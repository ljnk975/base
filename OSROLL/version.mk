## Create 
DISTRO=Rocky
ARCH=$(shell /bin/arch)

ifeq ($(VERSION.MAJOR), 8)
VERSION=8.9
PKGS=Packages
BASEOSPATH=$(BASENAME)/$(VERSION)/BaseOS/$(ARCH)/os/$(PKGS)/
APPSTREAMPATH=$(BASENAME)/$(VERSION)/AppStream/$(ARCH)/os/$(PKGS)/
DEVELPATH=$(BASENAME)/$(VERSION)/Devel/$(ARCH)/os/$(PKGS)/
EXTRASPATH=$(BASENAME)/$(VERSION)/extras/$(ARCH)/os/$(PKGS)/
POWERTOOLSPATH=$(BASENAME)/$(VERSION)/PowerTools/$(ARCH)/os/$(PKGS)/
EPELPATH=$(EPELNAME)/$(VERSION.MAJOR)/Everything/$(ARCH)/$(PKGS)/
endif

MIRRORURL=http://mirror1.hs-esslingen.de/Mirrors
BASENAME=rocky
EPELNAME=epel

#MIRRORURL=https://ftp.halifax.rwth-aachen.de
#BASENAME=rockylinux
#EPELNAME=fedora-epel

#UPDATESPATH=centos/$(VERSION)/updates/$(ARCH)/$(PKGS)/
#KERNELPATH=centos-altarch/$(VERSION)/experimental/$(ARCH)/$(PKGS)/
#ROLLNAME=CentOS-$(VERSION)-Updated
