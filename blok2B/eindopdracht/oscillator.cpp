
#include "oscillator.hpp"

#include <iostream>
#include <array>

//-- Constructor --//
Oscillator::Oscillator(int samplerate, float frequency, float phase, double amplitude) {
  wavetable_length = samplerate * 2;
  reset_phase();
  this->frequency = frequency;
  this->amplitude = amplitude;
  this->samplerate = samplerate;
  new_amplitude = false;
}

//-- Destructor --//
Oscillator::~Oscillator() {
  std::cout << "~Oscillator" << std::endl;
  delete wavetable;
}

//-- Sample --//
void Oscillator::tick() {
  wavetable_position += frequency * 2;
  wavetable_position = wavetable_position % wavetable_length;

  if(new_amplitude) {
    if(next_amplitude - amplitude > 0) {
      amplitude += 0.005;
      if(amplitude >= next_amplitude) {
        amplitude = next_amplitude;
        new_amplitude = false;
      }
    } else {
      amplitude -= 0.005;
      if(amplitude <= next_amplitude) {
        amplitude = next_amplitude;
        new_amplitude = false;
      }
    }
  }
}

void Oscillator::reset_phase() {
  wavetable_position = int(phase * wavetable_length);
}

//-- Setters --//
void Oscillator::set_frequency(float frequency) {
  if(frequency > 0 && frequency < 0.5 * samplerate) {
    this->frequency = frequency;
  }
}
void Oscillator::set_amplitude(double amplitude) {
  next_amplitude = amplitude;
  new_amplitude = true;
}

// -- Getters -- //
double Oscillator::get_sample() { return wavetable[wavetable_position] * amplitude; }

float Oscillator::get_frequency() { return frequency; }
