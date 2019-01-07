
#include <iostream>
#include "sine.hpp"
#include "jack_module.hpp"

int Sine::instance_count = 0;
Wavetable* Sine::wavetable_p = NULL;

int main(int argc, char **argv) {

  JackModule jack;
  jack.init(argv[0]);

  Sine sine(jack.getSamplerate(), 1);
  Oscillator* osc = &sine;

  osc->set_note(0, 200, 0.8);

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
