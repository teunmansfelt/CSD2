
#include "envelope_wavetable.hpp"

Envelope_Wavetable::Envelope_Wavetable(int samplerate, float attack_, float decay_, double sustain_, float release_) :
  Wavetable(int(samplerate * (attack_ + decay_ + release_)) + 1) {
    this->wavetable = new double[this->wavetable_length];
    double* wavetable_p = this->wavetable;
    this->sustain = 1;

    int attack = int(samplerate * attack_);
    int decay = int(samplerate * decay_);
    int release = int(samplerate * release_);

    this->release_index = attack + decay;

    double attack_increment = 1 / double(attack + 1);
    double decay_decrement = 0;
    if(sustain_ < 1) {
      decay_decrement = 1 / double(1 - sustain_) * (decay + 1);
    }
    double release_decrement = 1 / double(release + 1);

    double sample = 0;

    for(int i = 0; i < this->wavetable_length; i++) {
      if(i <= attack) {
        sample += attack_increment;
      } else if(i <= this->release_index - 1) {
        sample -= decay_decrement;
      } else if(i == this->release_index) {
        sample = 1;
      } else if(i <= attack + decay + release) {
        sample -= release_decrement;
      } else {
        sample = 0;
      }
      *wavetable_p = sample;
    }
}

Envelope_Wavetable::~Envelope_Wavetable() {}
