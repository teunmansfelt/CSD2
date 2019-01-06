
#include <iostream>
#include <math.h>
#include "voice.hpp"

Voice::Voice(Wavetable* wavetable_p) {
  this->wavetable_p = wavetable_p;
  this->sample = this->wavetable_p->get_wavetable_address();
  this->wavetable_length = this->wavetable_p->get_wavetable_length();
  this->wavetable_position = 0;
}

Voice::~Voice() {}
