#all the packages are stored in Fault_detection.egg-info/SOURCES.txt

from setuptools import setup,find_packages
from typing import List

HYPHEN_E_DOT="-e."  #we are writing this to remove the '-e.' file as it is not a dependency

def get_requirements(file_path:str)->List[str]:
    requirements=[]
    with open(file_path,"r") as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace('\n',"") for req in requirements]
    
    if(HYPHEN_E_DOT in requirements):
        requirements.remove(HYPHEN_E_DOT)
    return requirements

setup(
    name="Fault detection",     #now this name will be treated for package name 
    version="0.0.1",
    author="Amit",
    author_email="amitkumar990374@gmail.com",
    install_requirements=get_requirements("requirements.txt"),
    packages=find_packages()
)