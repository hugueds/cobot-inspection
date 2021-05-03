from math import pi, trunc

class Joints:
    def __init__(self, base=0, shoulder=0, elbow=0, wrist_1=0, wrist_2=0, wrist_3=0) -> None:
        # TODO Validar se numero é maior que -6.282
        self.base = base
        self.shoulder = shoulder
        self.elbow = elbow
        self.wrist_1 = wrist_1
        self.wrist_2 = wrist_2
        self.wrist_3 = wrist_3

    def get_joint_list(self) -> list:
        return list(self.__dict__.values())

    @staticmethod
    def convert_mrad2rad_s(joints) -> list:
        converted_joints = []
        mpi = trunc(pi * 1000)
        for j in joints:
            if j > mpi:
                j = - (2 * mpi - j)
            j = j / 1000
            converted_joints.append(j)
        return converted_joints

    def convert_mrad2rad(self) -> list:
        joints = self.get_joint_list()
        return Joints.convert_mrad2rad_s(joints)       

    def convert_rad2mrad(self) -> list:
        joints = self.get_joint_list()
        converted_joints = []
        mpi = trunc(pi * 1000)
        for j in joints:
            j = j * 1000
            if j < 0:
                j = j + mpi * 2
            converted_joints.append(int(j))
        return converted_joints

    def convert_rad2deg(self) -> list:
        joints = self.get_list()
        return [round(x * (180/pi), 2) for x in joints]


class Pose(Joints):
    def __init__(self, joints: list, speed: float = 1, acc: float = 0, has_inspection=False, sequence=0, name=''):
        j = joints
        self.joints = Joints(j[0], j[1], j[2], j[3], j[4], j[5])
        self.has_inspection = has_inspection
        self.speed = speed
        self.acc = acc
        self.sequence = sequence
        self.name = name

    def get_joint_list(self) -> list:
        return self.joints.get_joint_list()


if __name__ == '__main__':
    j = Pose([3500, 5567, 3881, 4856, 1542, 6279])
    a = Joints.convert_mrad2rad_s(j.get_joint_list())
    print(a)
    
    
    
