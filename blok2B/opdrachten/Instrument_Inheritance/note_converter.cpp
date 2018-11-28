
#include "note_converter.hpp"

#include <iostream>
#include <array>

//An array to store all the note_names
std::array<std::string,12> noteNames = {{"C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"}};

//Converts a note to it's midi-number and returns it.
int noteToNumber(std::string noteName){
  int octave = noteName.back()-46; //Takes the last char of the inputted note and converts the ASCII-code to it's corresponding number.
  noteName.pop_back(); //Removes the last char.
  for(int i = 0; i < 12; i++){ //Looks for the inputted string in the noteNames array.
    if(noteNames[i] == noteName){
      return i + 12 * octave;
    }
  }
  std::cout << "Invalid noteName\n";
  return -1; //Return -1 when the inputted string is not in the noteNames array.
}

//Converts a midi-number to it's note and octave number and returns it.
std::string numberToNote(int noteNumber){
  int octave = int(0);
  while(noteNumber >= 12){ //Figures out in what octave the inputted midi-number is.
    noteNumber -= 12;
    octave++;
  }
  octave += 46; //Converts the octave number to it's corresponding ASCII-code.
  return (noteNames[noteNumber] += octave);
}
