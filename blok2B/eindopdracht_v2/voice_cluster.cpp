
#include <iostream>
#include <array>
#include <math.h>
#include "voice_cluster.hpp"

Voice_Cluster::Voice_Cluster(Wavetable* wavetable_p) {
  std::cout << "Voice_Cluster - Constructor " << wavetable_p << std::endl;
  this->wavetable_p = wavetable_p;
  this->voices[0] = new Voice(this->wavetable_p);
  this->active_voices = 1;
  this->active = false;
}

Voice_Cluster::~Voice_Cluster() {
  std::cout << "Voice_Cluster - Destructor " << this->active_voices << std::endl;
  for(int i = 0; i < this->active_voices; i++) {
    delete this->voices[i];
  }
}

void Voice_Cluster::tick() {
  for(int i = 0; i < this->active_voices; i++) {
    this->voices[i]->tick();
  }
}

double Voice_Cluster::get_sample_L() {
  double sample = 0;
  for(int i = 0; i < this->active_voices; i++) {
    sample += this->voices[i]->get_sample_L();
  }
  return sample / double(this->active_voices);
}

double Voice_Cluster::get_sample_R() {
  double sample = 0;
  for(int i = 0; i < this->active_voices; i++) {
    sample += this->voices[i]->get_sample_R();
  }
  return sample / double(this->active_voices);
}

void Voice_Cluster::set_note(float frequency, double velocity) {
  for(int i = 0; i < this->active_voices; i++) {
    this->voices[i]->calculate_channel_multipliers(velocity);
    this->voices[i]->set_frequency(frequency);
    this->voices[i]->reset_phase();
  }
}

void Voice_Cluster::set_number_of_voices(int number_of_voices) {
  if(number_of_voices < 1) {
    for(int i = 1; i < this->active_voices; i++) {
      delete this->voices[i];
    }
  } else if(number_of_voices > 9) {
    for(int i = this->active_voices; i < 9; i++) {
      this->voices[i] = new Voice(this->wavetable_p);
    }
  } else {
    int voices_to_add = number_of_voices - this->active_voices;
    if(voices_to_add == 0) {
      return;
    } else if(voices_to_add > 0) {
      for(int i = this->active_voices; i < number_of_voices; i++) {
        this->voices[i] = new Voice(this->wavetable_p);
      }
    } else if(voices_to_add < 0) {
      for(int i = this->active_voices - 1; i >= number_of_voices; i--) {
        delete this->voices[i];
      }
    }
  }
  this->active_voices = number_of_voices;
}

void Voice_Cluster::set_unison_pitch(float pitch_amount) {
  float offset_step = 0.2 / float(this->active_voices - 1);
  for(int i = 0; i < this->active_voices; i++) {
    float offset = (offset_step * floor((i + 1) * 0.5)) * pitch_amount;
    this->voices[i]->set_pitch_offset(offset, i % 2);
  }
}

void Voice_Cluster::set_unison_panning(float panning_amount) {
  float pan_step = 2 / float(this->active_voices - 1);
  for(int i = 0; i < this->active_voices; i++) {
    float panning = (pan_step * floor((i + 1) * 0.5)) * panning_amount;
    if(i % 2 == 0) {
      this->voices[i]->set_panning(panning);
    } else {
      this->voices[i]->set_panning(-panning);
    }
  }
}

void Voice_Cluster::set_unison_phase(float phase_amount) {
  float phase_step = 1 / float(this->active_voices);
  for(int i = 0; i < this->active_voices; i++) {
    float phase = phase_step * i * phase_amount;
    this->voices[i]->set_phase_offset(phase);
  }
}

void Voice_Cluster::set_unison_blend(float blend_amount) {
  for(int i = 0; i < this->active_voices; i++) {
    float amplitude = 1 - floor((i + 1) * 0.5) * (2 * (1 - blend_amount) / this->active_voices);
    this->voices[i]->set_amplitude(amplitude);
  }
}
