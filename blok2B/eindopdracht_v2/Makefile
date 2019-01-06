CXX=g++
CXXFLAGS= -Wall -std=c++14
LDFLAGS= -ljack
SOURCE= jack_module.o square_wavetable.o saw_wavetable.o sine_wavetable.o wavetable.o square.o saw.o sine.o oscillator.o voice.o voice_cluster.o main.o

example: $(SOURCE)
	$(CXX) -o $@ $(SOURCE) $(LDFLAGS)

.cpp.o:
	$(CXX) -c $(CXXFLAGS) $<

clean:
	rm -f *.o
