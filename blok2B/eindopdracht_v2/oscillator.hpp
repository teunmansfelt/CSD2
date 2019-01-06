
#ifndef OSCILLATOR_H
#define OSCILLATOR_H

#include <iostream>
#include "voice_cluster.hpp"
#include "wavetable.hpp"

class Oscillator {
protected:
  Oscillator(int polyphony);
  ~Oscillator();

  Oscillator() = delete;

  static Wavetable* wavetables[4];
  static int sine_count;
  static int triangle_count;
  static int saw_count;
  static int square_count;

  int shape;

public:
  void tick();
  double get_sample_L(int voice_index);
  double get_sample_R(int voice_index);

  void play_tone(float frequency, double velocity);

  void set_polyphony(int polyphony);

  void set_unison_voices(int number_of_voices);
  void set_unison_pitch(float pitch_amount);
  void set_unison_panning(float panning_amount);
  void set_unison_phase(float phase_amount);
  void set_unison_blend(float blend_amount);

private:
  std::array<Voice_Cluster*, 12> voice_clusters;
  int polyphony;

  int unison_voices;
  float unison_pitch;
  float unison_panning;
  float unison_phase;
  float unison_blend;
};

#endif
