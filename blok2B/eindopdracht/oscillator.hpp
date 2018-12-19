
#ifndef OSCILLATOR_H
#define OSCILLATOR_H

#include <iostream>
#include <array>

class Oscillator {
protected:
  //-- Constructor Destructor  --//
  Oscillator(int samplerate, float frequency, float phase, double amplitude);
  virtual ~Oscillator();

  //--protected fields --//
  double* wavetable; // Dynamic allocated array to store the wavetable.
  int wavetable_length;

public:
  //-- Sample --//
  void tick();
  void reset_phase();

  //-- Setters --//
  void set_frequency(float frequency);
  void set_amplitude(double amplitude);

  //-- Getters --//
  double get_sample();
  float get_frequency();
  double get_amplitude();

private:
  //-- private methods --//
  virtual void calculate_wavetable() = 0;

  //-- private fields --//
  int wavetable_position;
  int samplerate;
  float frequency;
  float phase;

  double amplitude;
  double next_amplitude;
  bool new_amplitude;
};

#endif
