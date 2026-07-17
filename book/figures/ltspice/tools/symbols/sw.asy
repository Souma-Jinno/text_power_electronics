Version 4
SymbolType CELL
LINE Normal 32 0 32 32
LINE Normal 32 32 20 58
LINE Normal 32 64 32 96
CIRCLE Normal 30 30 34 34
CIRCLE Normal 30 62 34 66
LINE Normal 0 32 20 32
LINE Normal 0 64 20 64
WINDOW 0 40 8 Left 2
WINDOW 3 40 80 Left 2
SYMATTR Prefix S
SYMATTR Description Voltage-controlled switch, pins: N+(top) N-(bottom) NC+(upper-left control) NC-(lower-left control); open-blade artwork (chapter figure symbol, custom-drawn, not a copy of the real LTspice SW artwork). Value field holds the .model name (e.g. SW). Control pins are meant to be driven via matching net-name FLAGs (see corpus prof_00_boost.asc convention), not a direct wire.
PIN 32 0 NONE 0
PINATTR PinName N+
PIN 32 96 NONE 0
PINATTR PinName N-
PIN 0 32 NONE 0
PINATTR PinName NC+
PIN 0 64 NONE 0
PINATTR PinName NC-
