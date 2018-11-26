
#include "instrument.h"

int main() {
	Instrument trompet("trompet", "BBWAAAHHP");
	Instrument drum("drum", "BOOM");
	Instrument piano("piano", "'pling'");

	trompet.roll(int(3));
	drum.roll(int(5));
	piano.roll(int(6));

	return 0;
}