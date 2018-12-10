#include "square.h"
#include "pulse.h"
#include "math.h"


// Constructor and destructor
Square::Square(double samplerate, double frequency) :
  Pulse(samplerate, frequency, 0.5)
{
  // TODO - use setFrequency and phase instead, to prevent outrange values
  std::cout << "\nInside Square::oscillator"
    << "\nfrequency: " << frequency
    << "\nphase: " << phase;
}

Square::~Square()
{
  std::cout << "\nInside Square::~Square";
}
