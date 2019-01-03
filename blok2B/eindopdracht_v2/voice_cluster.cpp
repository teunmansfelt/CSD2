
#include <iostream>
#include <array>
#include "voice_cluster.hpp"

Voice_Cluster::Voice_Cluster(Wavetable** wavetable) {
  std::cout << "Voice_Cluster - Constructor " << wavetable << std::endl;
  this->voices[0] = new Voice(wavetable);
  this->wavetable = wavetable;
  this->active_voices = 1;
}

Voice_Cluster::~Voice_Cluster() {
  std::cout << "Voice_Cluster - Destructor " << this->active_voices << std::endl;
  for(int i = 0; i < this->active_voices; i++) {
    delete this->voices[i];
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

void Voice_Cluster::set_number_of_voices(int number_of_voices) {
  if(number_of_voices < 1) {
    for(int i = 1; i < this->active_voices; i++) {
      delete this->voices[i];
    }
  } else if(number_of_voices > 9) {
    for(int i = this->active_voices; i < 9; i++) {
      this->voices[i] = new Voice(this->wavetable);
    }
  } else {
    int voices_to_add = number_of_voices - this->active_voices;
    if(voices_to_add == 0) {
      return;
    } else if(voices_to_add > 0) {
      for(int i = this->active_voices; i < number_of_voices; i++) {
        this->voices[i] = new Voice(this->wavetable);
      }
    } else if(voices_to_add < 0) {
      for(int i = this->active_voices - 1; i >= number_of_voices; i--) {
        delete this->voices[i];
      }
    }
  }
  this->active_voices = number_of_voices;
}
