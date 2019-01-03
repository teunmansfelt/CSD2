
#include <iostream>
#include "voice.hpp"
// #include "wavetable.hpp"

Voice::Voice(Wavetable** wavetable) {
  this->wavetable = wavetable;
}

Voice::~Voice() {}
