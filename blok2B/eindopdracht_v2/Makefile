CXX=g++
CXXFLAGS= -Wall -std=c++14
LDFLAGS= -ljack
SOURCE= jack_module.o sine_wavetable.o wavetable.o sine.o oscillator.o voice_cluster.o main.o

example: $(SOURCE)
	$(CXX) -o $@ $(SOURCE) $(LDFLAGS)

.cpp.o:
	$(CXX) -c $(CXXFLAGS) $<

clean:
	rm -f *.o
