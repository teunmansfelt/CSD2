
#ifndef VOICE_CLUSTER_H
#define VOICE_CLUSTER_H

#include "voice.hpp"

#include <iostream>
#include <array>

class Voice_Cluster {
public:
  Voice_Cluster();
  ~Voice_Cluster();

  void set_wavetable(double* wavetable, int wavetable_length);

private:
  double* wavetable;
  int wavetable_length;
};

#endif
