
#ifndef WAVETABLE_H
#define WAVETABLE_H

#include <iostream>

class Wavetable {
protected:
  Wavetable(int samplerate);
  int wavetable_length;
  double* wavetable;

public:
  Wavetable();
  ~Wavetable();

private:
  virtual void calculate_wavetable() = 0;
};


#endif
