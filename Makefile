.PHONY: build test serve

build:
	pip3 install pytest -U

test:
	py.test tests/
	nginx -t -c `pwd`/conf/nginx.conf

serve:
	nginx -c `pwd`/conf/nginx.conf

stop:
	nginx -c `pwd`/conf/nginx.conf -s stop