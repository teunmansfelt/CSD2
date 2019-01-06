
#include <iostream>
#include "square.hpp"

Square::Square(int samplerate) : Square(samplerate, 6) {}
Square::Square(int samplerate, int polyphony) : Oscillator(polyphony) {
  if(this->sine_count < 1) {
    this->wavetables[3] = new Square_Wavetable(samplerate);
  }
  this->shape = 3;
  this->square_count += 1;
  this->set_polyphony(polyphony);
}

Square::~Square() {}
