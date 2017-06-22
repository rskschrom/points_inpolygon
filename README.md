# points_inpolygon
Determine where a point is located within a 2D polygon. We determine this by calculating the coverage fraction of the polygon line segments projected on a circle around the point.

There is also a script included for creating stellar crystal polygon shapes given a branch width fraction and an a axis length. After running the algorithm on a grid of points, we have an indicator array for whether the points are in the polygon or not. An example is shown below for a stellar crystal shape.
![alt text](https://github.com/rskschrom/points_inpolygon/blob/master/new_poly.png)
