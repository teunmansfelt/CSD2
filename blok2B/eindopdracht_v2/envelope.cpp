
#include <iostream>
#include "envelope.hpp"

Envelope::Envelope(int samplerate, int polyphony) : Envelope(samplerate, polyphony, 0, 0.500, 1, 0) {}

Envelope::Envelope(int samplerate, int polyphony, float attack, float decay, double sustain, float release) {
  this->wavetable = new Envelope_Wavetable(samplerate, attack, decay, sustain, release);
  this->polyphony = polyphony;
}

Envelope::~Envelope() {
  delete this->wavetable;
  for(int i = 0; i < this->polyphony; i++) {
    delete this->voices[i];
  }
}

void Envelope::tick() {
  for(int i = 0; i < this->polyphony; i++) {
    this->voices[i]->tick();
  }
}

double Envelope::get_sample(int voice_index) {
  return this->voices[voice_index]->get_sample();
}

void Envelope::set_polyphony(int polyphony) {
  Wavetable* wavetable_p = this->wavetable;
  if(polyphony < 1) {
    for(int i = this->polyphony - 1; i >= 1; i--) {
      delete this->voices[i];
    }
  } else if(polyphony > 9) {
    for(int i = this->polyphony; i < 9; i++) {
      this->voices[i] = new Envelope_Voice(wavetable_p);
    }
  } else {
    int voices_to_add = polyphony - this->polyphony;
    if(voices_to_add == 0) {
      return;
    } else if(voices_to_add > 0) {
      for(int i = this->polyphony; i < polyphony; i++) {
        this->voices[i] = new Envelope_Voice(wavetable_p);
      }
    } else if(voices_to_add < 0) {
      for(int i = this->polyphony - 1; i >= polyphony; i--) {
        delete this->voices[i];
      }
    }
  }
  this->polyphony = polyphony;
}
