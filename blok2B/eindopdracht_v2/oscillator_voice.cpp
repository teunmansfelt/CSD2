
#include <iostream>
#include <math.h>
#include "oscillator_voice.hpp"

Oscillator_Voice::Oscillator_Voice(Wavetable* wavetable_p) : Voice(wavetable_p) {
  this->frequency = 0;
  this->amplitude = 1;
  this->pitch_multiplier = 1;
  this->phase_offset = 0;
}

Oscillator_Voice::~Oscillator_Voice() {}

//-- Sample Playback --//
void Oscillator_Voice::tick() {
  this->wavetable_position += 2 * this->frequency;
  this->sample += int(2 * this->frequency);

  if(this->wavetable_position >= this->wavetable_length) {
    this->wavetable_position -= this->wavetable_length;
    this->sample -= this->wavetable_length;
  }
}

double Oscillator_Voice::get_sample_L() {
  return *this->sample * this->channel_multiplier_L;
}

double Oscillator_Voice::get_sample_R() {
  return *this->sample * this->channel_multiplier_R;
}

//-- Channel Multiplier Calculation --//
void Oscillator_Voice::calculate_channel_multipliers(double velocity) {
  this->channel_multiplier_L = this->amplitude * this->pan_factor_L * velocity;
  this->channel_multiplier_R = this->amplitude * this->pan_factor_R * velocity;
}

//-- Phase reset --//
void Oscillator_Voice::reset_wavetable() {
  this->wavetable_position = this->phase_offset;
  this->sample = this->wavetable_p->get_wavetable_address();
  this->sample += this->phase_offset;
}

//-- Setters --//
void Oscillator_Voice::set_panning(float panning) {
  this->pan_factor_L = cos((panning + 1) * QUARTER_PI);
  this->pan_factor_R = sin((panning + 1) * QUARTER_PI);
  std::cout << "Oscillator_Voice pan L: " << this->pan_factor_L << "   R: "<< this->pan_factor_R << std::endl;
}

void Oscillator_Voice::set_frequency(float frequency) {
  this->frequency = floor(frequency * 2 * this->pitch_multiplier) * 0.5;
  std::cout << "Oscillator_Voice freq in: " << frequency << "   Oscillator_Voice freq: " << this->frequency << std::endl;
}

void Oscillator_Voice::set_amplitude(double amplitude) {
  this->amplitude = amplitude;
  std::cout << "Oscillator_Voice amp: " << this->amplitude << std::endl;
}

void Oscillator_Voice::set_pitch_offset(float offset, int direction) {
  if(direction == 0) {
    this->pitch_multiplier = 1 + offset;
  } else if(direction == 1) {
    this->pitch_multiplier = 1 / (1 + offset);
  }
  std::cout << "Oscillator_Voice pitch_mult: " << this->pitch_multiplier << std::endl;
}

void Oscillator_Voice::set_phase_offset(float phase_offset) {
  this->phase_offset = floor(fmod(phase_offset, 1) * this->wavetable_length);
}
