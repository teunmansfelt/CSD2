
#include <iostream>
#include <array>
#include "oscillator.hpp"

Oscillator::Oscillator(int polyphony) {
  std::cout << "Oscillator - Constructor" << std::endl;
  this->polyphony = polyphony;
}

Oscillator::~Oscillator() {
  for(int i = 0; i < this->polyphony; i++) {
    delete this->voice_clusters[i];
  }
}

void Oscillator::tick() {
  for(int i = 0; i < this->polyphony; i++) {
    this->voice_clusters[i]->tick();
  }
}

double Oscillator::get_sample_L() {
  double sample = 0;
  for(int i = 0; i < this->polyphony; i++) {
    sample += this->voice_clusters[i]->get_sample_L();
  }
  return sample / double(this->polyphony);
}

double Oscillator::get_sample_R() {
  double sample = 0;
  for(int i = 0; i < this->polyphony; i++) {
    sample += this->voice_clusters[i]->get_sample_R();
  }
  return sample / double(this->polyphony);
}

void Oscillator::init_voices() {
  Wavetable* wavetable_p = this->wavetable;
  for(int i = 0; i < this->polyphony; i++) {
    this->voice_clusters[i] = new Voice_Cluster(wavetable_p);
  };
}

void Oscillator::play_tone(float frequency, double velocity) {
  this->voice_clusters[0]->set_note(frequency, velocity);
}

void Oscillator::set_unison_voices(int number_of_voices) {
  for(int i = 0; i < this->polyphony; i++) {
    this->voice_clusters[i]->set_number_of_voices(number_of_voices);
  }
}

void Oscillator::set_unison_pitch(float pitch_amount) {
  for(int i = 0; i < this->polyphony; i++) {
    this->voice_clusters[i]->set_unison_pitch(pitch_amount);
  }
}

void Oscillator::set_unison_panning(float panning_amount) {
  for(int i = 0; i < this->polyphony; i++) {
    this->voice_clusters[i]->set_unison_panning(panning_amount);
  }
}

void Oscillator::set_unison_phase(float phase_amount) {
  for(int i = 0; i < this->polyphony; i++) {
    this->voice_clusters[i]->set_unison_phase(phase_amount);
  }
}

void Oscillator::set_unison_blend(float blend_amount) {
  for(int i = 0; i < this->polyphony; i++) {
    this->voice_clusters[i]->set_unison_blend(blend_amount);
  }
}
