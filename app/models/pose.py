from math import pi, trunc

class Joint:
    def __init__(self, base=0, shoulder=0, elbow=0, wrist_1=0, wrist_2=0, wrist_3=0) -> None:  
        # TODO Validar se numero é maior que -6.282 
        self.base = base
        self.shoulder = shoulder
        self.elbow = elbow
        self.wrist_1 = wrist_1
        self.wrist_2 = wrist_2
        self.wrist_3 = wrist_3

    def get_joint_list(self):
        return list(self.joint.__dict__.values())

    def convert_to_rad(self):
        joints = self.get_list()
        converted_joints = []
        mpi = trunc(pi * 1000)
        for j in joints:
            if j > mpi:
                j = - ( 2 * mpi - j)
            j = j / 1000             
            converted_joints.append(j)
        return converted_joints

    def convert_to_deg(self):
        joints = self.get_list()
        return [round(x * (180/pi), 2) for x in joints]

class Pose(Joint):
    def __init__(self, joint: Joint = Joint(), has_inspection=False, speed: float=0.1, acc:float=0.1):
        self.joint = joint
        self.has_inspection = has_inspection
        self.speed = speed
        self.acc = acc

    def get_joint_list(self):
        return self.joint.get_joint_list()

    