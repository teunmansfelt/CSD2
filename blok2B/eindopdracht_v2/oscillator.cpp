
#include <iostream>
#include <array>
#include "oscillator.hpp"
#include "voice_cluster.hpp"

Oscillator::Oscillator(int polyphony) {
  std::cout << "Oscillator - Constructor" << std::endl;
  this->polyphony = polyphony;

  Wavetable** wavetable_pointer = &this->wavetable;
  for(int i = 0; i < this->polyphony; i++) {
    this->voice_clusters[i] = new Voice_Cluster(wavetable_pointer);
  };
}

Oscillator::~Oscillator() {
  for(int i = 0; i < this->polyphony; i++) {
    delete this->voice_clusters[i];
  }
}

double Oscillator::get_sample_L() {
  double sample = 0;
  for(int i = 0; i < this->active_voices; i++) {
    sample += this->voices[i]->get_sample_L();
  }
  return sample / double(this->active_voices);
}

double Oscillator::get_sample_R() {
  double sample = 0;
  for(int i = 0; i < this->active_voices; i++) {
    sample += this->voices[i]->get_sample_R();
  }
  return sample / double(this->active_voices);
}
