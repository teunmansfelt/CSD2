
#include "string_instrument.hpp"

#include <iostream>

int main() {

	// Note_Converter note_converter();

	std::array<int,2> vioolRange {{0, 10}};
	String_Instrument viool("viool", "vioolGeluid", vioolRange);

	viool.play("C3");

	return 0;
}
