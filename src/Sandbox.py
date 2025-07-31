import subprocess
PROJECT_DEFAULT = 'SR'
MAINLINE = 'mainline'

class Sandbox():
    def __init__(self, pname: str = PROJECT_DEFAULT, devpath: str = MAINLINE):
        self.project_name = pname
        self.project_path = f'/Chassis/iRWS_Platform_Development/400-SP_SW/200-Custom/{self.project_name}/300_SwiRWS/200_Application/project.pj'
        self.devpath = ''
        if devpath != MAINLINE:
            self.devpath = f'--devPath={devpath}'
        self.scope = '--scope=!path:ASW/*/Mdl* --scope=!path:ASW/*/Doc* --scope=!path:ASW/*/Test/TPT* --scope=!path:ASW/*/Test/MXAM* --scope=!path:ToolsLib/Tools*'
        self.sandbox_folder = f'C:\sandbox\{self.project_name}_200Appl_{devpath}'

    # https://support.ptc.com/help/windchillrvs/r12.3.0.0/en/index.html#page/IntegrityHelp/si_createsandbox.html
    def create_sandbox(self, file = None):
        """creates a new Sandbox on your local machine
        --no - Responds to all confirmations with 'no'
        --project - Project name in Windchill
        --devPath - Name of development branch or empty for mainline
        --scope - Defines what subprojects, members, or both are included or or inverted (!) in the Sandbox
        """
        if file is None:
            return subprocess.run(
                f'si createsandbox --project={self.project_path} --no {self.devpath} {self.scope} {self.sandbox_folder}')
        else:
            return subprocess.run(
                f'si createsandbox --project={self.project_path} --no {self.devpath} {self.scope} {self.sandbox_folder}',
                stdout=file, stderr=file)


sandb = Sandbox(pname = '110_SR_GEN2', devpath = 'T_ID20092614_CP1.44.1.2_OSTaskStructure')
#with open ('log.txt', 'w') as file:
    #cmpl_process = sandb.create_sandbox(file)
    #file.write(cmpl_process.args)
    #file.write(cmpl_process.returncode.__str__())
cmpl_process = sandb.create_sandbox()
print(f'Finished process: {cmpl_process.args}')
print(f'Return code: {cmpl_process.returncode.__str__()}')

