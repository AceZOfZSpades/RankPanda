#!/usr/bin/env python
import unittest
import Point
import CubicHermiteSpline as CHS
import math


class TestCHS(unittest.TestCase):
    
    # Expected return value for slopes when given all three input points is half the difference between 
    # the value at 0 and the value at 2 for both x and y 
    def testGetSlopeAllThreePoints(self):
        p0 = Point.Point(2, 3)
        p1 = Point.Point(4, 7)
        p2 = Point.Point(5, 1)
        
        slopeSimple = CHS.SplineGenerator._GetSlope([p0, p1, p2])
        self.assertEqual(slopeSimple.x, 1.5, "Failed to calculate slope for x when three points were specified.")
        self.assertEqual(slopeSimple.y, -1, "Failed to calculate slope for y when three points were specified.")

    # Here, we expect value at 2 minus the value at 1 (not halved this time because it's only half as far?
    def testGetSlopeZerothNone(self):
        p1 = Point.Point(4, 7)
        p2 = Point.Point(5, 1)
        
        slopeZerothNone = CHS.SplineGenerator._GetSlope([None, p1, p2])
        self.assertEqual(slopeZerothNone.x, 1, "Failed to calculate slope for x when zeroth point was not specified.")
        self.assertEqual(slopeZerothNone.y, -6, "Failed to calculate slope for y when zeroth point was not specified.")
    
    # Here, we expect value at 1 minus the value at 2 (not halved this time because it's only half as far?
    def testGetSlopeLastNone(self):
        p0 = Point.Point(2, 3)
        p1 = Point.Point(4, 7)
        
        slopeLastNone = CHS.SplineGenerator._GetSlope([p0, p1, None])
        self.assertEqual(slopeLastNone.x, 2, "Failed to calculate slope for x when zeroth point was not specified.")
        self.assertEqual(slopeLastNone.y, 4, "Failed to calculate slope for y when zeroth point was not specified.")
        
    # This should fail; we do not permit the middle Point to be None.
    # Is this ok?
    # Also: skipping doesn't seem to work.  Wrong version of Python?
    # @unittest.skip("Currently does not work: does not throw an exception but merely calculates ignoring middle point.")
    # def testGetSlopeMiddleNone(self):
        # p0 = Point.Point(2, 3)
        # p2 = Point.Point(5, 1)

        # TODO: Uncomment if test is actually correct.
        # self.assertRaises(None, CHS.SplineGenerator._GetSlope, [p0, None, p2])

    # Test the whole of the GetSplines method
    # For this test, we simply pick a bunch of points, calculate the expected splines manually, and compare.
    # This test is letting GetSplines calculate the slopes automatically. 
    def testGetSplinesNoSlope(self):
        p0 = Point.Point(10,10)
        p1 = Point.Point(15,15)
        p2 = Point.Point(20,10)
        p3 = Point.Point(30,10)
        p4 = Point.Point(30,30)
        p5 = Point.Point(10,20)
        
        # Expected slopes:
        # Yes I know this isn't a good unit test but it should stand until/unless we refactor GetSlopes out of CHS
        s0 = Point.Point(5, 5)
        s1 = Point.Point(5, 0)
        s2 = Point.Point(7.5, -2.5)
        s3 = Point.Point(5, 10)
        s4 = Point.Point(-10, 5)
        s5 = Point.Point(-20, -10)
        
        actualSplineList = CHS.SplineGenerator.GetSplines([p0,p1,p2,p3,p4,p5], [None,None,None,None,None,None])
        
        
        # Not in a loop so that it's explicit what's going on:
        xf0 = [p0.x, s0.x, (-3*p0.x + -2*s0.x + 3*p1.x + -1*s1.x), (2*p0.x + 1*s0.x + -2*p1.x + 1*s1.x)]
        yf0 = [p0.y, s0.y, (-3*p0.y + -2*s0.y + 3*p1.y + -1*s1.y), (2*p0.y + 1*s0.y + -2*p1.y + 1*s1.y)]
        xf1 = [p1.x, s1.x, (-3*p1.x + -2*s1.x + 3*p2.x + -1*s2.x), (2*p1.x + 1*s1.x + -2*p2.x + 1*s2.x)]
        yf1 = [p1.y, s1.y, (-3*p1.y + -2*s1.y + 3*p2.y + -1*s2.y), (2*p1.y + 1*s1.y + -2*p2.y + 1*s2.y)]
        xf2 = [p2.x, s2.x, (-3*p2.x + -2*s2.x + 3*p3.x + -1*s3.x), (2*p2.x + 1*s2.x + -2*p3.x + 1*s3.x)]
        yf2 = [p2.y, s2.y, (-3*p2.y + -2*s2.y + 3*p3.y + -1*s3.y), (2*p2.y + 1*s2.y + -2*p3.y + 1*s3.y)]
        xf3 = [p3.x, s3.x, (-3*p3.x + -2*s3.x + 3*p4.x + -1*s4.x), (2*p3.x + 1*s3.x + -2*p4.x + 1*s4.x)]
        yf3 = [p3.y, s3.y, (-3*p3.y + -2*s3.y + 3*p4.y + -1*s4.y), (2*p3.y + 1*s3.y + -2*p4.y + 1*s4.y)]
        xf4 = [p4.x, s4.x, (-3*p4.x + -2*s4.x + 3*p5.x + -1*s5.x), (2*p4.x + 1*s4.x + -2*p5.x + 1*s5.x)]
        yf4 = [p4.y, s4.y, (-3*p4.y + -2*s4.y + 3*p5.y + -1*s5.y), (2*p4.y + 1*s4.y + -2*p5.y + 1*s5.y)]
        
        expectedSplineList = [[xf0, yf0], [xf1, yf1], [xf2, yf2], [xf3, yf3], [xf4, yf4]]
        
        self.assertEqual(len(actualSplineList), len(expectedSplineList), "Failed to calculate the correct number of spline functions")
        
        for i in range (0, len(expectedSplineList)):
            for j in range (0,2):
                for k in range (0,4):
                    self.assertEqual(actualSplineList[i][j][k], expectedSplineList[i][j][k], "Error in calculating splines.  Spline number " + str(i) + ", axis number " + str(j) + ", coefficient " + str(k) + ".")
        
        
    # Test the whole of the GetSplines method
    # For this test, we simply pick a bunch of points and slopes, and compare.
    # This test is setting slopes explicitly (except one, to make sure it can still calculate it correctly. 
    def testGetSplinesInputSlope(self):
        p0 = Point.Point(10,10)
        p1 = Point.Point(15,15)
        p2 = Point.Point(20,10)
        p3 = Point.Point(30,10)
        p4 = Point.Point(30,30)
        p5 = Point.Point(10,20)
        
        # Slopes (chosen by randomly stabbing the keyboard):
        s0 = Point.Point(2, 4)
        s1 = Point.Point(7, 7)
        s2 = Point.Point(3.2, -3.6)
        s3 = Point.Point(5, 10) # this one is what we expect to calculate
        s4 = Point.Point(0, -23)
        s5 = Point.Point(1, -1)
        
        # Leave one None to make sure it still works:
        actualSplineList = CHS.SplineGenerator.GetSplines([p0,p1,p2,p3,p4,p5], [s0,s1,s2,None,s4,s5])
        
        # Not in a loop so that it's explicit what's going on:
        xf0 = [p0.x, s0.x, (-3*p0.x + -2*s0.x + 3*p1.x + -1*s1.x), (2*p0.x + 1*s0.x + -2*p1.x + 1*s1.x)]
        yf0 = [p0.y, s0.y, (-3*p0.y + -2*s0.y + 3*p1.y + -1*s1.y), (2*p0.y + 1*s0.y + -2*p1.y + 1*s1.y)]
        xf1 = [p1.x, s1.x, (-3*p1.x + -2*s1.x + 3*p2.x + -1*s2.x), (2*p1.x + 1*s1.x + -2*p2.x + 1*s2.x)]
        yf1 = [p1.y, s1.y, (-3*p1.y + -2*s1.y + 3*p2.y + -1*s2.y), (2*p1.y + 1*s1.y + -2*p2.y + 1*s2.y)]
        xf2 = [p2.x, s2.x, (-3*p2.x + -2*s2.x + 3*p3.x + -1*s3.x), (2*p2.x + 1*s2.x + -2*p3.x + 1*s3.x)]
        yf2 = [p2.y, s2.y, (-3*p2.y + -2*s2.y + 3*p3.y + -1*s3.y), (2*p2.y + 1*s2.y + -2*p3.y + 1*s3.y)]
        xf3 = [p3.x, s3.x, (-3*p3.x + -2*s3.x + 3*p4.x + -1*s4.x), (2*p3.x + 1*s3.x + -2*p4.x + 1*s4.x)]
        yf3 = [p3.y, s3.y, (-3*p3.y + -2*s3.y + 3*p4.y + -1*s4.y), (2*p3.y + 1*s3.y + -2*p4.y + 1*s4.y)]
        xf4 = [p4.x, s4.x, (-3*p4.x + -2*s4.x + 3*p5.x + -1*s5.x), (2*p4.x + 1*s4.x + -2*p5.x + 1*s5.x)]
        yf4 = [p4.y, s4.y, (-3*p4.y + -2*s4.y + 3*p5.y + -1*s5.y), (2*p4.y + 1*s4.y + -2*p5.y + 1*s5.y)]
        
        expectedSplineList = [[xf0, yf0], [xf1, yf1], [xf2, yf2], [xf3, yf3], [xf4, yf4]]
        
        self.assertEqual(len(actualSplineList), len(expectedSplineList), "Failed to calculate the correct number of spline functions")
        
        for i in range (0, len(expectedSplineList)):
            for j in range (0,2):
                for k in range (0,4):
                    self.assertEqual(actualSplineList[i][j][k], expectedSplineList[i][j][k], "Error in calculating splines.  Spline number " + str(i) + ", axis number " + str(j) + ", coefficient " + str(k) + ".")
        

    # Testing GetLength
    def testGetLength(self):
        
        # Test some cases we can verify analytically:
        
        # Straight line, vertical:
        fnlist = [[5, 0, 0, 0],[2, 3, 0, 0]] 
        self.assertAlmostEqual(CHS.SplineGenerator.GetLength(fnlist, 0.0001), 3, 3,  "GetLength incorrect for straight diagonal line case")
        
        # Straight line, horizontal:
        fnlist = [[5, 10, 0, 0],[2, 0, 0, 0]] 
        self.assertAlmostEqual(CHS.SplineGenerator.GetLength(fnlist, 0.0001), 10, 3,  "GetLength incorrect for straight diagonal line case")

        # A straight diagonal line:
        fnlist = [[23, 3, 0, 0],[2, 4, 0, 0]];
        self.assertAlmostEqual(CHS.SplineGenerator.GetLength(fnlist, 0.0001), 5, 3,  "GetLength incorrect for straight diagonal line case")
        
        # Should put in some more complicated cases but it's not trivial to find the length (without doing the computation of the method by hand.)
        
    def testEvalCubic(self):
        fn = [3, 6, 2, 8]
        t = 0.23;
        self.assertAlmostEqual(CHS.SplineGenerator.EvalCubic(t, fn), 8*t*t*t + 2*t*t + 6*t + 3, 6, "EvalCubic is incorrect")
        
    def testEvalSlopeOfCubic(self):
        fn = [3, 6, 2, 8]
        t = 0.43;
        self.assertAlmostEqual(CHS.SplineGenerator.EvalSlopeOfCubic(t, fn), 8*3*t*t + 2*2*t + 6, 6, "EvalSlopeOfCubic is incorrect")
        
    # This method assumes that GetPoints's constant NUMBERPESTEP = 8.
    # This should be changed to use a global constant.
    def testGetPoints(self):
        splineList = [[[2, 3, 0, 0], [2, 4, 0, 0]], [[5, -5, 0, 0], [6, 12, 0, 0]]]
        
        # This will generate 5 * 8 (+ 1?)  = 40 or 41 points in the first list, and 13 * 8 + 1 = 104 or 105 points in the second list.
        
        actualPoints = CHS.SplineGenerator.GetPoints(splineList)
        self.assertTrue(math.fabs(len(actualPoints[0]) - 41) <= 1, "Wrong number of points in the first list")
        self.assertTrue(math.fabs(len(actualPoints[1]) - 105) <= 1, "Wrong number of points in the second list")
        
        # Test the points (all but the last)
        
        for i in range(0, 40):
            self.assertAlmostEqual(actualPoints[0][i].x, 2 + 3 * (i / (float(40))), 6)
            self.assertAlmostEqual(actualPoints[0][i].y, 2 + 4 * (i / (float(40))), 6)
            
        for i in range(0, 104):
            self.assertAlmostEqual(actualPoints[1][i].x, 5 - 5 * (i / (float(104))), 6)
            self.assertAlmostEqual(actualPoints[1][i].y, 6 + 12 * (i / (float(104))), 6)
            
    # Use right triangles with integer lengths to make this simple...
    # 3,4,5; 5, 12, 13; 8, 15, 17.
    def testGetInformationAtLengthFraction(self):
        splineList = [[[2, 3, 0, 0], [2, 4, 0, 0]], [[5, -5, 0, 0], [6, 12, 0, 0]], [[0, 8, 0, 0], [18, -15, 0, 0]]]
        
        # Total length = 35 steps (5 + 13 + 17)
        
        info0 = CHS.SplineGenerator.GetInformationAtLengthFraction(splineList, 0.1)
        # This should be 3.5 steps into the 0th spline.
        
        self.assertAlmostEqual(info0[0].x, 2 + 3 * (3.5 / 5.0), 2)
        self.assertAlmostEqual(info0[0].y, 2 + 4 * (3.5 / 5.0), 2)
        self.assertAlmostEqual(info0[1].x, 3, 2)
        self.assertAlmostEqual(info0[1].y, 4, 2)
        self.assertEqual(info0[2], 0)
                 
        info0 = CHS.SplineGenerator.GetInformationAtLengthFraction(splineList, 0.5)
        # This should be 12.5 steps into the 1st spline (the middle one)
        
        self.assertAlmostEqual(info0[0].x, 5 - 5 * (12.5 / 13.0), 1)
        self.assertAlmostEqual(info0[0].y, 6 + 12 * (12.5 / 13.0), 1)
        self.assertAlmostEqual(info0[1].x, -5, 1)
        self.assertAlmostEqual(info0[1].y, 12, 1)
        self.assertEqual(info0[2], 1)
        
        
        
if __name__ == '__main__':
    unittest.main()
    
    
    
    
    
    
    
    
    
    
    
    
    
