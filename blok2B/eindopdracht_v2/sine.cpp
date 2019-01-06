
#include <iostream>
#include <vector>
#include "sine.hpp"

Sine::Sine(int samplerate) : Sine(samplerate, 6) {}
Sine::Sine(int samplerate, int polyphony) : Oscillator(polyphony) {
  std::cout << "Sine - Constructor" << std::endl;
  this->wavetable = new Sine_Wavetable(samplerate);
  this->init_voices();
}

Sine::~Sine() {}
