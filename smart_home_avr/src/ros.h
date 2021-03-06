#ifndef _ROS_H_
#define _ROS_H_

#include "ros/node_handle.h"
#include "atmega32hardware.h"

namespace ros
{
    typedef ros::NodeHandle_<Atmega32Hardware,25, 25, 280, 280> NodeHandle;
}

#endif
