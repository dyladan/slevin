BOOKIE := https://github.com/bookieio/bookie.git
REPO := bookie
SYSDEPS := git python-virtualenv

.PHONY: clean
clean:
	rm -rf bin bookie include lib local

.PHONY: run
run:
	bin/python bot.py

.PHONY: setup
setup:
	if [ ! -d $(REPO) ]; then\
		git clone $(BOOKIE) $(REPO);\
	fi
	virtualenv -p python2 .
	bin/pip install -r requirements.txt

.PHONY: sysdeps
sysdeps:
	if [ $(NONINTERACTIVE) ]; then\
		sudo apt-get install -y $(SYSDEPS);\
	else \
		sudo apt-get install $(SYSDEPS); \
	fi
