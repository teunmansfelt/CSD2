#ifndef SQUARE_H
#define SQUARE_H
#include <iostream>
#include "math.h"
#include "pulse.h"

#define PI_2 6.28318530717959


class Square : public Pulse
{
public:
  //Constructor and destructor
  Square(double samplerate, double frequency);
  ~Square();

};

#endif
