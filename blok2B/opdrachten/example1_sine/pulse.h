#ifndef PULSE_H
#define PULSE_H
#include <iostream>
#include "math.h"
#include "oscillator.h"

#define PI_2 6.28318530717959


class Pulse : public Oscillator
{
public:
  //Constructor and destructor
  Pulse(double samplerate, double frequency, double pulse_width);
  ~Pulse();

  // override calculate method
  void calculate();

private:
  double pulse_width;
};

#endif
