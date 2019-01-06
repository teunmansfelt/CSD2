
#include <iostream>
#include "saw.hpp"

Saw::Saw(int samplerate) : Saw(samplerate, 6) {}
Saw::Saw(int samplerate, int polyphony) : Oscillator(polyphony) {
  if(this->sine_count < 1) {
    this->wavetables[2] = new Saw_Wavetable(samplerate);
  }
  this->shape = 2;
  this->saw_count += 1;
  this->set_polyphony(polyphony);
}

Saw::~Saw() {}
