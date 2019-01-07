/*
#
# 2017 Marc Groenewegen
# altered by Ciska Vriezenga to serve as a simple example
#
*/

#ifndef JACK_MODULE_H
#define JACK_MODULE_H

#include <string>
#include <functional>
#include <jack/jack.h>

class JackModule
{
public:
  JackModule();
  ~JackModule();
  int init();
  int init(std::string clientName);
  unsigned long getSamplerate();
  void autoConnect();
  void end();
  //the onProcess function that needs to be assigned to a JackModule object
  std::function <int(jack_default_audio_sample_t **, jack_default_audio_sample_t **,jack_nframes_t)> onProcess;

private:
  jack_client_t *client;
  static int _wrap_jack_process_cb(jack_nframes_t nframes,void *arg);
  jack_port_t** registerPorts(int numPorts, std::string name, JackPortFlags portFlag);
  void connectPorts(jack_port_t** sourcePorts, int numPorts, JackPortFlags targetPortFlag);
  const char** getPorts(unsigned long flags);
};

#endif
