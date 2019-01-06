
#include "voice.hpp"

#include <iostream>

Voice::Voice(double* wavetable, int wavetable_length) {
  this->wavetable = wavetable;
  this->wavetable_length = wavetable_length;
}
