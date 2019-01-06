
#ifndef SQUARE_WAVETABLE_H
#define SQUARE_WAVETABLE_H

#include <iostream>
#include "wavetable.hpp"

#define PI_2 6.28318530717959

class Square_Wavetable : public Wavetable {
public:
  Square_Wavetable(int samplerate);
  ~Square_Wavetable();
};

#endif
