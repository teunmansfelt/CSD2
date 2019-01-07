
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

void Voice::tick() {
  this->wavetable_position += 2 * this->frequency;
  this->sample += int(2 * this->frequency);

  if(this->wavetable_position >= this->wavetable_length) {
    this->wavetable_position -= this->wavetable_length;
    this->sample -= this->wavetable_length;
  }
}

double Voice::get_sample_L() {
  return *this->sample;
}

double Voice::get_sample_R() {
  return *this->sample;
}

void Voice::set_frequency(float frequency) {
  this->frequency = frequency;
}
