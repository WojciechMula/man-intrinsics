help:
	@echo "Available targets:"
	@echo "download - download .xml files"
	@echo "deb      - create a .deb package"
	@echo "rpm      - create an .rpm package"
	@echo
	@echo "Set MANOPTIONS variable to pass extra parameters for the man pages generator."

# --------------------------------------------------

# man pages are small (up to 7MB), better use a ramdisc 
TMPDIR=/dev/shm/
MKDIR=mkdir -p

DATA_XML=data-latest.xml
UOPS_XML=instructions.xml
XMLFILES=$(DATA_XML) $(UOPS_XML)

GENERATOR=./main.py $(MANOPTIONS) -g $(DATA_XML) -u $(UOPS_XML)

INTEL_DOWNLOAD_URL=https://software.intel.com/sites/landingpage/IntrinsicsGuide/files/$(DATA_XML)
UOPS_DOWNLOAD_URL=http://uops.info/$(UOPS_XML)

# --- common ---------------------------------------

download: $(XMLFILES)

$(DATA_XML):
	wget $(INTEL_DOWNLOAD_URL)

$(UOPS_XML):
	wget $(UOPS_DOWNLOAD_URL)

# --- deb ------------------------------------------

DEBROOTDIR=$(TMPDIR)/man-intrinsics
MANDIR=$(DEBROOTDIR)/usr/share/man/man7
DEBDIR=$(DEBROOTDIR)

deb: $(XMLFILES)
	$(MKDIR) $(MANDIR)
	$(GENERATOR) --gzip -o $(MANDIR) --deb $(DEBDIR)
	chmod 444 ${MANDIR}/*.7*
	dpkg-deb -b $(DEBDIR) .

# --- rpm ------------------------------------------

RPMROOTDIR=$(TMPDIR)/rpm
RPMDIRS=$(RPMROOTDIR)/BUILD\
        $(RPMROOTDIR)/BUILDROOT\
        $(RPMROOTDIR)/RPMS\
        $(RPMROOTDIR)/SOURCES\
        $(RPMROOTDIR)/SPECS\
        $(RPMROOTDIR)/SRPMS

OUTDIR=$(RPMROOTDIR)/BUILD

SPECNAME=man-intrinsics.spec
SPECDIR=.
SPECPATH=$(SPECDIR)/$(SPECNAME)

rpm: $(XMLFILES)
	$(MKDIR) $(RPMDIRS) $(OUTDIR)
	$(GENERATOR) --gzip --rpm-spec-dir=$(SPECDIR) -o $(OUTDIR)
	rpmbuild -bb $(SPECPATH) --define '_topdir ${RPMROOTDIR}'
	@find $(RPMDIRS) -name '*.rpm' -printf 'RPM path is "%p"\n'


# --- test ------------------------------------------

test: deb rpm

clean:
	find -name '*.pyc' -print -delete
