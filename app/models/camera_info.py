from datetime import datetime

class CameraInfo:
    state: str = ''
    cobot_status: str = ''
    position_status: str = ''
    life_beat_cobot: str = ''
    popid: str = ''
    component_unit: str = ''
    parameter: str = ''
    manual: str = ''
    jobtime: str = '0'
    uptime: str = '0'
    message: str = ''
    final_result: str = ''
    parameters = ''
    param = ''
    predictions = ''
    results = ''
    joints = ''
    component_index = ''
    component_total = ''
    parameter_index = ''
    parameter_total = ''
    pose_index = ''
    pose_total = ''
    pose_name = ''

    def update(self, controller):
        self.state = controller.state.name
        self.cobot_status = controller.cobot.status.name
        self.parameter = controller.parameter         
        self.life_beat_cobot = str(controller.cobot.life_beat)
        self.manual = str(controller.manual_mode)
        self.position_status = controller.cobot.position_status.name
        # Create a class with all kind of images
        self.message = '[INFO] Message Test'
        self.joints = str(controller.cobot.joints.get_joint_list())            
        # self.results = controller.results
        ut = str((datetime.now() - controller.start_datetime).seconds)                
        self.uptime = ut
        self.component_index = str(controller.component_index)
        self.component_total = str(controller.total_components)
        self.pose_index = str(controller.pose_index + 1)
        self.pose_total = str(controller.total_poses)
        if controller.job:
            self.component_unit = controller.job.component_unit
            self.popid = controller.job.popid
            self.parameters = controller.job.parameter_list
            self.parameter_index = str(controller.param_index + 1)
            self.parameter_total = str(controller.total_param)
            jt = str((datetime.now() - controller.job.start_time).seconds)
            self.jobtime = jt
        pass
