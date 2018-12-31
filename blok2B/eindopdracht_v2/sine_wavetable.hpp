
#ifndef SINE_WAVETABLE_H
#define SINE_WAVETABLE_H

#include <iostream>
#include "wavetable.hpp"

class Sine_Wavetable : public Wavetable {
public:
  Sine_Wavetable(int samplerate);
  ~Sine_Wavetable();

  Sine_Wavetable();
};

#endif
