
#ifndef SQUARE_H
#define SQUARE_H

#include <iostream>
#include "oscillator.hpp"
#include "square_wavetable.hpp"

class Square : public Oscillator{
public:
  Square(int samplerate);
  Square(int samplerate, int polyphony);
  ~Square();

  Square() = delete;
};

#endif
