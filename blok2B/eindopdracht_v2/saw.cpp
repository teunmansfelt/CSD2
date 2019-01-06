
#include <iostream>
#include <vector>
#include "saw.hpp"

Saw::Saw(int samplerate) : Saw(samplerate, 6) {}
Saw::Saw(int samplerate, int polyphony) : Oscillator(polyphony) {
  std::cout << "Saw - Constructor" << std::endl;
  this->wavetable = new Saw_Wavetable(samplerate);
  this->init_voices();
}

Saw::~Saw() {}
