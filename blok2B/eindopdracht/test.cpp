
#include "sine.hpp"

#include <iostream>

int main() {

  // int size = 6;
  // double* test;
  // test = new double[size];
  // double* test_pointer = test;
  //
  // std::cout << test << std::endl;
  //
  // for(int i = 0; i < size; i++){
  //   *test_pointer = i;
  //   std::cout << *test_pointer << std::endl;
  //   test_pointer++;
  // }
  //
  // test_pointer = test;
  //
  // for(int i = 0; i < size; i++){
  //   std::cout << *test_pointer << std::endl;
  //   test_pointer++;
  // }

  Sine sine(44100);

  return 0;
}
