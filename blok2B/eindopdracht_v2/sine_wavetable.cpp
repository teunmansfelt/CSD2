
#include <iostream>
#include <vector>
#include "sine_wavetable.hpp"


Sine_Wavetable::Sine_Wavetable(int samplerate) : Wavetable(samplerate){
  std::cout << "Sine_Wavetable - Constructor " << std::endl;
}

Sine_Wavetable::~Sine_Wavetable() {}
