
#ifndef VOICE_H
#define VOICE_H

#include <iostream>
#include "wavetable.hpp"

class Voice {
public:
  Voice(Wavetable** wavetable);
  ~Voice();

  void tick();
  double get_sample_L();
  double get_sample_R();

private:
  Wavetable** wavetable;
};

#endif
