
#ifndef OSCILLATOR_H
#define OSCILLATOR_H

#include <iostream>
#include "signal_generator.hpp"

class Oscillator : public Signal_Generator {
protected:
  Oscillator();
  virtual ~Oscillator();

  virtual void init_voice(int voice_index) = 0;

public:
  double get_sample_L();
  double get_sample_R();

  void set_note(int voice_index, float frequency, double velocity);
  // void set_channel_multipliers(int voice_index, double multiplier_L, double multiplier_R);
};

#endif
