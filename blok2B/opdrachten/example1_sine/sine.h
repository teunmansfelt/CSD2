#ifndef _SINE_H_
#define _SINE_H_
#include <iostream>
#include "math.h"
#include "oscillator.h"

#define PI_2 6.28318530717959


class Sine : public Oscillator
{
public:
  //Constructor and destructor
  Sine(double samplerate, double frequency);
  ~Sine();

  // override calculate method
  void calculate();


};

#endif
