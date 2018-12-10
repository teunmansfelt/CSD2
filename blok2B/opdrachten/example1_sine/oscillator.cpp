#include "oscillator.h"


// Constructor and destructor
Oscillator::Oscillator(double samplerate, double frequency) :
  samplerate(samplerate), frequency(frequency), phase(0), sample(0)
{
  // TODO - use setFrequency and phase instead, to prevent outrange values
  std::cout << "\nInside Oscillator::Oscillator (double frequency, double phase)"
    << "\nfrequency: " << frequency
    << "\nphase: " << phase;
}

Oscillator::~Oscillator()
{
  std::cout << "\nInside Oscillator::~Oscillator" << std::endl;
}

double Oscillator::getSample() { return sample; }

void Oscillator::tick()
{
  // increase phase
  phase += frequency / samplerate;
  // wrap phase from 0 to 1
  if(phase >= 1) phase = phase - 1;

  // calculate new sample
  calculate();
}

void Oscillator::setFrequency(double frequency)
{
  if(frequency > 0 && frequency < 0.5 * samplerate)
  this->frequency = frequency;
}

double Oscillator::getFrequency()
{
  return frequency;
}
