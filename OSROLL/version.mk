## Create 
DISTRO=CentOS
TSTARCH=$(shell /bin/arch)
ifeq ($(TSTARCH),i686)
ARCH=i386
else
ARCH=$(TSTARCH)
endif

ifeq ($(VERSION.MAJOR), 5)
VERSION=5.9
PKGS=RPMS
BASEPATH=centos/$(VERSION)/os/$(ARCH)/CentOS/
endif
ifeq ($(VERSION.MAJOR), 6)
VERSION=6.8
PKGS=Packages
BASEPATH=centos/$(VERSION)/os/$(ARCH)/$(PKGS)/
endif
ifeq ($(VERSION.MAJOR), 7)
VERSION=7.9.2009
PKGS=Packages
BASEPATH=centos/$(VERSION)/os/$(ARCH)/$(PKGS)/
endif

MIRRORURL=http://mirror1.hs-esslingen.de/Mirrors

UPDATESPATH=centos/$(VERSION)/updates/$(ARCH)/$(PKGS)/

KERNELPATH=centos-altarch/$(VERSION)/experimental/$(ARCH)/$(PKGS)/

ROLLNAME=CentOS-$(VERSION)-Updated
