
#include <iostream>
#include "signal_generator.hpp"

Signal_Generator::Signal_Generator() {}

Signal_Generator::~Signal_Generator() {
  for(int i = 0; i < this->polyphony ; i++) {
    delete this->voices[i];
  }
}

void Signal_Generator::tick() {
  for(int i = 0; i < this->active_voices; i++) {
    this->voices[i]->tick();
  }
}

void Signal_Generator::set_polyphony(int polyphony) {
  if(polyphony < 1) {
    for(int i = this->polyphony - 1; i >= 1; i--) {
      delete this->voices[i];
    }
  } else if(polyphony > 9) {
    for(int i = this->polyphony; i < 9; i++) {
      this->init_voice(i);
    }
  } else {
    int voices_to_add = polyphony - this->polyphony;
    if(voices_to_add == 0) {
      return;
    } else if(voices_to_add > 0) {
      for(int i = this->polyphony; i < polyphony; i++) {
        this->init_voice(i);
      }
    } else if(voices_to_add < 0) {
      for(int i = this->polyphony - 1; i >= polyphony; i--) {
        delete this->voices[i];
      }
    }
  }
  this->polyphony = polyphony;
}
