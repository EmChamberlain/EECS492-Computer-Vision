//
//  main.cpp
//

#include <iostream>
#include <memory>
#include <vector>

#include "diagram_shape.h"
#include "diagram_processing.h"
#include "io.h"

using namespace std;

int main(int argc, const char *argv[]) {
    // *** IMPLEMENT ***   
    // - take in input, find shapes, output
	string inputLoc(argv[1]);
	string outputLoc(argv[2]);
	string outputBaseName(argv[3]);

	vector<DiagramShape> primitives;
	readInput(inputLoc, primitives);

	vector<vector<DiagramShape>> results;
	findShapes(primitives, results);

	printOutput(results, outputLoc + "/" + outputBaseName);

	

    return 0;
}
