
#include <iostream>
#include <math.h>
#include "sine_wavetable.hpp"

Sine_Wavetable::Sine_Wavetable(int samplerate) : Wavetable(samplerate){
  std::cout << "Sine_Wavetable - Constructor" << std::endl;
}

Sine_Wavetable::~Sine_Wavetable() {
  std::cout << "Sine_Wavetable - Destructor" << std::endl;
}

void Sine_Wavetable::calculate_wavetable() {
  wavetable = new double[wavetable_length];
  double* wavetable_pointer = wavetable;

  double phase = 0;
  double phase_increment = 1 / double(wavetable_length);

  for(int i = 0; i < wavetable_length; i++) {
    *wavetable_pointer = sin(PI_2 * phase);
    wavetable_pointer++;
    phase += phase_increment;
  }
}
