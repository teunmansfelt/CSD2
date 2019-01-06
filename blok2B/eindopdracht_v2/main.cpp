
#include <iostream>
#include "sine.hpp"
#include "saw.hpp"
#include "square.hpp"
#include "oscillator.hpp"
#include "jack_module.hpp"

int main(int argc, char **argv) {

  // create a JackModule instance
  JackModule jack;

  // init the jack, use program name as JACK client name
  jack.init(argv[0]);

  Sine sine(jack.getSamplerate(), 1);
  Saw saw(jack.getSamplerate(), 1);
  Square square(jack.getSamplerate(), 1);
  Oscillator* osc = &square;

  osc->set_unison_voices(7);
  osc->set_unison_pitch(1);
  osc->set_unison_phase(0.7);
  //osc->set_unison_phase_randomness(0.4);
  osc->set_unison_panning(1);
  osc->set_unison_blend(0.8);
  osc->play_tone(80, 1);

  //assign a function to the JackModule::onProces
  jack.onProcess = [osc](jack_default_audio_sample_t **inBuffers,
    jack_default_audio_sample_t **outBuffers, jack_nframes_t nframes) {

    for(unsigned int i = 0; i < nframes; i++) {
      outBuffers[0][i] = osc->get_sample_L();
      outBuffers[1][i] = osc->get_sample_R();
      osc->tick();
    }

    return 0;
  };

  jack.autoConnect();

  //keep the program running and listen for user input, q = quit
  std::cout << "\n\nPress 'q' when you want to quit the program.\n";
  bool running = true;
  while (running) {
    switch (std::cin.get()) {
      case 'q':
        running = false;
        jack.end();
        break;
    }
  }
  return 0;
};
