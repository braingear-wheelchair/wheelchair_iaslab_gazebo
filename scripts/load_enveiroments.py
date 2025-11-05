#!/usr/bin/env python3

import rospy
from gazebo_msgs.srv import SpawnModel, DeleteModel
from std_msgs.msg import String
from geometry_msgs.msg import Pose

# Read the SDF or URDF file
model_x = "/var/home/piero/Projects/ros/wheelchair_ws/src/wheelchair_iaslab_gazebo/configurations/wall_x.sdf"
model_y = "/var/home/piero/Projects/ros/wheelchair_ws/src/wheelchair_iaslab_gazebo/configurations/wall_y.sdf"


class hmm_configuration:
    def __init__(self) -> None:
        rospy.init_node('gazebo_wall')
        self.setup_objects()
        self.setup_services()
        self.setup_listeners()
        self.new_request = False
        self.request_conf = ""

    def setup_listeners(self):
        rospy.Subscriber("gazebo_wall_configuratio", String, self.callback_requested_task)

    def callback_requested_task(self, msg: String):
        self.request_conf = msg.data
        self.new_request  = True
        
    def setup_objects(self) -> None:
        self.pose_left  = Pose()
        self.pose_rigth = Pose()
        self.pose_front = Pose()

        self.pose_front.position.x = 2.0

        self.pose_left.position.x = -1.5
        self.pose_left.position.y =  3.5

        self.pose_rigth.position.x = -1.5
        self.pose_rigth.position.y = -3.5

        self.reference_frame = ""
        self.robot_namespace = ""

        self.name_left  = "left"
        self.name_rigth = "rigth"
        self.name_front = "front"

        with open(model_x, 'r') as file:
            self.model_xml_x = file.read()

        with open(model_y, 'r') as file:
            self.model_xml_y = file.read()

        
    def setup_services(self) -> None:
        rospy.wait_for_service('/gazebo/spawn_sdf_model')
        rospy.wait_for_service('/gazebo/delete_model')

        self.spawn_model = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
        self.delete_model = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)

    def delete_current_env(self) -> None:
        objects = [self.name_left, self.name_rigth, self.name_front]
        for obj in objects:
            try:
                self.delete_model(obj)
            except:
                pass
  
    def run(self) -> None:
        r = rospy.Rate(16)

        while not rospy.is_shutdown():
            if self.new_request:
                self.new_request = False
                self.delete_current_env()
                if 'c' in self.request_conf:
                    self.spawn_model(self.name_front, self.model_xml_y , self.robot_namespace, self.pose_front, self.reference_frame)
                    rospy.sleep(0.3)
                if 'r' in self.request_conf:
                    self.spawn_model(self.name_rigth, self.model_xml_x , self.robot_namespace, self.pose_rigth, self.reference_frame)
                    rospy.sleep(0.3)
                if 'l' in self.request_conf:
                    self.spawn_model(self.name_left, self.model_xml_x , self.robot_namespace, self.pose_left, self.reference_frame)
                    rospy.sleep(0.3)
            r.sleep()

def main() -> None:
    conf = hmm_configuration()
    conf.run()

if __name__ == '__main__':
    main()