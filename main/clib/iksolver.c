#include <math.h>
#define link_one = 0
#define link_two = 1
#define link_three = 2
#define jone_min = 3
#define jone_max = 4
#define jtwo_min = 5
#define jtwo_max = 6
#define jthree_min = 7
#define jthree_max = 8
#define ee_x = 9
#define ee_y = 10
#define phi_min = 11;
#define phi_max = 12;
#define phi_increments_index = 13;

float * IKSolver(float (*position)[3], float (*robot_params)[14]) {
    float ee_angle = -atan((*robot_params)[ee_y] / (*robot_params)[ee_x]);
    float phi = radians((*robot_params)[phi_min]);
    float phi_increment = radians((*robot_params)[phi_increments_index]);
    //calculates the angle by which the target has to be rotated to land on the y-z-plane
    float tx = (*position)[0];
    float ty = (*position)[1];
    float tz = (*position)[2];
    //float base_x = 1;
    //float base_y = 0;

    //The next few lines can be compacted into 1 line
    //base_y is zero, so ignored
    //float dn = tx * base_x;

    //norm of the base is 1 anyway
    //float n = norm(tx, ty);

    //float result = acos(dn/n)
    //I compacted everything into 1 line

    float base_angle = acos(tx / norm(tx, ty));
    if (ty > 0) {
        base_angle = -base_angle;
    }

    //rotation matrix is: [[cos(base_angle), -sin(base_angle), 0],
    //                    [sin(base_angle), cos(base_angle), 0],
    //                    [0, 0, 1]]
    //I'll hard-code the calculations here for performance.

    //we don't need the y-component (since we rotate s.t. y = 0)
    tx = cos(base_angle)*tx - sin(base_angle)*ty;

    //pre-allocate some variables I'll use in the while-loops so they don't get allocated
    //over and over again in each iteration.
    float wx;
    float wy;
    float delta;
    float c1_1;
    float c1_2;
    float c2;
    float s1_1;
    float s2_2;
    float s2_1;
    float s2_2;
    float theta1_1;
    float theta1_2;
    float theta2_1;
    float theta2_2;
    float theta3_1;
    float theta3_2;

    bool first_solution_valid = true;
    bool second_solution_valid = true;

    while (true) {
        wx = tx - (*robot_params)[link_three];
        wy = tz - (*robot_params)[link_three];

        delta = (wx*wx) + (wy*wy);

        c2 = (delta - pow((*robot_params)[0], 2) - pow((*robot_params)[1], 2) / (2*(*robot_params)[0]*(*robot_params)[1]);

        //prevents the calculation of a sqrt of c2<0
        if (c2 < 0) {
            phi += phi_increment;
            continue;
            //target is not reachable
        }
        s2_1 = -sqrt((1 - pow(c2, 2)));
        s2_2 = - s2_1;

        theta2_1 = atan2(s2_1, c2);
        theta2_2 = atan2(s2_2, c2);

        //checks if there doesn't exists a theta2 that is within bounds, then continue with the next phi.
        if (theta2_1 > (*robot_params)[jtwo_max] || theta2_1 < (*robot_params)[jtwo_min]) {
            first_solution_valid = false;
            if (theta2_2 > (*robot_params)[jtwo_max] || theta2_2 < (*robot_params)[jtwo_min]) {
                second_solution_valid = false;
                phi += phi_increment;
                continue;
            }
        }

        s1_1 = ((((*robot_params)[link_one] + ((*robot_params)[link_two] * c2)) * wy) - ((*robot_params)[link_two] * s2_1 * wx)) / delta;
        s1_2 = ((((*robot_params)[link_one] + ((*robot_params)[link_two] * c2)) * wy) - ((*robot_params)[link_two] * s2_2 * wx)) / delta;

        c1_1 = ((((*robot_params)[link_one] + ((*robot_params)[link_two] * c2)) * wx) + ((*robot_params)[link_two] * s2_1 * wy)) / delta;
        c1_2 = ((((*robot_params)[link_one] + ((*robot_params)[link_two] * c2)) * wx) + ((*robot_params)[link_two] * s2_2 * wy)) / delta;

        theta1_1 = atan2(s1_1, c1_1);
        theta1_2 = atan2(s1_2, c1_2);

        //checks if there doesn't exist a theta2 that is within bounds, then continue with the next phi
        if (theta1_1 > (*robot_params)[jone_max] || theta1_1 < (*robot_params)[jone_min]) {
            first_solution_valid = false;
            if (theta1_2 > (*robot_params)[jone_max] || theta1_2 < (*robot_params)[jone_min]) {
                second_solution_valid = false;
                phi += phi_increment;
                continue;
            }
        }

        theta3_1 = phi - theta2_1 - theta1_1;
        theta3_2 = phi - theta2_2 - theta1_2;

        //checks if there doesn't exist a theta3 that is within bounds, then continue with the next phi
        if (theta3_1 > (*robot_params)[jthree_max] || theta3_1 < (*robot_params)[jthree_min]) {
            first_solution_valid = false;
            if (theta3_2 > (*robot_params)[jthree_max] || theta3_2 < (*robot_params)[jthree_min]) {
                first_solution_valid = false;
                phi += phi_increment;
                continue;
            }
        }

        if (first_solution_valid != second_solution_valid) {
            if (first_solution_valid) {
                theta3_1 += degrees(ee_angle);
                theta1_1 += degrees(0.5 * M_PI);
                static float angles[][] = { {base_angle, theta1_1, theta2_1, theta3_1}, {0,0,0,0} };
                return &angles[0][0];
            }
             else {
                theta3_2 += degrees(ee_angle);
                theta1_2 += degrees(0.5 * M_PI);
                static float angles[][] = { {0,0,0,0}, {base_angle, theta1_2, theta2_2, theta3_2}};
                return &angles[0][0];
            }
        }
        else {
            theta3_1 += degrees(ee_angle);
            theta1_1 += degrees(0.5 * M_PI);

            theta3_2 += degrees(ee_angle);
            theta1_2 += degrees(0.5 * M_PI);

            static float angles[][] = { {base_angle, theta1_1, theta2_1, theta3_1}, {base_angle, theta1_2, theta2_2, theta3_2}};
            return &angles[0][0];
        }
    }




}

inline float norm(float x, float y) {
    return sqrt(x*x+y*y);
}

inline float radians(float angle) {
    return (angle*M_PI/180.0);
}

inline float degrees(float angle) {
    return (angle*180.0/M_PI);
}
}