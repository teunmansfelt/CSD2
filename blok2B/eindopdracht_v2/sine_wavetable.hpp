
#ifndef SINE_WAVETABLE_H
#define SINE_WAVETABLE_H

#include <iostream>
#include "wavetable.hpp"

#define PI_2 6.28318530717959

class Sine_Wavetable : public Wavetable {
public:
  Sine_Wavetable(int samplerate);
  ~Sine_Wavetable();

  Sine_Wavetable();

private:
  void calculate_wavetable() override;
};

#endif
