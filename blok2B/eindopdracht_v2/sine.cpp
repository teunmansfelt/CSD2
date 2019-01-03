
#include <iostream>
#include <vector>
#include "sine.hpp"
// #include "sine_wavetable.hpp"

Sine::Sine(int samplerate) : Sine(samplerate, 6) {}
Sine::Sine(int samplerate, int polyphony) : Oscillator(polyphony) {
  std::cout << "Sine - Constructor" << std::endl;
  *this->wavetable = Sine_Wavetable(samplerate);
}

Sine::~Sine() {}
