
#include <iostream>
#include <vector>
#include "wavetable.hpp"


Wavetable::Wavetable() {}

Wavetable::Wavetable(int samplerate) {
  std::cout << "Wavetable - Constructor " << samplerate << std::endl;
  this->wavetable_length = samplerate * 2;
}

Wavetable::~Wavetable() {
  std::cout << "Wavetable - Destructor " << std::endl;
}
