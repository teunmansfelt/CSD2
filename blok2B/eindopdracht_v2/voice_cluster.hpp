
#ifndef VOICE_CLUSTER_H
#define VOICE_CLUSTER_H

#include <iostream>
#include <vector>
#include "voice_cluster.hpp"
#include "wavetable.hpp"

class Voice_Cluster {
public:
  Voice_Cluster(Wavetable* a);
  ~Voice_Cluster();
};

#endif
