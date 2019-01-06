
#ifndef SAW_WAVETABLE_H
#define SAW_WAVETABLE_H

#include <iostream>
#include "wavetable.hpp"

#define PI_2 6.28318530717959

class Saw_Wavetable : public Wavetable {
public:
  Saw_Wavetable(int samplerate);
  ~Saw_Wavetable();
};

#endif
