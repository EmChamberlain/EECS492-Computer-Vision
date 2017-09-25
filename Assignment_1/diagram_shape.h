//
//  diagram_shape.h
//

#ifndef diagram_shape_h
#define diagram_shape_h

#include <vector>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc.hpp>

using namespace std;

class DiagramShape;

enum ShapeType {CIRCLE, DOT, SQUARE, RECTANGLE, TRIANGLE, SCC};
enum RelationType {LEFT_OF, RIGHT_OF, ABOVE, BELOW, INSIDE, OVERLAP, TOUCH};

struct Relation {
public:
	//stores the id of the related shape
	Relation(string id, RelationType type)
	{
		otherShape_id = id;
		relation_type = type;
	}
    string otherShape_id;
    RelationType relation_type;
};

//You may edit this class but the output function is built to 
//work with the included member variables
class DiagramShape {
public:
	//stores relations to other diagrams that are found
    vector<Relation> relations;

    //stores ids of primitives that make up the shape
    vector<string> ids;
    
    //for all shapes not a circle or dot this vector stores the points that make up the shape
    vector<cv::Point> points;
   
    //the center of the shape, should be found for every shape to help with finding relations
    cv::Point center;

    // Only used for circles and dots. ------
    int radius;
    // --------------------------------------
    
    //The most specific type the shape is
    ShapeType type;

    //each shapes unqiue ID
    string id;
    
    //suggested helper functions, you may want to add more of your own ---------
    bool convertToSquare();
    bool convertToRectangle();
    bool convertToTriangle();
    bool convertToScc();
	bool closed() const;
	bool equals(const DiagramShape &other)const;
	bool shareSide(const DiagramShape &other)const;
	bool overlapping()const;
	void purgeExtraPoints();
	void calcCenter();


    bool combine(const DiagramShape &shape, DiagramShape &result_combination) const;

   //-------------------

    //Draws the shape to the given cv Matrix with a given color
    //This function is implemented for you
    void draw(cv::Mat &img, cv::Scalar color);
    
};


#endif /* diagram_shape_h */
