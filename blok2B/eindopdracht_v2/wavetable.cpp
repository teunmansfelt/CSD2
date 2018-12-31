
#include <iostream>
#include <vector>
#include "wavetable.hpp"

Wavetable::Wavetable(int samplerate) {
  std::cout << "Wavetable - Constructor " << samplerate << std::endl;
}

Wavetable::Wavetable() {
  std::cout << "Wavetable - def_Constructor " << std::endl;
}

Wavetable::~Wavetable() {}
