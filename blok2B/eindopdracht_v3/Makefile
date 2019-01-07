CXX=g++
CXXFLAGS= -Wall -std=c++14
LDFLAGS= -ljack
SOURCE= jack_module.o voice.o sine_wavetable.o wavetable.o sine.o oscillator.o signal_generator.o main.o

example: $(SOURCE)
	$(CXX) -o $@ $(SOURCE) $(LDFLAGS)

.cpp.o:
	$(CXX) -c $(CXXFLAGS) $<

clean:
	rm -f *.o
