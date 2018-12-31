
#include <iostream>
#include <vector>
#include "oscillator.hpp"
#include "voice_cluster.hpp"

Oscillator::Oscillator(int samplerate, int polyphony) {
  std::cout << "Oscillator - Constructor" << std::endl;
  this->samplerate = samplerate;

  Wavetable* wavetable_pointer = &wavetable;
  for(int i = 0; i < polyphony; i++) {
    voices.push_back(Voice_Cluster(wavetable_pointer));
  }
}

Oscillator::~Oscillator() {}
