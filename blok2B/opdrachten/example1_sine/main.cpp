#include <iostream>
#include <thread>
#include "jack_module.h"
#include "sine.h"
#include "saw.h"
#include "pulse.h"
#include "square.h"

/*
 * NOTE: jack2 needs to be installed
 * jackd invokes the JACK audio server daemon
 * https://github.com/jackaudio/jackaudio.github.com/wiki/jackd(1)
 * on mac, you can start the jack audio server daemon in the terminal:
 * jackd -d coreaudio
 */

#define PI_2 6.28318530717959

int main(int argc,char **argv)
{
  // create a JackModule instance
  JackModule jack;

  // init the jack, use program name as JACK client name
  jack.init(argv[0]);
  double samplerate = jack.getSamplerate();
  double freq = 150;

  // create sine wave
  Sine sine(samplerate, freq);
  Saw saw(samplerate, freq);
  Square square(samplerate, freq);
  Pulse pulse(samplerate, freq, 0.2);

  Oscillator *osc = &sine;

  //assign a function to the JackModule::onProces
  jack.onProcess = [&osc](jack_default_audio_sample_t *inBuf,
     jack_default_audio_sample_t *outBuf, jack_nframes_t nframes) {

    static double amplitude = 0.5;

    for(unsigned int i = 0; i < nframes; i++) {
      // write sine output * amplitude --> to output buffer
      outBuf[i] = amplitude * osc->getSample();
      // calculate next sample
      osc->tick();
    }
    return 0;
  };

  jack.autoConnect();

  //keep the program running and listen for user input, q = quit
  std::cout << "\n\nPress 'q' when you want to quit the program.\n";
  bool running = true;
  while (running)
  {
    switch (std::cin.get())
    {
      case 'q':
        running = false;
        jack.end();
        break;
      case '1':
        osc = &sine;
        break;
      case '2':
        osc = &saw;
        break;
      case '3':
        osc = &square;
        break;
      case '4':
        osc = &pulse;
        break;
    }
  }

  //end the program
  return 0;
} // main()
