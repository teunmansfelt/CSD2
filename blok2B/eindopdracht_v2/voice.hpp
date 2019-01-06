
#ifndef VOICE_H
#define VOICE_H

#include <iostream>
#include "wavetable.hpp"

class Voice {
protected:
//-- Constructor / Destructor --//
  Voice(Wavetable* wavetable_p);
  virtual ~Voice();

//-- Sample Playback --//
  virtual void tick() = 0;

//-- Reset phase --//
  virtual void reset_wavetable() = 0;

  Wavetable* wavetable_p; //pointer to the wavetable_object of the oscillator.
  double* sample; //pointer to actual wavetable_array.
  int wavetable_position; //sample_position in the wavetable_array.
  int wavetable_length; //length of the wavetable_array.
};

#endif
