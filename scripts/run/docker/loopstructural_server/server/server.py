import asyncio
import websockets
import json
import base64


import asyncio
import websockets
import json
import base64
import ast
import os
import glob
import logging
from pathlib import Path
from typing import Dict, List, Union
from dataclasses import dataclass
from L2S_wrapper import LoopStructural_Wrapper

# Configure logging
logging.basicConfig(
	level=logging.INFO,
	format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
	handlers=[
		logging.FileHandler('server.log'),
		logging.StreamHandler()
	]
)
logger = logging.getLogger(__name__)

@dataclass
class ServerConfig:
	"""Server configuration parameters"""
	port: int
	ip: str
	max_size: int
	source_data_path: Path = Path('./server/source_data')
	output_data_path: Path = Path('./output_data/vtk')

	def __post_init__(self):
		"""Ensure directories exist after initialization"""
		self.source_data_path.mkdir(parents=True, exist_ok=True)
		self.output_data_path.mkdir(parents=True, exist_ok=True)
		logger.info(f"Server configured with IP: {self.ip}, Port: {self.port}")

class MessageValidator:
	"""Validates incoming messages"""
	@staticmethod
	def validate(message: Dict) -> bool:
		required_fields = {
			"client_id": int,
			"project_id": int,
			"function": str,
			"params": str
		}
		
		try:
			if not isinstance(message, dict):
				return False
				
			for field, field_type in required_fields.items():
				if field not in message or not isinstance(message[field], field_type):
					logger.error(f"Invalid message format: missing or invalid {field}")
					return False
			return True
		except Exception as e:
			logger.error(f"Message validation error: {e}")
			return False

class FileManager:
	"""Handles file operations"""
	@staticmethod
	def clear_folder(folder_path: Path) -> None:
		"""Clear contents of a folder except __init__.py"""
		try:
			for file_path in folder_path.glob('*'):
				if file_path.is_file() and file_path.name != '__init__.py':
					file_path.unlink()
					logger.info(f"Deleted file: {file_path}")
		except Exception as e:
			logger.error(f"Error clearing folder {folder_path}: {e}")
			raise

	@staticmethod
	def list_files(directory_path: Path) -> List[Path]:
		"""Recursively list all files in directory"""
		try:
			return [f for f in directory_path.rglob('*') if f.is_file()]
		except Exception as e:
			logger.error(f"Error listing files in {directory_path}: {e}")
			return []

class LoopStructuralServer:
	"""Main server class handling WebSocket connections"""
	def __init__(self, config: ServerConfig):
		self.config = config

	async def create_response(self, package: Dict) -> Dict:
		"""Create base response package"""
		return {
			"client_id": package["client_id"],
			"project_id": package["project_id"],
			"success": 1,
			"error_msg": "",
			"response": "",
			"params": package["params"],
			"filename": package["filename"],

		}

	async def handle_test(self, package: Dict) -> Dict:
		"""Handle TEST function"""
		response = await self.create_response(package)
		response["response"] = f"Test message received ({package['params']})"
		print(f" Test message received  from {package['params']}")
		return response

	async def handle_upload(self, package: Dict) -> Dict:
		"""Handle UPLOAD function"""
		response = await self.create_response(package)
		try:
			flag = str(package["filename"])

			if flag == "":
				loopprojectfilename = f"server/source_data/server.{package['client_id']}.{package['project_id']}.loop3d"
			elif flag == "server_out":
				pass
			else:
				loopprojectfilename = f"server/source_data/server_" + str(
					response["filename"]
				)
			path = Path(loopprojectfilename)
			if path.exists():
				msg = f"Client {package['client_id']} already exists in container"
				logger.warning(msg)
				response["response"] = msg
			else:
				data = base64.b64decode(package["params"].encode("utf-8"))
				path.write_bytes(data)
				logger.info(f"Successfully uploaded file for client {package['client_id']}")
				
			# Check if all files received
			received_files = int(package["idx"])
			total_expected = int(package["Length"])
			if received_files+1 == total_expected:
				response["response"] = f"All data from client {package['client_id']} received"
				
		except Exception as e:
			logger.error(f"Upload error: {e}")
			response["success"] = 0
			response["error_msg"] = str(e)
		
		return response

	async def handle_execute(self, package: Dict) -> Dict:
		"""Handle EXECUTE function"""
		response = await self.create_response(package)
		try:
			config_data = ast.literal_eval(package["params"])
			logger.info(f"Executing LoopStructural with config: {config_data}")
			
			m2l = LoopStructural_Wrapper(config_data)
			m2l.run_all()
			
			# Collect output files
			output_files = FileManager.list_files(Path("output_data"))
			filepath_map = {f.name: str(f) for f in output_files}
			
			response.update({
				"output_data": str(filepath_map),
				"response": "output_data/vtk data is available"
			})
			logger.info("LoopStructural execution completed successfully")
			response["response"] =f"LoopStructural execution completed successfully"
		except Exception as e:
			logger.error(f"Execution error: {e}")
			response["success"] = 0
			response["error_msg"] = str(e)
		
		return response






	# async def handle_download(self, package: Dict) -> None:
	# 	"""Handles file requests and sends file data one at a time."""
	# 	VTK_FOLDER = Path("./output_data/vtk")

	# 	try:
	# 		logger.info("Downloading data...")
	# 		requested_filename = package.get("filename")
	# 		file_path = VTK_FOLDER / requested_filename

	# 		if not file_path.exists():
	# 			raise FileNotFoundError(f"File not found: {file_path}")

	# 		# Iterate over all files in the directory and send one at a time
	# 		file_count = 0
	# 		for file_path in VTK_FOLDER.glob("*"):
	# 			if file_path.is_file():
	# 				data = file_path.read_bytes()
	# 				encoded_data = base64.b64encode(data).decode("utf-8")

	# 				response = {
	# 					"success": 1,
	# 					"filename": file_path.name,
	# 					"filedata": encoded_data
	# 				}

	# 				logging.info(f"Sending file: {file_path.name}")
	# 				await self.send_response(response)  # Send file individually

	# 				file_count += 1
	# 				await asyncio.sleep(0.1)  # Optional: Prevent blocking other tasks

	# 		if file_count == 0:
	# 			raise FileNotFoundError(f"No files found in {VTK_FOLDER}")

	# 		logging.info("All files sent successfully.")

	# 	except Exception as e:
	# 		logging.error(f"Fetch error: {e}")
	# 		error_response = {
	# 			"success": 0,
	# 			"error_msg": str(e)
	# 		}
	# 		await self.send_response(error_response)  # Send error response


	# async def send_response(self, response: Dict) -> None:
	# 	"""Simulated function to send a response (to be implemented in your server)."""
	# 	print(f"Sending response: {response}")  # Replace with actual socket or WebSocket send




	async def handle_download(self, package: Dict) -> None:
			"""Handles file requests and sends file data (only the requested file)."""
			VTK_FOLDER = Path("./output_data/vtk")

			try:
				logging.info("Downloading data...")
				requested_filename = package.get("filename")
				print(f"requested filename is {requested_filename}")
				if not requested_filename:
					raise ValueError("No filename provided")

				file_path = VTK_FOLDER / requested_filename

				# Check if the file exists
				if not file_path.exists():
					raise FileNotFoundError(f"File not found: {file_path}")

				# Read and encode the requested file
				data = file_path.read_bytes()
				encoded_data = base64.b64encode(data).decode("utf-8")

				# Prepare the response
				response = {
					"success": 1,
					"filename": requested_filename,
					"filedata": encoded_data
				}

				logging.info(f"Sending file: {requested_filename}")
				await self.send_response(response)  # Send the encoded data response

			except Exception as e:
				logging.error(f"Fetch error: {e}")
				error_response = {
					"success": 0,
					"error_msg": str(e)
				}
				await self.send_response(error_response)  # Send error response

	async def send_response(self, response: Dict) -> None:
		"""Simulated function to send a response (to be implemented in your server)."""
		print(f"Sending response: {response}")  # Replace with actual socket or WebSocket send



	async def handle_full(self, package: Dict) -> Dict:
		"""Handle FULL function (clearing data)"""
		response = await self.create_response(package)
		try:
			for folder in [self.config.source_data_path, self.config.output_data_path]:
				FileManager.clear_folder(folder)
			response["response"] = f"FULL message received ({package['client_id']})"
			logger.info(f"Cleared all data for client {package['client_id']}")
			
		except Exception as e:
			logger.error(f"Error handling FULL request: {e}")
			response["success"] = 0
			response["error_msg"] = str(e)
		
		return response

	async def handler(self, websocket):
		"""Main WebSocket handler"""
		try:
			data = await websocket.recv()
			package = json.loads(data)
			logger.info(f"Received {package['function']} request from client {package['client_id']}")

			if not MessageValidator.validate(package):
				await websocket.send("Invalid server request")
				return

			handlers = {
				"TEST": self.handle_test,
				"UPLOAD": self.handle_upload,
				"EXECUTE": self.handle_execute,
				"DOWNLOAD": self.handle_download,
				"FULL": self.handle_full
			}

			handler = handlers.get(package["function"])
			if not handler:
				raise ValueError(f"Unknown function: {package['function']}")

			response = await handler(package)
			await websocket.send(json.dumps(response))
			
		except Exception as e:
			logger.error(f"Handler error: {e}")
			await websocket.send(json.dumps({
				"success": 0,
				"error_msg": str(e)
			}))
			
	# async def websocket_handler(self, websocket, path):
	# 	async for message in websocket:
	# 		package = json.loads(message)

	# 		if package.get("function") == "DOWNLOAD":
	# 			await self.handle_download(websocket, package)  # ✅ Fix: Ensure both websocket and package are passed


	async def start(self):
		"""Start the WebSocket server"""
		try:
			async with websockets.serve(
				self.handler,
				self.config.ip,
				self.config.port,
				max_size=self.config.max_size,
				ping_interval=None
			):
				logger.info(f"Server started on {self.config.ip}:{self.config.port}")
				await asyncio.Future()
		except Exception as e:
			logger.error(f"Server startup error: {e}")
			raise

def parse_arguments():
	"""Parse command line arguments"""
	import argparse
	parser = argparse.ArgumentParser(description="LoopStructural Server")
	parser.add_argument("-p", "--port", type=int, default=8888, help="Port to listen on")
	parser.add_argument("-ip", "--ip", type=str, default="", help="IP address to listen on. 0.0.0.0 for all")
	parser.add_argument("-m", "--max_size", type=int, default=2**20, help="Maximum size of packets in bytes")
	return parser.parse_args()

if __name__ == "__main__":
	args = parse_arguments()
	config = ServerConfig(args.port, args.ip, args.max_size)
	server = LoopStructuralServer(config)
	asyncio.run(server.start())
