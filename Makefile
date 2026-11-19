.PHONY: all firmware daemon clean

all: firmware daemon

firmware:
	$(MAKE) -C firmware

daemon:
	$(MAKE) -C daemon

clean:
	$(MAKE) -C firmware clean
	$(MAKE) -C daemon clean
