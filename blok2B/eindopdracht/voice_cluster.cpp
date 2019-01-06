
#include "voice_cluster.hpp"
#include "voice.hpp"

#include <iostream>
#include <array>

Voice_Cluster::Voice_Cluster() {
}

Voice_Cluster::~Voice_Cluster() {}

void Voice_Cluster::set_wavetable(double* wavetable, int wavetable_length) {
  this->wavetable = wavetable;
  this->wavetable_length = wavetable_length;
}
