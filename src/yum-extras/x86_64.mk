#ifeq ($(VERSION.MAJOR),5)
#REPORPMS += rpmforge-release-0.5.2-2.el5.rf.x86_64.rpm
#else
#REPORPMS += rpmforge-release-0.5.2-2.el6.rf.x86_64.rpm
#endif
# ROCKS8 - no rpmforge-release. rpmforge is obsolete.
ifeq ($(VERSION.MAJOR),8)
REPORPMS +=
endif
