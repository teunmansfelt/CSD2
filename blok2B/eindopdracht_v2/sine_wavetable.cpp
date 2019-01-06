
#include <iostream>
#include <math.h>
#include "sine_wavetable.hpp"

Sine_Wavetable::Sine_Wavetable(int samplerate) : Wavetable(samplerate){
  std::cout << "Sine_Wavetable - Constructor" << std::endl;
  this->wavetable = new double[wavetable_length];
  double* wavetable_p = this->wavetable;

  double phase = 0;
  double phase_increment = 1 / double(wavetable_length);

  for(int i = 0; i < wavetable_length; i++) {
    *wavetable_p = sin(PI_2 * phase);
    wavetable_p++;
    phase += phase_increment;
  }
}

Sine_Wavetable::~Sine_Wavetable() {
  std::cout << "Sine_Wavetable - Destructor" << std::endl;
}
