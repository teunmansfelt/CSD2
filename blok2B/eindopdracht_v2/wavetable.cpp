
#include <iostream>
#include "wavetable.hpp"

Wavetable::Wavetable(int samplerate) {
  std::cout << "Wavetable - Constructor " << samplerate << std::endl;
  this->wavetable_length = samplerate * 2;
}

Wavetable::~Wavetable() {
  std::cout << "Wavetable - Destructor " << std::endl;
}

double* Wavetable::get_wavetable_address() {
  return this->wavetable;
}

int Wavetable::get_wavetable_length() {
  return this->wavetable_length;
}
