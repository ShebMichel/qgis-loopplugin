import rasterio
import geopandas as gpd
from pyproj import Transformer

# Path to your DTM file


def extract_bbox( self, dtm_file):
	# Open the DTM file
	with rasterio.open(dtm_file) as src:
		# Get the current CRS of the DTM file
		dtm_crs = src.crs
		# Get the bounding box in the current CRS
		minx, miny, maxx, maxy = src.bounds
		try:
			return minx, miny, maxx, maxy
		except:
			# If the DTM is in a geographic CRS (e.g., WGS84), convert it to UTM
			# Define a transformer to UTM (replace "EPSG:32633" with your desired UTM zone)
			transformer = Transformer.from_crs(dtm_crs, "EPSG:32633", always_xy=True)

			# Convert the bounding box coordinates to UTM
			minx_utm, miny_utm = transformer.transform(minx, miny)
			maxx_utm, maxy_utm = transformer.transform(maxx, maxy)
			return minx_utm, miny_utm, maxx_utm, maxy_utm

	return



def get_shapefile_bounds(self, shapefile_path):
	"""
	Extracts the bounding box (minx, miny, maxx, maxy) from a shapefile.

	:param shapefile_path: Path to the geology shapefile (.shp)
	:return: A dictionary containing bounding box coordinates
	"""
	try:
		# Load the shapefile
		gdf = gpd.read_file(shapefile_path)

		# Get the bounding box values
		minx, miny, maxx, maxy = gdf.total_bounds
		bbox= {"minx": minx, "miny": miny, "maxx": maxx, "maxy": maxy}

		return bbox
	
	except Exception as e:
		print(f"Error: {e}")
		return None