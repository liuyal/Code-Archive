# =============================================================================
#
# (c) 2023 Schneider Electric SE. All rights reserved.
# All trademarks are owned or licensed by Schneider Electric SAS,
# its subsidiaries or affiliated companies.
#
# =============================================================================

import logging
import os
import pathlib
import subprocess
import sys
import tarfile

import docker

BASE_PATH = pathlib.Path(__file__).resolve().parent


def stop_all_containers(client: docker.client):
    """ Stop all running containers """

    for dc in client.containers.list(all=True):
        dc.remove(force=True)

    if len(client.containers.list(all=True)) == 0:
        return True

    return False


def create_container(dockerfile_path: str, image_name: str, container_name: str):
    """ Create a docker container """

    if not os.path.exists(dockerfile_path):
        raise Exception(f"Dockerfile does not exist {dockerfile_path}")

    client = docker.from_env()
    stop_all_containers(client)

    logging.info(f"Building docker image {image_name}:latest")
    build_cmd = (f"docker build . -f {dockerfile_path} -t {image_name}:latest")
    subprocess.run(build_cmd, capture_output=True)

    logging.info(f"Creating container {container_name} with image {image_name}")
    container = client.containers.run(image=image_name,
                                      name=container_name,
                                      ports={'22/tcp': ('127.0.0.1', 2222)},
                                      tty=True,
                                      detach=True)

    _ = subprocess.run("docker image prune -f", capture_output=True)

    return container


def download_from_container(container, file_path: str):
    """ Download file from container to host"""

    logging.info(f"Downloading {file_path} from {container.name}")

    with open(BASE_PATH / "tmp.tar", 'wb') as f:
        bits, stat = container.get_archive(file_path)
        for chunk in bits:
            f.write(chunk)

    file = tarfile.open(BASE_PATH / "tmp.tar")
    file.extract(file_path.split('/')[-1], BASE_PATH)
    file.close()
    os.remove(BASE_PATH / "tmp.tar")


def upload_to_container(container, dst_file_path: str, src_file_path: str):
    """ Upload file from container to host"""

    logging.info(f"Uploading {src_file_path} to {container.name}:{dst_file_path}")

    tar_file_name = src_file_path.split('.')[0] + '.tar'
    tar = tarfile.open(tar_file_name, mode='w')
    tar.add(src_file_path, arcname=src_file_path.split(os.sep)[-1])
    tar.close()

    data = open(tar_file_name, 'rb').read()
    container.put_archive(dst_file_path, data)
    os.remove(tar_file_name)


if __name__ == "__main__":
    logging.basicConfig(datefmt="%Y-%m-%d %H:%M:%S",
                        format="[%(asctime)s.%(msecs)03d] %(levelname)s: %(message)s",
                        stream=sys.stdout,
                        level=logging.INFO)

    docker_image_name = "ubuntu"
    docker_run_name = "apps-jerry-1"

    container = create_container(str(BASE_PATH / "Dockerfile"), docker_image_name, docker_run_name)
