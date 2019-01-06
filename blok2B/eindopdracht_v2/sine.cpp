
#include <iostream>
#include "sine.hpp"

Sine::Sine(int samplerate) : Sine(samplerate, 6) {}
Sine::Sine(int samplerate, int polyphony) : Oscillator(polyphony) {
  if(this->sine_count < 1) {
    this->wavetables[0] = new Sine_Wavetable(samplerate);
  }
  std::cout << this->wavetables[0]->get_wavetable_length() << std::endl;
  this->shape = 0;
  this->sine_count += 1;
  std::cout << this->sine_count << std::endl;
  this->set_polyphony(polyphony);
}

Sine::~Sine() {
  this->sine_count -= 1;
  if(this->sine_count) {
    delete this->wavetables[0];
  }
}
