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

import asyncio
import websockets
import json
import glob
import os
import base64
import subprocess
import logging
from pathlib import Path


class LoopClientManager:
	def __init__(self, ip_address: str, port_number: int):
		self.ip_address         = ip_address
		self.port_number        = port_number
		self.uri = f"ws://{self.ip_address}:{self.port_number}"

	async def ping_server_async(self) -> bool:
		"""Async function to ping the server with a timeout."""
		try:
			async with websockets.connect(self.uri, ping_interval=None) as socket:
				package = {
					"client_id": 1,
					"project_id": 1,
					"function": "TEST",
					"params": "Hello",
					"filename": "None"
				}
				await socket.send(json.dumps(package))
				resp = json.loads(await asyncio.wait_for(socket.recv(), timeout=5))
				return resp.get("success", 0) == 1
		except asyncio.TimeoutError:
			logging.error("Ping timeout: Server took too long to respond.")
			return False
		except Exception as e:
			logging.error(f"Ping failed: {e}")
			return False

	def ping_server(self) -> bool:
		"""Synchronous wrapper for ping_server_async"""
		return asyncio.run(self.ping_server_async())

	async def data_uploader_async(self, filename, filepath, idx, total_files):
		"""Async function to upload data."""
		try:
			async with websockets.connect(self.uri) as socket:
				with open(filepath, "rb") as file:
					encoded_data = base64.b64encode(file.read()).decode("utf-8")
				package = {
					"client_id": 1,
					"project_id": 1,
					"function": "UPLOAD",
					"params": encoded_data,
					"filename": filename,
					"Length": total_files,
					"loopprojectfilename": "./server/source_data",
					"idx": idx
				}
				await socket.send(json.dumps(package))
				resp = json.loads(await socket.recv())
				return resp.get("response", "")
		except Exception as e:
			logging.error(f"Error during upload: {e}")
			#self.run_log_listWidget.addItem(f"Error during upload: {e}")
			return ""

	def data_uploader(self, filename, filepath, idx, total_files):
		"""Synchronous wrapper for data_uploader_async"""
		return asyncio.run(self.data_uploader_async(filename, filepath, idx, total_files))

	async def loop_executor_async(self, conf_param):
		"""Async function to execute the loop."""
		try:
			async with websockets.connect(self.uri, ping_interval=None) as socket:
				package = {
					"client_id": 1,
					"project_id": 1,
					"function": "EXECUTE",
					"params": conf_param,
					"filename": "",
					"Length": ""
				}
				await socket.send(json.dumps(package))
				resp = json.loads(await socket.recv())
				return resp.get("output_data", []), resp.get("response", "")
		except Exception as e:
			logging.error(f"Execution error: {e}")
			return [], ""

	def loop_executor(self, conf_param):
		"""Synchronous wrapper for loop_executor_async"""
		return asyncio.run(self.loop_executor_async(conf_param))


	async def download_files_async(self, filename, output_dir,N,idx):
		# return the data downloaded

		try:
			async with websockets.connect(self.uri, ping_interval=None) as socket:
				package = {
					"client_id"    : 1,
					"project_id"   : 1,
					"function"     : "DOWNLOAD",
					"params"       : "",
					"filename"     :str(filename),
					"server_index" :idx,
					"nbre of files":N
				}
				await socket.send(json.dumps(package))
				resp = json.loads(await socket.recv())
				data = base64.b64decode(resp["filedata"].encode("utf-8"))
				# Save the received data to a local file
				file_path =os.path.join(output_dir,package["filename"])
				#print(f" File idx: {package["count"]} and name: {package["filename"]}")
				with open(str(file_path), 'wb') as f:
					f.write(data)
				
		except:
			print(f"Error: {package["filename"]} Can't be saved!")
	
	def data_downloader(self, filename, output_dir,N,idx):
		"""Synchronous wrapper for loop_executor_async"""
		return asyncio.run(self.download_files_async(filename,output_dir,N,idx))

#asyncio.run(main())