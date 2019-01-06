
#include <iostream>
#include "oscillator.hpp"

Oscillator::Oscillator(int polyphony) {
  this->polyphony = 0;
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

double Oscillator::get_sample_L(int voice_index) {
  return this->voice_clusters[voice_index]->get_sample_L();
}

double Oscillator::get_sample_R(int voice_index) {
  return this->voice_clusters[voice_index]->get_sample_L();
}

void Oscillator::set_polyphony(int polyphony) {
  Wavetable* wavetable_p = this->wavetables[this->shape];
  if(polyphony < 1) {
    for(int i = this->polyphony - 1; i >= 1; i--) {
      delete this->voice_clusters[i];
    }
  } else if(polyphony > 9) {
    for(int i = this->polyphony; i < 9; i++) {
      this->voice_clusters[i] = new Voice_Cluster(
        wavetable_p,
        this->unison_voices,
        this->unison_pitch,
        this->unison_panning,
        this->unison_phase,
        this->unison_blend
      );
    }
  } else {
    int voices_to_add = polyphony - this->polyphony;
    if(voices_to_add == 0) {
      return;
    } else if(voices_to_add > 0) {
      for(int i = this->polyphony; i < polyphony; i++) {
        this->voice_clusters[i] = new Voice_Cluster(
          wavetable_p,
          this->unison_voices,
          this->unison_pitch,
          this->unison_panning,
          this->unison_phase,
          this->unison_blend
        );
      }
    } else if(voices_to_add < 0) {
      for(int i = this->polyphony - 1; i >= polyphony; i--) {
        delete this->voice_clusters[i];
      }
    }
  }
  this->polyphony = polyphony;
}


void Oscillator::play_tone(float frequency, double velocity) {
  this->voice_clusters[0]->set_note(frequency, velocity);
}

void Oscillator::set_unison_voices(int number_of_voices) {
  this->unison_voices = number_of_voices;
  for(int i = 0; i < this->polyphony; i++) {
    this->voice_clusters[i]->set_number_of_voices(number_of_voices);
  }
}

void Oscillator::set_unison_pitch(float pitch_amount) {
  this->unison_pitch = pitch_amount;
  for(int i = 0; i < this->polyphony; i++) {
    this->voice_clusters[i]->set_unison_pitch(pitch_amount);
  }
}

void Oscillator::set_unison_panning(float panning_amount) {
  this->unison_panning = panning_amount;
  for(int i = 0; i < this->polyphony; i++) {
    this->voice_clusters[i]->set_unison_panning(panning_amount);
  }
}

void Oscillator::set_unison_phase(float phase_amount) {
  this->unison_phase = phase_amount;
  for(int i = 0; i < this->polyphony; i++) {
    this->voice_clusters[i]->set_unison_phase(phase_amount);
  }
}

void Oscillator::set_unison_blend(float blend_amount) {
  this->unison_blend = blend_amount;
  for(int i = 0; i < this->polyphony; i++) {
    this->voice_clusters[i]->set_unison_blend(blend_amount);
  }
}
