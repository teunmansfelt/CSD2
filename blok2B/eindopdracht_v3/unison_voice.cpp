
#include <iostream>
#include "unison_voice.hpp"

Unison_Voice::Unison_Voice(Wavetable* wavetable_p, int unison_voices) : Voice(wavetable_p) {
  this->set_num_voices(unison_voices);
}

Unison_Voice::~Unison_Voice() {
  for(int i = 0; i < this->active_voices; i++) {
    delete this->voices[i];
  }
}

void Unison_Voice::tick() {
  for(int i = 0; i < this->active_voices; i++) {
    this->voices[i]->tick();
  }
}

void Unison_Voice::set_tick_step(int step, int step_offset) {
  int offset = 0.5 * (this->active_voices - 1) * -step_offset
  for(int i = 0; i < this->active_voices; i++) {
    this->voices[i]->set_tick_step(step, offset);
    offset += step_offset;
  }
}

double Unison_Voice::get_sample_L() {
  double sample = 0;
  for(int i = 0; i < this->active_voices; i++) {
    sample += this->voices[i]->get_sample_L();
  }
  return sample;
}

double Unison_Voice::get_sample_R() {
  double sample = 0;
  for(int i = 0; i < this->active_voices; i++) {
    sample += this->voices[i]->get_sample_R();
  }
  return sample;
}

void Unison_Voice::set_channel_multipliers(double multiplier_L, double multiplier_R) {
  for(int i = 0; i < this->active_voices; i++) {
    this->voices[i]->set_channel_multipliers(multiplier_L, multiplier_R);
  }
}

void Unison_Voice::set_num_voices(int number_of_voices) {
  if(number_of_voices < 1) {
    for(int i = this->active_voices - 1; i >= 1; i--) {
      delete this->voices[i];
    }
  } else if(number_of_voices > 9) {
    for(int i = this->active_voices; i < 9; i++) {
      this->init_voice(i);
    }
  } else {
    int voices_to_add = number_of_voices - this->active_voices;
    if(voices_to_add == 0) {
      return;
    } else if(voices_to_add > 0) {
      for(int i = this->active_voices; i < number_of_voices; i++) {
        this->init_voice(i);
      }
    } else if(voices_to_add < 0) {
      for(int i = this->active_voices - 1; i >= number_of_voices; i--) {
        delete this->voices[i];
      }
    }
  }
  this->active_voices = number_of_voices;
}

void Unison_Voice::reset_wavetable() {
  for(int i = 0; i < this->active_voices; i++) {
    this->voices[i]->reset_wavetable();
  }
}

void Unison_Voice::set_phase_offset(int offset) {
  int phase = offset;
  for(int i = 1; i < this->active_voices; i++) {
    this->voices[i]->set_phase_offset(phase);
    phase += offset;
  }
}
