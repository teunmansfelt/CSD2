
#include "oscillator.hpp"
#include "voice_cluster.hpp"

#include <iostream>

//-- Constructor --//
Oscillator::Oscillator(int samplerate, double amplitude, int polyphony, int unison) {
  wavetable_length = samplerate * 2;
  this->samplerate = samplerate;
  this->amplitude = amplitude;
  this->polyphony = polyphony;
  this->unison = unison;

  std::cout << "Oscillator:   " << wavetable << std::endl;

  voices = new Voice_Cluster[polyphony];
  for(int i = 0; i < polyphony; i++) {
    voices[i].set_wavetable(wavetable);
  }
}

//-- Destructor --//
Oscillator::~Oscillator() {
  std::cout << "~Oscillator" << std::endl;
  delete wavetable;
  delete voices;
}

//-- Setters --//
void Oscillator::set_amplitude(double amplitude) {
  if(amplitude >= 0 && amplitude <= 1) {
    this->amplitude = amplitude;
  }
}

void Oscillator::set_polyphony(int number_of_voices) {
  delete voices;
  voices = new Voice_Cluster[number_of_voices];
  for(int i = 0; i < number_of_voices; i++) {
      voices[i].set_wavetable(wavetable);
  }
}

void Oscillator::set_unison(int number_of_unison_voices) {
  unison = number_of_unison_voices;
}
