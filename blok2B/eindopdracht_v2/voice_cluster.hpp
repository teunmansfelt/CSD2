
#ifndef VOICE_CLUSTER_H
#define VOICE_CLUSTER_H

#include <iostream>
#include <array>
#include "voice_cluster.hpp"
#include "voice.hpp"
#include "wavetable.hpp"

class Voice_Cluster {
public:
  Voice_Cluster(Wavetable** wavetable);
  ~Voice_Cluster();

  void tick();
  double get_sample_L();
  double get_sample_R();
  
  void set_number_of_voices(int number_of_voices);

private:
  Wavetable** wavetable;
  std::array<Voice*, 9> voices;
  int active_voices;
};

#endif
