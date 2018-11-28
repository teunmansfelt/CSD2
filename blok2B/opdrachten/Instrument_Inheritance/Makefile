CXX=g++
CXXFLAGS=-Wall -std=c++14
LDFLAGS=
SOURCE=instrument.o string_instrument.o note_converter.o main.o

ensemble: $(SOURCE)
	$(CXX) -o $@ $(SOURCE) $(LDFLAGS)

.cpp.o:
	$(CXX) -c $(CXXFLAGS) $<

clean:
	rm -f *.o
