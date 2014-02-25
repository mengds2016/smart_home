#ifndef _ROS_SERVICE_WriteSensorBit_h
#define _ROS_SERVICE_WriteSensorBit_h
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"

namespace smart_home_sensors
{

static const char WRITESENSORBIT[] = "smart_home_sensors/WriteSensorBit";

  class WriteSensorBitRequest : public ros::Msg
  {
    public:
      int32_t num;
      bool value;

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      union {
        int32_t real;
        uint32_t base;
      } u_num;
      u_num.real = this->num;
      *(outbuffer + offset + 0) = (u_num.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_num.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_num.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_num.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->num);
      union {
        bool real;
        uint8_t base;
      } u_value;
      u_value.real = this->value;
      *(outbuffer + offset + 0) = (u_value.base >> (8 * 0)) & 0xFF;
      offset += sizeof(this->value);
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      union {
        int32_t real;
        uint32_t base;
      } u_num;
      u_num.base = 0;
      u_num.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_num.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_num.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_num.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->num = u_num.real;
      offset += sizeof(this->num);
      union {
        bool real;
        uint8_t base;
      } u_value;
      u_value.base = 0;
      u_value.base |= ((uint8_t) (*(inbuffer + offset + 0))) << (8 * 0);
      this->value = u_value.real;
      offset += sizeof(this->value);
     return offset;
    }

    const char * getType(){ return WRITESENSORBIT; };
    const char * getMD5(){ return "bd079cf0ab9f0de476fa62cfbc9282a3"; };

  };

  class WriteSensorBitResponse : public ros::Msg
  {
    public:
      bool success;

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      union {
        bool real;
        uint8_t base;
      } u_success;
      u_success.real = this->success;
      *(outbuffer + offset + 0) = (u_success.base >> (8 * 0)) & 0xFF;
      offset += sizeof(this->success);
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      union {
        bool real;
        uint8_t base;
      } u_success;
      u_success.base = 0;
      u_success.base |= ((uint8_t) (*(inbuffer + offset + 0))) << (8 * 0);
      this->success = u_success.real;
      offset += sizeof(this->success);
     return offset;
    }

    const char * getType(){ return WRITESENSORBIT; };
    const char * getMD5(){ return "358e233cde0c8a8bcfea4ce193f8fc15"; };

  };

  class WriteSensorBit {
    public:
    typedef WriteSensorBitRequest Request;
    typedef WriteSensorBitResponse Response;
  };

}
#endif