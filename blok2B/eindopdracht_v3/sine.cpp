
#include <iostream>
#include "sine.hpp"

Sine::Sine(int samplerate) : Sine(samplerate, 6) {}

Sine::Sine(int samplerate, int polyphony) : Oscillator() {
  if(this->instance_count < 1) {
    this->wavetable = new Sine_Wavetable(samplerate);
    this->wavetable_p = this->wavetable;
  }
  this->instance_count += 1;
  this->set_polyphony(polyphony);
}

Sine::~Sine() {
  this->instance_count -= 1;
  if(this->instance_count < 1) {
    delete this->wavetable;
    this->wavetable_p = NULL;
  }
}

void Sine::init_voice(int voice_index) {
  this->voices[voice_index] = new Voice(this->wavetable_p);
}
