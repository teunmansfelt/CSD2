
#ifndef SIGNAL_GENERATOR_H
#define SIGNAL_GENERATOR_H

#include <iostream>
#include <array>
#include "wavetable.hpp"
#include "voice.hpp"

class Signal_Generator {
protected:
  Signal_Generator();
  virtual ~Signal_Generator();

  Wavetable* wavetable; //Pointer to initialize the wavetable-object.

  int polyphony = 0; //Number of initiated voice-objects.
  std::array<Voice*, 12> voices; //Array to store voice-objects.
  int active_voices = 1; //Number of active voices (voices to be ticked).
  virtual void init_voice(int voice_index) = 0; //Voice-initiation function.

public:
  void tick();
  void set_polyphony(int polyphony); //Initiate voices.
};

#endif
