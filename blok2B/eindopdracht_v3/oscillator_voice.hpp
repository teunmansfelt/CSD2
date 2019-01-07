
#ifndef OSCILLATOR_VOICE_H
#define OSCILLATOR_VOICE_H

#include <iostream>
#include "voice.hpp"

class Oscillator_Voice : public Voice {
public:
  Oscillator_Voice(Wavetable* wavetable_p);
  ~Oscillator_Voice();
  Oscillator_Voice() = delete;

public:
  void tick() override;
  void set_tick_step(int step, int step_offset) override;

  double get_sample() = 0 override;
  double get_sample_L() override;
  double get_sample_R() override;

  void reset_wavetable() override;

  void set_channel_multipliers(double multiplier_L, double multiplier_R) override;
  void set_num_voices(int number_of_voices) = 0 override;
  void set_phase_offset(int offset) = 0;

private:
  double* sample;
  double multiplier_L;
  double multiplier_R;

  int wavetable_position = 0;
  int wavetable_length;
  int phase_offset = 0;
};

#endif
