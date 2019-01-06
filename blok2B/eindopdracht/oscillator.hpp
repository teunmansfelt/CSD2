
#ifndef OSCILLATOR_H
#define OSCILLATOR_H

#include "voice_cluster.hpp"

#include <iostream>

class Oscillator {
protected:
  //-- Constructor Destructor  --//
  Oscillator(int samplerate, double amplitude, int polyphony, int unison);
  virtual ~Oscillator();

  //--protected fields --//
  double* wavetable; // Dynamic allocated array to store the wavetable.
  int wavetable_length;

public:
  void set_amplitude(double amplitude);
  void set_polyphony(int number_of_voices);
  void set_unison(int number_of_unison_voices);

private:
  //-- private methods --//
  virtual void calculate_wavetable() = 0;

  //-- private fields --//
  int samplerate;
  double amplitude;

  Voice_Cluster* voices;
  int voice_index;
  int polyphony;
  int unison;
};

#endif
