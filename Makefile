.PHONY: build test serve

build: deps serve

clean:
	#noop

deps:
	rm -rf ${HOME}/.virtualenv
	which python3
	virtualenv -p `which python3` "${HOME}/.virtualenv"
	pip3 install -U -r `pwd`/requirements.txt

test:
	py.test tests/
	nginx -t -c `pwd`/conf/nginx.conf

serve: stop
	rm -f /tmp/www
	ln -s `pwd`/www /tmp/www
	nginx -c `pwd`/conf/nginx.conf

stop:
	nginx -c `pwd`/conf/nginx.conf -s stop

reload:
	nginx -c `pwd`/conf/nginx.conf -s reload