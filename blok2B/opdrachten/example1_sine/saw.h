#ifndef SAW_H
#define SAW_H
#include <iostream>
#include "math.h"
#include "oscillator.h"

#define PI_2 6.28318530717959


class Saw : public Oscillator
{
public:
  //Constructor and destructor
  Saw(double samplerate, double frequency);
  ~Saw();

  // override calculate method
  void calculate();

};

#endif
