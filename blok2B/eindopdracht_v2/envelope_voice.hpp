
#ifndef ENVELOPE_VOICE_H
#define ENVELOPE_VOICE_H

#include <iostream>
#include "voice.hpp"
#include "wavetable.hpp"

class Envelope_Voice : public Voice {
public:
  Envelope_Voice(Wavetable* wavetable_p);
  ~Envelope_Voice();

  void tick() override;
  double get_sample();
  void reset_wavetable() override;
};

#endif
