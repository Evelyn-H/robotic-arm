default: %.so

%.so: setup.py clib.pyx
	make -C clib
	python3 setup.py build_ext --inplace && rm -f clib.c && rm -Rf build

clean:
	rm *.so
