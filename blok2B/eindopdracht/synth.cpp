

calculate_envelope(attack_time, decay_time, release_time);

//-- Envelope --//
void Oscillator::calculate_envelope(unsigned short attack_time, unsigned short decay_time, unsigned short release_time) {
  unsigned int attack_steps = (attack_time / float(1000)) * samplerate;    // Convert milliseconds to # of samples.
  unsigned int decay_steps = (decay_time / float(1000)) * samplerate;      //                ''
  unsigned int release_steps = (release_time / float(1000)) * samplerate;  //                ''
  unsigned int envelope_length = attack_steps + decay_steps + release_steps + 1; // envelope lenght in # of samples.
  envelope = new double[envelope_length];

  double attack_increment = double(1) / double(attack_steps);   // increment step of the attack per sample.
  double release_decrement = double(1) / double(release_steps); // decrement step of the release per sample.

  for(int i; i < envelope_length; i++) {
    if(i < attack_steps){
      envelope[i] = attack_increment * i;
    } else if(i < decay_steps){
      envelope[i] = double(1);
    } else if(i < release_steps){
      envelope[i] = 1 - release_decrement * i;
    } else {
      envelope[i] = 0;
    }
  }
}
