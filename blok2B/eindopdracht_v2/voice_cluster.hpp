
#ifndef VOICE_CLUSTER_H
#define VOICE_CLUSTER_H

#include <iostream>
#include <array>
#include "voice_cluster.hpp"
#include "oscillator_voice.hpp"
#include "wavetable.hpp"

class Voice_Cluster {
public:
  Voice_Cluster(Wavetable* wavetable_p);
  Voice_Cluster(
    Wavetable* wavetable_p,
    int unison_voices,
    float unison_pitch,
    float unison_panning,
    float unison_phase,
    float unison_blend
  );
  ~Voice_Cluster();

  void tick();
  double get_sample_L();
  double get_sample_R();

  void set_note(float frequency, double velocity);
  void set_number_of_voices(int number_of_voices);
  void set_unison(float pitch_amount, float panning_amount, float phase_amount, float blend_amount);
  void set_unison_pitch(float pitch_amount);
  void set_unison_panning(float panning_amount);
  void set_unison_phase(float phase_amount);
  void set_unison_blend(float blend_amount);

  bool is_active();

private:
  Wavetable* wavetable_p;
  std::array<Oscillator_Voice*, 9> voices;
  int active_voices;

  bool active;
};

#endif
