# You may wish to run this file under poetry's virtual environment, like this:
#
# poetry run make

.DEFAULT_GOAL := mo
.PHONY: po mo clean


# Update .po files, used for translation
po:
	cd invitations && python ../manage.py makemessages -a --no-wrap

# Compile .mo files, used for translation
mo: po
	cd invitations && python ../manage.py compilemessages

# Clean files that are compiled by this Makefile
clean:
	rm -f invitations/locale/*/LC_MESSAGES/*.mo
