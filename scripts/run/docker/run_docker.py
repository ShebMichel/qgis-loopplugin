# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Loop3DModelGenDockWidget
								 A QGIS plugin
 This plugin preprocess map layers using map2loop and use its output for 3D modelling using LoopStructural.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
							 -------------------
		begin                : 2024-12-13
		git sha              : $Format:%H$
		copyright            : (C) 2024 by Center of Exploration Targeting, UWA
		email                : michel.nzikoumamboukou@uwa.edu.au
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt5.QtWidgets import QProgressBar
import shutil
import subprocess
import platform
import os
from pathlib import Path


def find_docker_path():
	"""
	Finds the Docker executable path.

	Returns:
		str: Full path to Docker executable if found.
		None: If Docker is not found.
	"""
	docker_path = shutil.which("docker")
	
	if docker_path:
		return docker_path

	if platform.system() == "Windows":
		possible_paths = [
			r"C:\Program Files\Docker\Docker\resources\bin\docker.exe",
			r"C:\Program Files\Docker\Docker\cli-plugins\docker.exe"
		]
		for path in possible_paths:
			if os.path.exists(path):
				return path

	return None

def is_docker_installed():
	"""Check if Docker is installed and accessible."""
	docker_path =find_docker_path()
	try:
		
		subprocess.run([str(docker_path), "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		return True
	except FileNotFoundError:
		return False
	except subprocess.CalledProcessError:
		return False

def is_container_running(docker_path,container_name):
	"""Check if a Docker container is running."""
	try:
		result = subprocess.run(
			[str(docker_path), "ps", "--filter", f"name={container_name}", "--format", "{{.Names}}"],
			stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True
		)
		return container_name in result.stdout.strip()
	except subprocess.CalledProcessError:
		return False

def get_running_container(docker_path,image_name):
	"""Get the name of a running container based on the image name."""
	try:
		result = subprocess.run(
			[str(docker_path), "ps", "--filter", f"ancestor={image_name}", "--format", "{{.Names}}"],
			stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True
		)
		return result.stdout.strip() if result.stdout.strip() else None
	except subprocess.CalledProcessError:
		return None


def run_docker_compose(self, yaml_directory, run_log_listWidget):
    """Check if the container is running; if not, build and start it."""
    self.run_log_listWidget = run_log_listWidget
    docker_path = find_docker_path()

    if not is_docker_installed():
        self.run_log_listWidget.addItem("Docker is not installed or not in PATH. Please install Docker.")
        return

    image_name = "loopstructural_server-loopstructural"

    try:
        container_name = get_running_container(docker_path, image_name)

        if is_container_running(docker_path, container_name):
            self.run_log_listWidget.addItem(f"Container '{container_name}' is already running.")
            return container_name  # Return the running container's name

    except Exception as e:
        self.run_log_listWidget.addItem(f"Error checking container status: {e}")

    # If not running, start the container
    self.run_log_listWidget.addItem("Starting Docker Compose...")

    compose_command = [str(docker_path), "compose", "up", "--build", "-d"]
    
    try:
        if platform.system() == "Windows":
            subprocess.run(compose_command, cwd=str(yaml_directory), shell=True, check=True)
        else:  # Linux or macOS
            subprocess.run(compose_command, cwd=str(yaml_directory), check=True)

        self.run_log_listWidget.addItem("Docker Compose started successfully!")
        
        # Get the container name after starting
        container_name = get_running_container(docker_path, image_name)
        self.run_log_listWidget.addItem(f"Container '{container_name}' is now running!")
        return container_name

    except subprocess.CalledProcessError as e:
        self.run_log_listWidget.addItem(f"Error running Docker Compose: {e}")
        return None


