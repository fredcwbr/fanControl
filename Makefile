.PHONY: all firmware daemon dashboard dashboard-c clean

all: firmware daemon dashboard-c

firmware:
	$(MAKE) -C firmware

daemon:
	$(MAKE) -C daemon

dashboard-c:
	$(MAKE) -C dashboard/tui_c

dashboard: dashboard-c
	./dashboard/run.sh

clean:
	$(MAKE) -C firmware clean
	$(MAKE) -C daemon clean
	$(MAKE) -C dashboard/tui_c clean
