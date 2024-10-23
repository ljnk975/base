# Makefile to create an OS Roll and Updates
# $Id: Makefile,v 1.5 2012/10/04 16:52:58 clem Exp $
# $Log: Makefile,v $
# Revision 1.5  2012/10/04 16:52:58  clem
# Now properly deletes downloaded files to save disk space
#
# Signed-off-by: Luca Clementi <luca.clementi@gmail.com>
#
# Revision 1.4  2012/04/24 00:06:20  clem
# Delete mirrored data after creation of roll
#
# Revision 1.3  2012/02/24 02:01:53  clem
# os roll and update roll was always built for 6.2 (now it build also for 5.7)
#
# Revision 1.2  2011/11/11 06:00:24  phil
# Updated anaconda to RHEL 5.7 base
#
# Revision 1.1  2011/11/02 16:43:38  phil
# In bootstrap0, create an OS and Updates roll after the Rocks database is up and running.
#

SHELL = /bin/bash
DATEFMT =  $(shell date +%F)
TIMEFMT =  $(shell date +%T)
ZONEFMT =  $(shell date +%Z)
#needs this to include proper version number
-include $(ROLLSROOT)/etc/Rolls.mk

.PHONY : baseos appstream updated-dist updated-iso rebuild-iso roll-$(DISTRO)-$(VERSION)-update.xml

include version.mk

WORKDIR = /tmp/ALMAROLL
default: baseos appstream devel extras crb 

# Create the AlmaLinux BaseOS Roll
baseos: workdir
	( cd $(WORKDIR);\
	/opt/rocks/bin/rocks create mirror $(MIRRORURL)/$(BASEOSPATH) arch=$(ARCH) rollname=$(DISTRO)-BaseOS-$(VERSION) version="`date +%F`" )
	/opt/rocks/bin/rocks add roll $(WORKDIR)/$(DISTRO)-BaseOS-$(VERSION)-*.$(ARCH).*.iso
	/opt/rocks/bin/rocks enable roll $(DISTRO)-BaseOS-$(VERSION)
	- rm -rf `readlink -f $(WORKDIR)/$(subst http://,,$(MIRRORURL))/$(BASEOSPATH)/../..`

# Create the AlmaLinux AppStream Roll
appstream: workdir
	(cd $(WORKDIR) ;\
	/opt/rocks/bin/rocks create mirror $(MIRRORURL)/$(APPSTREAMPATH) arch=$(ARCH) rollname=$(DISTRO)-AppStream-$(VERSION) version="`date +%F`" )
	/opt/rocks/bin/rocks add roll $(WORKDIR)/$(DISTRO)-AppStream-$(VERSION)-*.$(ARCH).*.iso
	/opt/rocks/bin/rocks enable roll $(DISTRO)-AppStream-$(VERSION)
	- rm -rf `readlink -f $(WORKDIR)/$(subst http://,,$(MIRRORURL))/$(APPSTREAMPATH)/../..`

# Create the AlmaLinux Devel Roll
devel: workdir
	( cd $(WORKDIR);\
	/opt/rocks/bin/rocks create mirror $(MIRRORURL)/$(DEVELPATH) arch=$(ARCH) rollname=$(DISTRO)-Devel-$(VERSION) version="`date +%F`" )
	/opt/rocks/bin/rocks add roll $(WORKDIR)/$(DISTRO)-Devel-$(VERSION)-*.$(ARCH).*.iso
	/opt/rocks/bin/rocks enable roll $(DISTRO)-Devel-$(VERSION)
	- rm -rf `readlink -f $(WORKDIR)/$(subst http://,,$(MIRRORURL))/$(DEVELPATH)/../..`

# Create the AlmaLinux extras Roll
extras: workdir
	( cd $(WORKDIR);\
	/opt/rocks/bin/rocks create mirror $(MIRRORURL)/$(EXTRASPATH) arch=$(ARCH) rollname=$(DISTRO)-Extras-$(VERSION) version="`date +%F`" )
	/opt/rocks/bin/rocks add roll $(WORKDIR)/$(DISTRO)-Extras-$(VERSION)-*.$(ARCH).*.iso
	/opt/rocks/bin/rocks enable roll $(DISTRO)-Extras-$(VERSION)
	- rm -rf `readlink -f $(WORKDIR)/$(subst http://,,$(MIRRORURL))/$(EXTRASPATH)/../..`

# Create the AlmaLinux PowerTools Roll
crb: workdir
	(cd $(WORKDIR) ;\
	/opt/rocks/bin/rocks create mirror $(MIRRORURL)/$(CRBPATH) arch=$(ARCH) rollname=$(DISTRO)-CRB-$(VERSION) version="`date +%F`" )
	/opt/rocks/bin/rocks add roll $(WORKDIR)/$(DISTRO)-CRB-$(VERSION)-*.$(ARCH).*.iso
	/opt/rocks/bin/rocks enable roll $(DISTRO)-CRB-$(VERSION)
	- rm -rf `readlink -f $(WORKDIR)/$(subst http://,,$(MIRRORURL))/$(CRBPATH)/../..`

# Create the (optional) Extra Packages for Enterprise Linux (EPEL) Roll
epel: workdir
	(cd $(WORKDIR) ;\
	/opt/rocks/bin/rocks create mirror $(EPELMIRRORURL)/$(EPELPATH) arch=$(ARCH) rollname=EPEL-$(VERSION.MAJOR) version="`date +%F`" )
	/opt/rocks/bin/rocks add roll $(WORKDIR)/EPEL-$(VERSION.MAJOR)-*.$(ARCH).*.iso
	/opt/rocks/bin/rocks enable roll EPEL-$(VERSION.MAJOR)
	- rm -rf `readlink -f $(WORKDIR)/$(subst http://,,$(EPELMIRRORURL))/$(EPELPATH)/../..`

# Create the XML for creating an joint BaseOS / AppStream roll
# FIXME - Shall we join BaseOS and AppStream as default?
roll-$(DISTRO)-$(VERSION)-update.xml:
	sed -e 's/@DISTRO@/$(DISTRO)/g' -e 's/@VERSION@/$(VERSION)/g' -e 's/@DATE@/$(DATEFMT)/g' roll-distro-update.xml.in > roll-$(DISTRO)-$(VERSION)-update.xml 

# Create the updated distro
updated-dist: roll-$(DISTRO)-$(VERSION)-update.xml
	if [ -d rocks-dist ]; then /bin/rm -rf rocks-dist; fi
	rocks create distro rolls="$(DISTRO)-BaseOS-$(VERSION),$(DATEFMT) $(DISTRO)-Appstream-$(VERSION),$(DATEFMT)" 

## This mirrors the OS baseos and and appstream, creates a distro based upon those and then creates
## an ISO 
updated-iso: baseos appstream updated-dist rebuild-iso
	echo "This is is the full mirror and build"

## This rebuilds the updated-iso and assumes that baseos, appstream rolls are already downloaded and
## in the distro
rebuild-iso: updated-dist
	(cd rocks-dist/$(ARCH)/RedHat; \
	 rocks create roll ../../../roll-$(DISTRO)-$(VERSION)-update.xml; \
	 mv *iso ../../.. )

# Remove All Previous Appstream Rolls
cleanappstream: workdir
#	- /sbin/service httpd stop
	- /opt/rocks/bin/rocks disable roll $(DISTRO)-AppStream-$(VERSION) arch=$(ARCH)
	- /opt/rocks/bin/rocks remove roll $(DISTRO)-AppStream-$(VERSION) arch=$(ARCH)
	- /bin/rm $(WORKDIR)/$(DISTRO)-AppStream-$(VERSION)-*.$(ARCH).*.iso
#	- /sbin/service httpd start

workdir:
	if [ ! -d $(WORKDIR) ]; then mkdir -p $(WORKDIR); fi

clean:: workdir
	/bin/rm $(WORKDIR)/*iso
	/bin/rm roll-$(DISTRO)-$(VERSION)-update.xml

testing:
	echo "arch is " $(ARCH)
