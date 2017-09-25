//
//  read_input.hpp
//

#ifndef io_hpp
#define io_hpp

#include <stdio.h>
#include <vector>
#include <fstream>
#include <iostream>
#include <sstream>

#include "diagram_shape.h"
#include "diagram_processing.h"


using namespace std;

//Fills given primitive vector with primitives from the file named fileName
// *** IMPLEMENT ***
void readInput(string fileName, vector <DiagramShape> &primitives);
   
//Prints diagrams representations listed in the diagrams vector to two files with the base name output_name
void printOutput(vector < vector<DiagramShape> > diagrams, string output_name);



#endif /* io_hpp */
