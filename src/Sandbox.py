import subprocess
from io import TextIOWrapper
from abc import ABC, abstractmethod


class Sandbox(ABC):
    TYPE_NORMAL  = 0
    TYPE_VARIANT = 1
    TYPE_BUILD   = 2

    # https://support.ptc.com/help/windchillrvs/r12.3.0.0/en/index.html#page/IntegrityHelp/si_createsandbox.html
    @staticmethod
    def create(project_name: str,
               project_path: str,
               sandbox_location: str,
               type: int = TYPE_NORMAL,
               build_revision: str = '',
               variant: str = '',
               scope: str = '',
               log_file: TextIOWrapper = None) -> subprocess.CompletedProcess[bytes]:
        """creates a new Sandbox on your local machine
        --no - Responds to all confirmations with 'no'
        --project - Project name in Windchill
        --devPath - Name of development branch or empty for mainline
        --scope - Defines what subprojects, members, or both are included or or inverted (!) in the Sandbox
        """
        devpath: str = ''
        build: str = ''
        if type == Sandbox.TYPE_BUILD:
            build = f'--projectRevision={build_revision}'
        elif type == Sandbox.TYPE_VARIANT:
            devpath = f'--devpath={variant}'

        if log_file is None:
            return subprocess.run(
                f'si createsandbox --project={project_path} --no {devpath} {build} {scope} {sandbox_location}')
        else:
            return subprocess.run(
                f'si createsandbox --project={project_path} --no {devpath} {build} {scope} {sandbox_location}',
                stdout=log_file, stderr=log_file, stdin=log_file)

