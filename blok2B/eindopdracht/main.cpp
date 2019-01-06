
#include "jack_module.hpp"
#include "sine.hpp"

#include <iostream>
#include <thread>

int main(int argc,char **argv) {

  // JackModule jack;
  // jack.init(argv[0]);
  // int samplerate = jack.getSamplerate();
  //
  // Sine sine(samplerate, 150);
  //
  // Oscillator* osc = &sine;
  //
  // jack.onProcess = [&osc](jack_default_audio_sample_t *inBuf,
  //    jack_default_audio_sample_t *outBuf, jack_nframes_t nframes) {
  //
  //   static double amplitude = 0.5;
  //
  //   for(unsigned int i = 0; i < nframes; i++) {
  //     // write sine output * amplitude --> to output buffer
  //     outBuf[i] = amplitude * osc->get_sample();
  //     // calculate next sample
  //     osc->tick();
  //   }
  //   return 0;
  // };
  //
  // jack.autoConnect();
  //
  // std::cout << "\n\nPress 'q' when you want to quit the program.\n";
  // bool running = true;
  // while (running)
  // {
  //   switch (std::cin.get())
  //   {
  //     case 'q':
  //       running = false;
  //       jack.end();
  //       break;
  //     case '1':
  //       int freq;
  //       std::cin >> freq;
  //       osc->set_frequency(freq);
  //       break;
  //     case '2':
  //       double amp;
  //       std::cin >> amp;
  //       osc->set_amplitude(amp);
  //   }
  // }
  return 0;
}
