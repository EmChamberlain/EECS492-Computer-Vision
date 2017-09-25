//
//  diagram_processing.h
//

#ifndef diagram_processing_h
#define diagram_processing_h

#include "diagram_shape.h"

// Main method called to solve this problem. The results should be stored in "results", where each inner vector is a found solution for the input diagram (given by the vector of primitives).
// ***IMPLEMENT***
void findShapes(vector<DiagramShape> &primitives, vector<vector<DiagramShape> > &results);

void recursiveFindValidCombinations(vector<vector<DiagramShape>> &results, vector<DiagramShape> validShapes, vector<DiagramShape> completedShapes);

//add relationships to shapes in each diagram
// ***IMPLEMENT***
void findRelations(vector<vector<DiagramShape> > &diagrams);

// Determines whether two shapes overlap. Returns true if shapes overlap, false otherwise.
bool shapeOverlap(const DiagramShape& shape1, const DiagramShape& shape2);

// Determines whether a shape is within another shape.
// Returns 0 if neither are within the other, 1 if shape1 is within shape2, 2 if shape2 is within shape1.
int shapeInside(const DiagramShape& shape1, const DiagramShape& shape2);

#endif /* diagram_processing_h */
