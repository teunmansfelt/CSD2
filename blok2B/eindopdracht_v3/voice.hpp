
#ifndef VOICE_H
#define VOICE_H

#include <iostream>
#include "wavetable.hpp"

class Voice {
protected:
  Voice(Wavetable* wavetable_p);
  virtual ~Voice();
  Voice() = delete;

  Wavetable* wavetable_p; //pointer to the wavetable_object of the oscillator.

  int tick_step;

public:
  virtual void tick() = 0;
  virtual void set_tick_step(int step, int step_offset) = 0;

  virtual double get_sample() = 0;
  virtual double get_sample_L() = 0;
  virtual double get_sample_R() = 0;

  virtual void reset_wavetable() = 0;

  virtual void set_channel_multipliers(double multiplier_L, double multiplier_R) = 0;
  virtual void set_num_voices(int number_of_voices) = 0;
  virtual void set_phase_offset(int offset) = 0;
};
