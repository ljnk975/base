# $Id: Makefile,v 1.5 2012/11/27 00:48:39 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 6.2 (SideWinder)
# 		         version 7.0 (Manzanita)
# 
# Copyright (c) 2000 - 2017 The Regents of the University of California.
# All rights reserved.	
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
# 
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
# 
# 	"This product includes software developed by the Rocks(r)
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
# 
# 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
# neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
# the associated name, interested parties should contact Technology 
# Transfer & Intellectual Property Services, University of California, 
# San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
# Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# @Copyright@
#

REDHAT.ROOT = $(CURDIR)/../../
HTTPGET     = $(ROCKSROOT)/bin/httpget.sh
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk


build:
# ROCKS8 - bump to 1.4.0 (same as on Rocky8)
# Rocky supplied mosh is an EPEL-package -> need to build it here, EPEL is not part of OS rolls
# Link against OpenSSL lib from foundation-openssl-old
# https://src.fedoraproject.org/lookaside/extras/mosh/mosh-1.4.0.tar.gz/sha512/38c11f52ff1e42965b50a22bf6de80b0fa8ebbff841d825e760abf69c788a2bf5f34e6f7fc047574d595118334eef9edf8da5520b52cdde3ac1a79d7ad70312e/mosh-1.4.0.tar.gz
ifeq ($(shell ! test -f $(NAME)-$(VERSION).$(TARBALL_POSTFIX) && echo -n yes),yes)
	@echo "ROCKS8: Sideloading $(NAME)-$(VERSION).$(TARBALL_POSTFIX)."
	$(HTTPGET) -B https://src.fedoraproject.org -F lookaside/extras/mosh/mosh-1.4.0.tar.gz/sha512/38c11f52ff1e42965b50a22bf6de80b0fa8ebbff841d825e760abf69c788a2bf5f34e6f7fc047574d595118334eef9edf8da5520b52cdde3ac1a79d7ad70312e -n $(NAME)-$(VERSION).$(TARBALL_POSTFIX)
endif
	zcat $(NAME)-$(VERSION).$(TARBALL_POSTFIX) | $(TAR) -xf -
	( 							\
		cd $(NAME)-$(VERSION);				\
		PKG_CONFIG_PATH=/opt/rocks/lib/pkgconfig:$$PKG_CONFIG_PATH LDFLAGS="-ldl" ./configure  --prefix=$(PKGROOT);		\
		$(MAKE);					\
	)
	
install::
	mkdir -p $(ROOT)/$(PKGROOT)
	(							\
		cd $(NAME)-$(VERSION);				\
		$(MAKE) prefix=$(ROOT)/$(PKGROOT) install;	\
	)
clean::
	rm -rf $(NAME)-$(VERSION)
