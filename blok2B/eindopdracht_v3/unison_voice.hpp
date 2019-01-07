
#ifndef UNISON_VOICE_H
#define UNISON_VOICE_H

#include <iostream>
#include <array>
#include "voice.hpp"
#include "oscillator_voice.hpp"

class Unison_Voice : public Voice {
public:
  Unison_Voice(Wavetable* wavetable_p, int unison_voices);
  ~Unison_Voice();
  Unison_Voice() = delete;

public:
  void tick() override;
  void set_tick_step(int step, int step_offset) override;

  double get_sample() = 0 override;
  double get_sample_L() override;
  double get_sample_R() override;

  void reset_wavetable() override;

  void set_channel_multipliers(double multiplier_L, double multiplier_R) override;
  void set_num_voices(int number_of_voices) override;

private:
  std::array<Oscillator_Voice*, 9> voices;
  int active_voices = 1;
};

#endif
