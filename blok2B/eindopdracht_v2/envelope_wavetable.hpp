
#ifndef ENVELOPE_WAVETABLE_H
#define ENVELOPE_WAVETABLE_H

#include <iostream>
#include "wavetable.hpp"

class Envelope_Wavetable : public Wavetable {
public:
  Envelope_Wavetable(int samplerate, float attack, float decay, double sustain, float release);
  ~Envelope_Wavetable();

private:
  double sustain;
  int release_index;
};

#endif
