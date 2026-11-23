Element(0x00 "LM2596 / LM2596HVS Step-Down Module Upright 2x2 (200 mil pitch)" "VR101" "LM2596_UPRIGHT_2X2" 160 10 3 100 0x00)
(
	# 4 Pins in 2x2 grid with 200 mil (5.08 mm) spacing
	# Pin 1: IN+  (-100 mil, -100 mil) - Square pad
	Pin(-100 -100 66 20 76 38 "1" "1" 0x101)
	# Pin 2: IN-  (+100 mil, -100 mil) - Round pad
	Pin( 100 -100 66 20 76 38 "2" "2" 0x01)
	# Pin 3: OUT+ (-100 mil, +100 mil) - Round pad
	Pin(-100  100 66 20 76 38 "3" "3" 0x01)
	# Pin 4: OUT- (+100 mil, +100 mil) - Round pad
	Pin( 100  100 66 20 76 38 "4" "4" 0x01)

	# Module physical envelope when sitting upright (standing vertically along Y):
	# Length: 43.6 mm = 1716 mil (~1720 mil, Y = -860 to +860 mil)
	# Width (component envelope depth): ~13.5 mm = ~530 mil (X = -265 to +265 mil)
	ElementLine(-265 -860  265 -860 10)
	ElementLine( 265 -860  265  860 10)
	ElementLine( 265  860 -265  860 10)
	ElementLine(-265  860 -265 -860 10)

	# Module M3 mounting holes (3.2 mm = 126 mil diameter)
	# Top hole (near input): X = -120 mil, Y = -600 mil
	ElementArc(-120 -600 63 63 0 360 10)
	# Bottom hole (near output): X = +120 mil, Y = +600 mil
	ElementArc( 120  600 63 63 0 360 10)

	# Input Capacitor Cin (8mm dia = 315 mil) at top
	ElementArc(0 -700 150 150 0 360 8)

	# LM2596 IC TO-263-5 representation (upper-middle)
	ElementLine(-150 -450  150 -450 8)
	ElementLine( 150 -450  150 -250 8)
	ElementLine( 150 -250 -150 -250 8)
	ElementLine(-150 -250 -150 -450 8)

	# Inductor L1 marker (12mm x 12mm) in center
	ElementLine(-180 -180  180 -180 8)
	ElementLine( 180 -180  180  180 8)
	ElementLine( 180  180 -180  180 8)
	ElementLine(-180  180 -180 -180 8)

	# Trimmer Potentiometer marker (Bourns 3296W)
	ElementLine(-240 -350 -160 -350 8)
	ElementLine(-160 -350 -160 -50 8)
	ElementLine(-160 -50 -240 -50 8)
	ElementLine(-240 -50 -240 -350 8)
	ElementArc(-200 -300 20 20 0 360 8)

	# Output Capacitor Cout (8mm dia) at bottom
	ElementArc(0 700 150 150 0 360 8)

	# Pin 1 indicator dot
	ElementArc(-140 -140 20 20 0 360 8)

	Mark(0 0)
)
