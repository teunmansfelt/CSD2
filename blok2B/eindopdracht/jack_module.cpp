/*
#
# 2017 Marc Groenewegen
# altered by Ciska Vriezenga to serve as a simple example
#
*/

#include <iostream>
#include <mutex>
#include <unistd.h> // usleep
//TEMP - remove
#include "math.h"
#include "jack_module.h"

// prototypes & globals
static void jack_shutdown(void *);
static jack_port_t **input_ports,**output_ports;
static int numPorts = 2;
static jack_default_audio_sample_t **inBuffers;
static jack_default_audio_sample_t **outBuffers;


JackModule::JackModule()
{
  inBuffers = new jack_default_audio_sample_t*[numPorts];
  outBuffers = new jack_default_audio_sample_t*[numPorts];
} // JackModule()

JackModule::~JackModule()
{
  //deactivate jack and disconnect jack ports
  end();
} // ~JackModule()


int JackModule::init()
{
  return init("JackModule");
} // init()


int JackModule::init(std::string clientName)
{
  //open an external client session with a JACK server
  //options: use JackNullOption or JackNoStartServer
  //JackNullOption -> Null value to use when no option bits are needed.
  //JackNoStartServer -> Do not automatically start the JACK server when it is not already running
  client = jack_client_open(clientName.c_str(),JackNoStartServer,NULL);
  if( client == 0) {
    std::cout <<  "Unable to retrieve a JACK client. \n " <<
                  "Is the JACK server running?" << std::endl;
    return 1;
  }

  // install a shutdown callback
  jack_on_shutdown(client,jack_shutdown,0);
  // Install the callback wrapper
  jack_set_process_callback(client,_wrap_jack_process_cb,this);

  //register output and input ports for the client.
  input_ports = registerPorts(numPorts, "input", JackPortIsInput);
  output_ports = registerPorts(numPorts, "output", JackPortIsOutput);

  //Tell the Jack server that the program is ready to start processing audio.
  if(jack_activate(client)) {
    std::cout << "Cannot activate client." << std::endl;
    return -1;
  } // if

  return 0;
} // init()

jack_port_t**  JackModule::registerPorts(int numPorts, std::string name, JackPortFlags portFlag) {
  /* jack_port_register function parameters:
  jack_client_t * 	client,
  const char * 	port_name,
  const char * 	port_type,
  unsigned long 	flags,
  unsigned long 	buffer_size*/
  jack_port_t** ports = (jack_port_t **) malloc (sizeof (jack_port_t *) * numPorts);

  for(int i = 0; i < numPorts; i++) {
    if ((ports[i] = jack_port_register (client, (name + "_" + std::to_string(i)).c_str() , JACK_DEFAULT_AUDIO_TYPE, portFlag, 0)) == 0) {
      std::cout << "Can not register port: " << name << "\n";
      jack_client_close (client);
      exit (1);
    }
  }
  return ports;
}

const char** JackModule::getPorts(unsigned long flags)
{
  const char **ports;
  if((ports = jack_get_ports(client,NULL,NULL,flags)) == NULL)
  {
    std::cout << "Cannot find any physical output ports" << std::endl;
    exit(1);
  }
  return ports;
}


void JackModule::autoConnect()
{
  //check if a function is assigned to onProcess
  if(!onProcess) {
    std::cout << "\n_____ EXIT PROGRAM _____\n"
      << "The onProcess method is unassigned.\n"
      << "You need to assign a (lambda) function to JackModule::onProcess.\n"
      << "JackModule.onProcess will be called by the jack callback function.\n"
      << "________________________\n\n";
    exit(1);
  }
  const char **output_target_ports = getPorts(JackPortIsPhysical|JackPortIsInput);
  const char **input_target_ports = getPorts(JackPortIsOutput);

  for(int i = 0; i < numPorts; i++) {
    if(jack_connect(client,jack_port_name(output_ports[i]), output_target_ports[i]))
    {
      std::cout << "Cannot connect port: " << jack_port_name(output_ports[i])
        << ", to system port: " << output_target_ports[i] << std::endl;
    }
    if(jack_connect(client, input_target_ports[i], jack_port_name(input_ports[i])))
    {
      std::cout << "Cannot connect port: " << jack_port_name(input_ports[i])
        << ", to system port: " << input_target_ports[i] << std::endl;
    }
  }
  free(output_target_ports);
  free(input_target_ports);
} // autoConnect()




//returns the jack_clients samplerate
unsigned long JackModule::getSamplerate()
{
  return jack_get_sample_rate(client);
} // getSamplerate()



/* Deactivate jack and disconnect jack ports*/
void JackModule::end()
{
  jack_deactivate(client);
  for(int i = 0; i < numPorts; i++) {
    jack_port_disconnect(client,input_ports[i]);
    jack_port_disconnect(client,output_ports[i]);
    free(outBuffers[i]);
    free(inBuffers[i]);
  }
  delete outBuffers;
  outBuffers = nullptr;
  delete inBuffers;
  inBuffers = nullptr;
} // end()


/* allows to use a cpp function for the audio callback function */
int JackModule::_wrap_jack_process_cb(jack_nframes_t nframes,void *arg)
{
  // retrieve in and out buffers
  for(int i = 0; i < numPorts; i++) {
    inBuffers[i] = (jack_default_audio_sample_t *)jack_port_get_buffer(input_ports[i],nframes);
    outBuffers[i] = (jack_default_audio_sample_t *)jack_port_get_buffer(output_ports[i],nframes);
  }
  //call the onProcess function, that is assigned to the object
  return ((JackModule *)arg)->onProcess(inBuffers, outBuffers, nframes);
} // _wrap_jack_process_cb()


/*
 * shutdown callback may be called by JACK
 */
static void jack_shutdown(void *arg)
{
  exit(1);
} // jack_shutdown()
