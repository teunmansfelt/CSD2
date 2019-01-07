
#include <iostream>
#include "oscillator.hpp"

Oscillator::Oscillator() : Signal_Generator() {}

Oscillator::~Oscillator() {}

double Oscillator::get_sample_L() {
  double sample = 0;
  for(int i = 0; i < this->active_voices; i++) {
    sample += this->voices[i]->get_sample_L();
  }
  return sample / this->active_voices; //remove devision
}

double Oscillator::get_sample_R() {
  double sample = 0;
  for(int i = 0; i < this->active_voices; i++) {
    sample += this->voices[i]->get_sample_R();
  }
  return sample / this->active_voices; //remove devision
}

void Oscillator::set_note(int voice_index, float frequency, double velocity) {
  this->voices[voice_index]->set_frequency(frequency);
}

// void Oscillator::set_channel_multipliers(int voice_index, double multiplier_L, double multiplier_R) {
//   this->voices[voice_index]->set_channel_multipliers(multiplier_L, multiplier_R);
// }
