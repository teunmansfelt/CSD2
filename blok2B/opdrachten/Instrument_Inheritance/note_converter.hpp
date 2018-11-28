#ifndef NOTE_CONVERTER_H
#define NOTE_CONVERTER_H

#include <iostream>
#include <array>

int noteToNumber(std::string noteName); //Converts a note to a midi-number. Returns -1 when the note is invalid.
std::string numberToNote(int noteNumber); //Converts a midi-number to a note (including the octave number).

extern std::array<std::string,12> noteNames;

#endif
