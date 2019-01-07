
#ifndef VOICE_H
#define VOICE_H

#include <iostream>
#include "wavetable.hpp"

class Voice {
public:
  Voice(Wavetable* wavetable_p);
  ~Voice();
// protected:
//   Voice(Wavetable* wavetable_p);
//   virtual ~Voice();

  void tick(); //later virtual
  double get_sample_L();
  double get_sample_R();

  void set_frequency(float frequency);

private:
  Wavetable* wavetable_p; //pointer to the wavetable_object of the oscillator.
  double* sample; //pointer to actual wavetable_array.
  int wavetable_position; //sample_position in the wavetable_array.
  int wavetable_length; //length of the wavetable_array.

  float frequency;
};

#endif
