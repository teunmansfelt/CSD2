
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

  Wavetable* wavetable;
  void init_voices();

public:
  void tick();
  double get_sample_L();
  double get_sample_R();

  void play_tone(float frequency, double velocity);

  void set_unison_voices(int number_of_voices);
  void set_unison_pitch(float pitch_amount);
  void set_unison_panning(float panning_amount);
  void set_unison_phase(float phase_amount);
  void set_unison_blend(float blend_amount);

private:
  std::array<Voice_Cluster*, 12> voice_clusters;
  int polyphony;
};

#endif
