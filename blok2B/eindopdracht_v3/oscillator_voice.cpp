
#include <iostream>
#include "oscillator_voice.hpp"

Oscillator_Voice::Oscillator_Voice(Wavetable* wavetable_p) : Voice(wavetable_p) {
  this->sample = this->wavetable_p->get_wavetable_address();
  this->wavetable_length = this->wavetable_p->get_wavetable_length();
}

Oscillator_Voice::~Oscillator_Voice() {}

void Oscillator_Voice::tick() {
  this->wavetable_position += 2 * this->tick_step;
  this->sample += int(2 * this->tick_step);

  if(this->wavetable_position >= this->wavetable_length) {
    this->wavetable_position -= this->wavetable_length;
    this->sample -= this->wavetable_length;
  }
}

void Oscillator_Voice::set_tick_step(int step, int step_offset) {
  this->tick_step = (step + step_offset) * 2;
}

double Oscillator_Voice::get_sample_L() {
  return *this->sample * this->multiplier_L;
}

double Oscillator_Voice::get_sample_R() {
  return *this->sample * this->multiplier_R;
}

void Oscillator_Voice::reset_wavetable() {
  this->wavetable_position = this->phase_offset;
  this->sample = this->wavetable_p->get_wavetable_address();
  this->sample += this->phase_offset;
}

void Oscillator_Voice::set_channel_multipliers(double multiplier_L, double multiplier_R) {
  this->multiplier_L = multiplier_L;
  this->multiplier_R = multiplier_R;
}

void Oscillator_Voice::set_phase_offset(int offset) {
  this->phase_offset = offset;
}
