
#ifndef ENVELOPE_H
#define ENVELOPE_H

#include <iostream>
#include <array>
#include "envelope_voice.hpp"
#include "envelope_wavetable.hpp"

class Envelope {
public:
  Envelope(int samplerate, int polyphony);
  Envelope(int samplerate, int polyphony, float attack, float decay, double sustain, float release);
  ~Envelope();

  Envelope() = delete;

  void tick();
  double get_sample(int voice_index);
  void set_polyphony(int polyphony);

private:
  Envelope_Wavetable* wavetable;
  std::array<Envelope_Voice*, 12> voices;
  int polyphony;
};

#endif
