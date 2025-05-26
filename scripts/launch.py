import os #functionalities for interacting with the OS, such as environment variables and file paths
import subprocess #enables execution of external commands or programs directly from python

current_file_path = os.path.abspath(__file__) #retrieve absolute path of current python script


def run_docker_container():
    user = os.getenv("USER") #fetch username
    container_name = f"gello_{user}" #define container as gello_username
    gello_path = os.path.abspath(os.path.join(current_file_path, "../../")) #determine absolute path of gello, two levels above current script
    volume_mapping = f"{gello_path}:/gello" #prepare docker volume mapping from local gello directory to /gello inside container. Ensures changes inside the container affect the original source code

#docker run command construction
    cmd = [
        "docker",
        "run",
        "--runtime=nvidia", #use NVIDIA GPU runtime support
        "--rm", #autoremove container when it stops running
        "--name", 
        container_name,
        "--privileged", #grants the container priviliges such as accessing hardware
        "--volume", 
        volume_mapping,
        "--volume",
        "/home/gello:/homefolder", #maps host directory /home/gello to /homefolder insode the container
        "--net=host", #uses host network stack within the container for simplicity and direct access
        "--volume",
        "/dev/serial/by-id/:/dev/serial/by-id/", #maps serial devices such as Dynamixel motors
        "-it", #interactive mode with terminal support
        "gello:latest", #docker image
        "bash",
        "-c", #execute command inside bash
        "pip install -e third_party/DynamixelSDK/python && exec bash", #install DynamixelSDK python package, then runs a new bash shell
    ]

    subprocess.run(cmd) #execute assembled docker command


if __name__ == "__main__":
    run_docker_container()
