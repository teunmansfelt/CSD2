#include "saw.h"
#include "math.h"


// Constructor and destructor
Saw::Saw(double samplerate, double frequency) :
  Oscillator(samplerate, frequency)
{
  // TODO - use setFrequency and phase instead, to prevent outrange values
  std::cout << "\nInside Saw::oscillator"
    << "\nfrequency: " << frequency
    << "\nphase: " << phase;
}

Saw::~Saw()
{
  std::cout << "\nInside Saw::~Saw";
}


void Saw::calculate()
{
  // calculate sample
  // NOTE: sin() method is not the most efficient way to calculate the sine value
  sample = (phase * 2) - 1;
}
