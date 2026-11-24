.PHONY: all rev1.0 rev1.1 rev1.1a layout sziklai clean

all: rev1.0 rev1.1 rev1.1a layout sziklai

sziklai:
	lepton-netlist -g PCB -o fancontrol_sziklai.net fancontrol_sziklai.sch
	lepton-cli export -o sziklaiN.png sziklaiN.sch
	lepton-cli export -o fancontrol_sziklai.png fancontrol_sziklai.sch
	cp -f fancontrol_sziklai.png ../docs/fancontrol_sziklai_schematic.png
	cp -f sziklaiN.png ../docs/sziklaiN_subcircuit.png

rev1.0:
	cd rev1.0 && lepton-netlist -g PCB -o stripboard_rev1.0.net centro.sch lado1.sch lado2.sch
	cd rev1.0 && lepton-sch2pcb protoboard
	cd rev1.0 && lepton-cli export -o centro.png centro.sch
	cd rev1.0 && lepton-cli export -o lado1.png lado1.sch

rev1.1:
	cd rev1.1 && lepton-netlist -g PCB -o stripboard_rev1.1.net centro.sch lado1.sch lado2.sch interconnect.sch
	cd rev1.1 && lepton-sch2pcb protoboard
	cd rev1.1 && lepton-cli export -o centro.png centro.sch
	cd rev1.1 && lepton-cli export -o lado1.png lado1.sch
	cd rev1.1 && lepton-cli export -o lado2.png lado2.sch
	cd rev1.1 && lepton-cli export -o interconnect.png interconnect.sch

rev1.1a:
	cd rev1.1a && lepton-netlist -g PCB -o stripboard_rev1.1a.net centro.sch lado1.sch lado2.sch interconnect.sch
	cd rev1.1a && lepton-sch2pcb protoboard
	cd rev1.1a && lepton-cli export -o centro.png centro.sch
	cd rev1.1a && lepton-cli export -o lado1.png lado1.sch
	cd rev1.1a && lepton-cli export -o lado2.png lado2.sch
	cd rev1.1a && lepton-cli export -o interconnect.png interconnect.sch

layout:
	python3 layout_stripboards.py

clean:
	rm -f rev1.0/*.png rev1.0/*.bak rev1.0/*.new.pcb
	rm -f rev1.1/*.png rev1.1/*.bak rev1.1/*.new.pcb
	rm -f rev1.1a/*.png rev1.1a/*.bak rev1.1a/*.new.pcb
