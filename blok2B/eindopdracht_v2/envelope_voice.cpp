
#include <iostream>
#include "envelope_voice.hpp"

Envelope_Voice::Envelope_Voice(Wavetable* wavetable_p) : Voice(wavetable_p) {}

Envelope_Voice::~Envelope_Voice() {}

void Envelope_Voice::tick() {
  if(this->wavetable_position < this->wavetable_length) {
    this->wavetable_position += 1;
    this->sample++;
  }
}

double Envelope_Voice::get_sample() {
  return *this->sample;
}

void Envelope_Voice::reset_wavetable() {
  this->wavetable_position = 0;
  this->sample = this->wavetable_p->get_wavetable_address();
}
