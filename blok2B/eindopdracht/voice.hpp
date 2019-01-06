
#ifndef VOICE_H
#define VOICE_H

#include "voice.hpp"

#include <iostream>

class Voice {
public:
  //-- Constructor Destructor--//
  Voice(double* wavetable, int wavetable_length);
  ~Voice();

private:
  double* wavetable;
  int wavetable_length;
}
