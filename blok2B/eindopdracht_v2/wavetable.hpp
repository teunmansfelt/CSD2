
#ifndef WAVETABLE_H
#define WAVETABLE_H

#include <iostream>

class Wavetable {
protected:
  Wavetable(int samplerate);
  int wavetable_length;
  double* wavetable;

public:
  ~Wavetable();
  double* get_wavetable_address();
  int get_wavetable_length();
};

#endif
