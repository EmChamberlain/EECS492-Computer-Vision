//
//  diagram_processing.cpp
//

#include <iostream>
#include <vector>
#include <stack>
#include <set>

#include "diagram_processing.h"

using namespace std;

set<string> allIds;

void findShapes(vector<DiagramShape> &primitives, vector<vector<DiagramShape> > &results) {
  // *** IMPLEMENT ***
	for (DiagramShape prim : primitives)
		allIds.insert(prim.id);

	vector<DiagramShape> shapes;
	vector<DiagramShape> circles;
	for (vector<DiagramShape>::iterator it = primitives.begin(); it != primitives.end();)
	{
		if ((*it).type != SCC)
		{
			circles.push_back(*it);
			it = primitives.erase(it);
		}
		else
			it++;

	}
	stack<DiagramShape, vector<DiagramShape>> stack(primitives);
	while (!stack.empty())
	{
		DiagramShape shape = stack.top();
		stack.pop();
		for (DiagramShape primitive : primitives)
		{
			DiagramShape newShape;
			if (shape.combine(primitive, newShape))
			{
				if (newShape.closed())
					shapes.push_back(newShape);
				else if (newShape.overlapping())
					continue;
				else
					stack.push(newShape);
			}
			
		}
	}
	
	for (vector<DiagramShape>::iterator it = shapes.begin(); it != shapes.end(); it++)
		for (vector<DiagramShape>::iterator jt = it + 1; jt != shapes.end();)
		{
			if ((*it).equals(*jt) && it != jt)
				jt = shapes.erase(jt);
			else
				jt++;
		}
			
	
	for (DiagramShape shape : circles)
	{
		shapes.push_back(shape);
	}
	/*for (DiagramShape shape : shapes)
	{
		vector<DiagramShape> temp;
		temp.push_back(shape);
		results.push_back(temp);
	}*/
	//results.push_back(shapes);
	
	
	recursiveFindValidCombinations(results, shapes, vector<DiagramShape>());
	updateShapeInfo(results);
	
}


// This is used only for the shape overlap/inside functions.
void drawFilledShape(const DiagramShape& shape, cv::Mat& image, cv::Scalar color) {
    if (shape.type == CIRCLE || shape.type == DOT) {
        cv::Point center = shape.center;
        // Scale to 1000x1000 grid from 100x100 grid.
        center.x *= 10;
        center.y *= 10;
        cv::circle(image, center, shape.radius*10, color, -1);
    }
    else {
        vector<cv::Point> contour = shape.points;
        // Remove the last point, which is a repeat of the first point.
        contour.pop_back();
        // Scale to 1000x1000 grid from 100x100 grid.
        for (int i = 0; i < contour.size(); ++i) {
            contour[i] *= 10;
        }
        
        
        // create a pointer to the data as an array of points (via a conversion to
        // a Mat() object)
        
        const cv::Point *pts = (const cv::Point*) cv::Mat(contour).data;
        int npts = cv::Mat(contour).rows;
        
        cv::fillPoly(image, &pts, &npts, 1, color);
    }
}

bool shapeOverlap(DiagramShape& shape1, DiagramShape& shape2) {
    // Test overlap by doing per-pixel comparison of the two shapes.
    cv::Mat image1 = cv::Mat::zeros(cv::Size(1000, 1000), CV_8UC1);
    cv::Mat image2 = cv::Mat::zeros(cv::Size(1000, 1000), CV_8UC1);
    
    drawFilledShape(shape1, image1, cv::Scalar(255));
    drawFilledShape(shape2, image2, cv::Scalar(255));
    
    cv::Mat overlap;
    cv::bitwise_and(image1, image2, overlap);
    //cv::imshow("overlap test", overlap);
    
	// Check if shape 1 is entirely within the overlap. If so, then the overlap between shape 1 and the overlap should be the entirety of shape 1.
	cv::Mat shape1_overlap;
	cv::bitwise_and(image1, overlap, shape1_overlap);
	bool eq1 = cv::countNonZero(shape1_overlap != image1) == 0;

	// Check if shape 2 is entirely within the overlap.
	cv::Mat shape2_overlap;
	cv::bitwise_and(image2, overlap, shape2_overlap);
	bool eq2 = cv::countNonZero(shape2_overlap != image2) == 0;


	if (eq1) {
		shape1.relations.push_back(Relation(shape2.id, INSIDE));
		return true;
	}
	else if (eq2) {
		shape2.relations.push_back(Relation(shape1.id, INSIDE));
		return false;
	}
	
    //cv::waitKey();
    if (cv::countNonZero(overlap) > 0) {
		shape1.relations.push_back(Relation(shape2.id, OVERLAP));
        return true;
    }
    else {
        return false;
    }
}

int shapeInside(DiagramShape& shape1, DiagramShape& shape2) {
    // Compare the overlapping area and each shape. If a shape is entirely within the overlap, then that shape is within the other shape.
    cv::Mat image1 = cv::Mat::zeros(cv::Size(1000, 1000), CV_8UC1);
    cv::Mat image2 = cv::Mat::zeros(cv::Size(1000, 1000), CV_8UC1);
    
    drawFilledShape(shape1, image1, cv::Scalar(255));
    drawFilledShape(shape2, image2, cv::Scalar(255));
    
    cv::Mat overlap;
    cv::bitwise_and(image1, image2, overlap);
    
    // Check if shape 1 is entirely within the overlap. If so, then the overlap between shape 1 and the overlap should be the entirety of shape 1.
    cv::Mat shape1_overlap;
    cv::bitwise_and(image1, overlap, shape1_overlap);
    bool eq1 = cv::countNonZero(shape1_overlap != image1) == 0;
    
    // Check if shape 2 is entirely within the overlap.
    cv::Mat shape2_overlap;
    cv::bitwise_and(image2, overlap, shape2_overlap);
    bool eq2 = cv::countNonZero(shape2_overlap != image2) == 0;

    
    if (eq1) {
		shape1.relations.push_back(Relation(shape2.id, INSIDE));
        return 1;
    }
    else if (eq2) {
		shape2.relations.push_back(Relation(shape1.id, INSIDE));
        return 2;
    }
    else {
        return 0;
    }
}

bool shapeLeftOf(DiagramShape& shape1, DiagramShape& shape2)
{
	shape1.calcCenter();
	shape2.calcCenter();
	if (shape1.center.x < shape2.center.x)
	{
		shape1.relations.push_back(Relation(shape2.id, LEFT_OF));
		return true;
	}
		
	else if (shape2.center.x < shape1.center.x)
	{
		shape2.relations.push_back(Relation(shape1.id, LEFT_OF));
		return false;
	}

}

bool shapeAbove(DiagramShape& shape1, DiagramShape& shape2)
{
	shape1.calcCenter();
	shape2.calcCenter();
	if (shape1.center.y < shape2.center.y)
	{
		shape1.relations.push_back(Relation(shape2.id, ABOVE));
		return true;
	}
		
	else if (shape2.center.y < shape1.center.y)
	{
		shape2.relations.push_back(Relation(shape1.id, ABOVE));
		return false;
	}
		
}

void updateShapeInfo(vector<vector<DiagramShape>> &results)
{
	for (vector<DiagramShape> &vec : results)
	{
		for (int i = 0; i < vec.size(); i++)
		{
			vec[i].purgeExtraPoints();
			if (vec[i].convertToTriangle())
				continue;
			else if (vec[i].convertToSquare())
				continue;
			else if (vec[i].convertToRectangle())
				continue;
			else if (vec[i].convertToScc())
				continue;
			else
				cout << "Could not convert to any shape" << endl;
			for (int j = i + 1; j < vec.size(); j++)
			{
				
				shapeOverlap(vec[i], vec[j]);
				shapeLeftOf(vec[i], vec[j]);
				shapeAbove(vec[i], vec[j]);
			}
		}
	}
}


bool validShapeVector(const vector<DiagramShape> &shapes)
{
	vector<string> ids;
	for (DiagramShape shape : shapes)
		for (string id : shape.ids)
		{
			if (find(ids.begin(), ids.end(), id) != ids.end())
				return false;
			ids.push_back(id);
		}
			

	for (string id : allIds)
	{
		if (find(ids.begin(), ids.end(), id) == ids.end())
			return false;
	}
	return true;
}

void recursiveFindValidCombinations(vector<vector<DiagramShape>> &results, vector<DiagramShape> validShapes, vector<DiagramShape> completedShapes)
{
	if (validShapes.empty())
	{
		
		// check completedShapes for validity (uses all primitives)
		// add to results if it does
		if (validShapeVector(completedShapes) && !completedShapes.empty())
			results.push_back(completedShapes);
		else
			return;
	}
	for (vector<DiagramShape>::iterator it = validShapes.begin(); it != validShapes.end();)
	{
		DiagramShape currentShape = *it;
		completedShapes.push_back(currentShape);
		it = validShapes.erase(it);
		vector<DiagramShape> nextShapes = validShapes;
		for (vector<DiagramShape>::iterator jt = nextShapes.begin(); jt != nextShapes.end();)
		{
			if ((currentShape).shareSide(*jt))
				jt = nextShapes.erase(jt);
			else
				jt++;
		}
		recursiveFindValidCombinations(results, nextShapes, completedShapes);
		completedShapes.pop_back();
	}
}



