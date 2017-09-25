#include <iostream>
#include <sstream>
#include "diagram_shape.h"

//used to compare doubles
bool doubleEqual(double a, double b) {
    return fabs(a - b) < DBL_EPSILON;
}

//finds distance between two points
double euclideanDistance(cv::Point pt1, cv::Point pt2) {
    cv::Point diff = pt1 - pt2;
    return cv::sqrt(diff.x*diff.x + diff.y*diff.y);
}

double dotProduct(cv::Point pt1, cv::Point pt2, cv::Point pt3)
{
	return (pt2 - pt1).ddot((pt3 - pt1));
}

//checks if it is possible to to combine this and shape, if it is return true and edit result_combination
//Can be used when finding shapes in diagram_processing.cpp
bool DiagramShape::combine(const DiagramShape &shape, DiagramShape &result_combination) const {
  // *** IMPLEMENT *** 

	if (closed())
		return false;
	if (find(ids.begin(), ids.end(), shape.id) != ids.end())
		return false;
	if (points.back() == shape.points.back())
	{
		result_combination.points = points;
		result_combination.points.push_back(shape.points.front());
		result_combination.ids = ids;
		result_combination.ids.push_back(shape.id);

		return true;
	}
	if (points.back() == shape.points.front())
	{
		result_combination.points = points;
		result_combination.points.push_back(shape.points.back());
		result_combination.ids = ids;
		result_combination.ids.push_back(shape.id);

		return true;
	}
	if (points.front() == shape.points.back())
	{
		result_combination.points = points;
		result_combination.points.insert(result_combination.points.begin(), shape.points.front());
		result_combination.ids = ids;
		result_combination.ids.push_back(shape.id);

		return true;
	}
	if (points.front() == shape.points.front())
	{
		result_combination.points = points;
		result_combination.points.insert(result_combination.points.begin(), shape.points.back());
		result_combination.ids = ids;
		result_combination.ids.push_back(shape.id);

		return true;
	}

	return false;
}


bool DiagramShape::convertToSquare() {
  // *** IMPLEMENT ***
	if (points.size() != 5)
		return false;
	double sideLength = euclideanDistance(points[0], points[1]);
	for (int i = 0; i < points.size() - 1; i++)
	{
		if (euclideanDistance(points[i], points[i + 1]) != sideLength)
		{
			return false;
		}
	}
	if (dotProduct(points[1], points[0], points[2]) != 0)
		return false;
	type = SQUARE;
	static int sqInd = 1;
	stringstream ss;
	ss << "sq" << sqInd++;
	id = ss.str();
	sort(ids.begin(), ids.end());
	return true;
}

bool DiagramShape::convertToRectangle() {
  // *** IMPLEMENT ***

	if (points.size() != 5)
		return false;

	double width = euclideanDistance(points[0], points[1]);
	double height = euclideanDistance(points[1], points[2]);
	if (width != euclideanDistance(points[2], points[3]))
		return false;
	if (height != euclideanDistance(points[3], points[0]))
		return false;
	
	if (dotProduct(points[1], points[0], points[2]) != 0)
		return false;

	type = RECTANGLE;
	static int rInd = 1;
	stringstream ss;
	ss << "r" << rInd++;
	id = ss.str();
	sort(ids.begin(), ids.end());
	return true;
}

bool DiagramShape::convertToTriangle() {
    // *** IMPLEMENT ***

	if (points.size() != 4)
		return false;


    type = TRIANGLE;
	static int tInd = 1;
	stringstream ss;
	ss << "t" << tInd++;
	id = ss.str();
	sort(ids.begin(), ids.end());
    return true;
}

bool DiagramShape::convertToScc()
{
	type = SCC;
	static int sccInd = 1;
	stringstream ss;
	ss << "scc" << sccInd++;
	id = ss.str();
	sort(ids.begin(), ids.end());
	return true;
}

bool DiagramShape::closed() const
{
	return points.front() == points.back();
}
bool DiagramShape::equals(const DiagramShape &other) const
{
	for (string primId : ids)
	{
		if (find(other.ids.begin(), other.ids.end(), primId) == other.ids.end())
			return false;
	}
	return true;
}
bool DiagramShape::shareSide(const DiagramShape &other) const
{
	for (string primId : ids)
	{
		if (find(other.ids.begin(), other.ids.end(), primId) != other.ids.end())
			return true;
	}
	return false;
}
bool DiagramShape::overlapping() const
{
	for (int i = 0; i < points.size(); i++)
	{
		for (int j = i + 1; j < points.size(); j++)
		{
			if (points[i] == points[j])
				return true;
		}
	}
	return false;
}
void DiagramShape::purgeExtraPoints()
{
	for (int i = 0; i < points.size() - 2;)
	{
		cv::Point point21 = (points[i + 2] - points[i + 1]);
		point21 = point21 / (sqrt(point21.ddot(point21)));
		cv::Point point10 = (points[i + 1] - points[i + 0]);
		point10 = point10 / (sqrt(point10.ddot(point10)));
		if (point21 == point10)
		{
			points.erase(points.begin() + i + 1);
		}
		else
			i++;
	}
	cv::Point point21 = (points[points.size() - 1] - points[points.size() - 2]);
	point21 = point21 / (sqrt(point21.ddot(point21)));
	cv::Point point10 = (points[0] - points[1]);
	point10 = point10 / (sqrt(point10.ddot(point10)));
	if (point21 == point10)
	{
		points.erase(points.begin());
		points.pop_back();
		points.push_back(points[0]);
	}
	
}

//You do not need to edit this function
void DiagramShape::draw(cv::Mat &img, cv::Scalar color) {
    // scale everything to 1000 x 1000 (better resolution) and plot
    if (this->type == CIRCLE){
        cv::Point center = this->center;
        center.x *= 10;
        center.y *= 10;
        cv::circle(img, center, this->radius*10, color);
    }
    else if (this->type == DOT) {
        cv::Point center = this->center;
        center.x *= 10;
        center.y *= 10;
        cv::circle(img, center, this->radius*10, color, -1);
    }
    else {
        // Draw lines between each set of points.
        for (int i = 0; i < this->points.size()-1; i++) {
            cv::Point pt1 = this->points[i];
            pt1.x *= 10;
            pt1.y *= 10;
            cv::Point pt2 = this->points[i+1];
            pt2.x *= 10;
            pt2.y *= 10;
            cv::line(img, pt1, pt2, color);
        }
    }
}

