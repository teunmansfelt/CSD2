
#ifndef OSCILLATOR_H
#define OSCILLATOR_H

#include <iostream>
#include <vector>
#include "voice_cluster.hpp"
#include "wavetable.hpp"

class Oscillator {
protected:
  Oscillator(int samplerate, int polyphony);
  ~Oscillator();

  Wavetable wavetable;

public:

private:
  int samplerate;
  std::vector<Voice_Cluster> voices;
};

#endif
