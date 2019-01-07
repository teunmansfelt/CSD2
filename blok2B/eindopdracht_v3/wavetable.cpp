
#include <iostream>
#include "wavetable.hpp"

Wavetable::Wavetable(int samplerate) {
  this->wavetable_length = samplerate;
}

Wavetable::~Wavetable() {
  delete this->wavetable;
}

double* Wavetable::get_wavetable_address() {
  return this->wavetable;
}

int Wavetable::get_wavetable_length() {
  return this->wavetable_length;
}
