
#include <iostream>
#include "voice.hpp"

Voice::Voice(Wavetable* wavetable_p) {
  this->wavetable_p = wavetable_p;
}

Voice::~Voice() {}
