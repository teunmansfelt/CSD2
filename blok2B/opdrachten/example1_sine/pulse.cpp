#include "pulse.h"
#include "math.h"


// Constructor and destructor
Pulse::Pulse(double samplerate, double frequency, double pulse_width) :
  Oscillator(samplerate, frequency)
{
  this->pulse_width = pulse_width;
  // TODO - use setFrequency and phase instead, to prevent outrange values
  std::cout << "\nInside Pulse::oscillator"
    << "\nfrequency: " << frequency
    << "\nphase: " << phase;
}

Pulse::~Pulse()
{
  std::cout << "\nInside Pulse::~Pulse";
}


void Pulse::calculate()
{
  // calculate sample
  // NOTE: sin() method is not the most efficient way to calculate the sine value
  if(phase > pulse_width) {
    sample = 1;
  } else {
    sample = -1;
  }
}
