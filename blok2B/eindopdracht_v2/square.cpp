
#include <iostream>
#include <vector>
#include "square.hpp"

Square::Square(int samplerate) : Square(samplerate, 6) {}
Square::Square(int samplerate, int polyphony) : Oscillator(polyphony) {
  std::cout << "Square - Constructor" << std::endl;
  this->wavetable = new Square_Wavetable(samplerate);
  this->init_voices();
}

Square::~Square() {}
