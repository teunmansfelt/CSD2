
#ifndef VOICE_H
#define VOICE_H

#include <iostream>
#include "wavetable.hpp"

#define QUARTER_PI 0.78539816339744

// class Voice_Cluster;

class Voice {
public:
//-- Constructor / Destructor --//
  Voice(Wavetable* wavetable_p);
  ~Voice();

//-- Sample Playback --//
  void tick();
  double get_sample_L(); //gets the samples from the wavetable for the left channel.
  double get_sample_R(); //gets the samples from the wavetable for the right channel.

//-- Channel Multiplier Calcultion --//
  void calculate_channel_multipliers(double velocity); //calculates and sets the left and right channel multiplier.

//-- Reset phase --//
  void reset_phase();

//-- Setters --//
  void set_panning(float panning); //sets both panning_factors.
  void set_frequency(float frequency);
  void set_amplitude(double amplitude);
  void set_pitch_offset(float offset, int direction);
  void set_phase_offset(float phase);

private:
  Wavetable* wavetable_p; //pointer to the wavetable_object of the oscillator.
  double* sample; //pointer to actual wavetable_array.
  double channel_multiplier_L; //multiplier for the left channel.
  double channel_multiplier_R; //multiplier for the right channel.
  int wavetable_position; //sample_position in the wavetable_array.

  int wavetable_length; //length of the wavetable_array.
  float frequency;
  double amplitude;
  float pitch_multiplier;
  int phase_offset;
  double pan_factor_L; //multiplier for the left channel as result of panning.
  double pan_factor_R; //multiplier for the right channel as result of panning.
};

#endif
