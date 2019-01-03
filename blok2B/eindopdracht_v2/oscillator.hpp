
#ifndef OSCILLATOR_H
#define OSCILLATOR_H

#include <iostream>
#include <array>
#include "voice_cluster.hpp"
#include "wavetable.hpp"

class Oscillator {
protected:
  Oscillator(int polyphony);
  ~Oscillator();

  void tick();
  double get_sample_L();
  double get_sample_R();

  Wavetable* wavetable;

private:
  std::array<Voice_Cluster*, 12> voice_clusters;
  int polyphony;
};

#endif
