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

import subprocess
import shutil
import platform
import os

class DockerDataCopy:
    def __init__(self):
        self.docker_exe_path = self._find_docker_path()
    
    def _find_docker_path(self):
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

    def _run_command(self, command):
        """
        Run a subprocess command silently.
        
        :param command: Command to run as a list of arguments.
        :return: Command output (str) or None on failure.
        """
        try:
            result = subprocess.run(
                command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, check=False
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None
    
    def copy_from_docker(self, container_name, container_dir, local_dir):
        """
        Copies all files from a Docker container directory to the local machine directory.
        
        :param container_name: Name or ID of the Docker container.
        :param container_dir: Directory path inside the container.
        :param local_dir: Destination directory on the local machine.
        """
        if not os.path.exists(local_dir):
            os.makedirs(local_dir, exist_ok=True)
        if platform.system() == "Windows":
            command = [self.docker_exe_path, "cp", f"{container_name}:{container_dir}/.", local_dir]
        else:
             command = ["docker", "cp", local_dir, f"{container_name}:~/output_data/vtk"]
        self._run_command(command)
    
    def find_running_container(self, container_name):
        """
        Checks if a specific Docker container is running silently.
        
        :param container_name: Name of the container to check.
        :return: Container ID if running, None otherwise.
        """
        command = [self.docker_exe_path, "ps", "--filter", f"name={container_name}", "--format", "{{.ID}}"]
        return self._run_command(command)

