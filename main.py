import os
import sys

def split_file(file_path, chunk_size_in_mb=90):
	"""Splits a file into smaller chunks.

	Args:
		file_path (str): The path to the file to split.
		chunk_size_in_mb (int): The size of each chunk in megabytes.
	"""
	file_path = os.path.abspath(file_path)
	chunk_size_in_bytes = chunk_size_in_mb * 1024 * 1024

	# Get the directory and filename
	filename = os.path.basename(file_path)

	container_folder = f"{filename}_chunks"
	output_chunks_dir = os.path.join(os.getcwd(), container_folder)
	total_size = os.path.getsize(file_path)
	total_chunks = (total_size + chunk_size_in_bytes -1) // chunk_size_in_bytes
	
	# split the file into chunks
	try:
		os.makedirs(output_chunks_dir, exist_ok=True)
		with open(file_path, 'rb') as file:
			chunk_index = 0
			while True:
				# Read the chunk from the file.
				chunk = file.read(chunk_size_in_bytes)
				# End of the file.
				if not chunk:
					break
				chunk_filename = os.path.join(output_chunks_dir, f"{filename}.chunk_{chunk_index:04d}")
				with open(chunk_filename, 'wb') as chunk_file:
					chunk_file.write(chunk)
				print(f"Progress: {chunk_index}/{total_chunks} chunks created...", end='\r')
				chunk_index += 1
			print()
			print(f"Completed.")
	except FileNotFoundError:
		print(f"Error: Input file {file_path} not found.")
	except Exception as e:
		print(f"An error has occurred during splitting: {e}")

def combine_files(output_filepath, original_input_filepath_prefix):
	"""
	Combines previously split file chunks (from a dedicated subfolder in the current working directory)
	back into the original file.

	Args:
		output_filepath (str): The desired path for the combined output file.
		original_input_filepath_prefix (str): The full path to the original file
											  that was split (e.g., 'path/to/my_large_file.zip').
											  This is used to determine the base filename to locate the chunks folder.
	"""
	print(f"Combining files with prefix '{original_input_filepath_prefix}' into '{output_filepath}'...")

	# Get the base filename of the original file
	original_input_filename = os.path.basename(original_input_filepath_prefix)

	# Determine the expected chunks folder name, assuming it's in the current working directory
	container_folder = f"{original_input_filename}_chunks"
	chunks_dir = os.path.join(os.getcwd(), container_folder)

	if not os.path.isdir(chunks_dir):
		print(f"Error: Chunks directory '{chunks_dir}' not found. Cannot combine files.")
		return

	# Find all chunks based on the original filename prefix within the chunks directory
	chunk_files = []
	for f_name in os.listdir(chunks_dir):
		if f_name.startswith(f"{original_input_filename}.chunk_") and os.path.isfile(os.path.join(chunks_dir, f_name)):
			chunk_files.append(os.path.join(chunks_dir, f_name))

	# Sort the chunk files numerically to ensure correct order
	chunk_files.sort()

	if not chunk_files:
		print(f"Error: No chunk files found in '{chunks_dir}' for prefix '{original_input_filename}'.")
		return

	total_chunks = len(chunk_files)
	try:
		with open(output_filepath, 'wb') as f_write:
			for i, chunk_file_path in enumerate(chunk_files):
				print(f"Reading chunk: '{chunk_file_path}'", end='\r') # Keep this for detailed view, or remove for cleaner progress
				with open(chunk_file_path, 'rb') as f_read:
					f_write.write(f_read.read())
				# Print progress on the same line for combining
				print(f"Progress: {i + 1}/{total_chunks} chunks combined...", end='\r')

			print() # Newline after combining loop
		print(f"Files combined successfully into '{output_filepath}'.")
	except Exception as e:
		print(f"An error occurred during combining: {e}")


if __name__ == "__main__":
	# Example Usage:
	# To split a file:
	# python your_script_name.py split path/to/your/large_file.zip 100
	# (This will split large_file.zip into 100MB chunks and place them in './large_file.zip_parts/' relative to where the script is run)

	# To combine files:
	# python your_script_name.py combine path/to/recombined_file.zip path/to/your/large_file.zip
	# (This will look for parts in './large_file.zip_parts/' relative to where the script is run and combine them back into recombined_file.zip)

	if len(sys.argv) < 2:
		print("Usage:")
		print("  To split: python file_splitter.py split <input_filepath> <chunk_size_mb>")
		print("  To combine: python file_splitter.py combine <output_filepath> <original_input_filepath_prefix>")
		sys.exit(1)

	command = sys.argv[1].lower()

	if command == "split":
		if len(sys.argv) != 4:
			print("Usage for split: python file_splitter.py split <input_filepath> <chunk_size_mb>")
			sys.exit(1)
		input_file = sys.argv[2]
		try:
			chunk_size = int(sys.argv[3])
			if chunk_size <= 0:
				raise ValueError("Chunk size must be a positive integer.")
			split_file(input_file, chunk_size)
		except ValueError as ve:
			print(f"Error: Invalid chunk size. {ve}")
	elif command == "combine":
		if len(sys.argv) != 4:
			print("Usage for combine: python file_splitter.py combine <output_filepath> <original_input_filepath_prefix>")
			sys.exit(1)
		output_file = sys.argv[2]
		original_input_prefix = sys.argv[3]
		combine_files(output_file, original_input_prefix)
	else:
		print(f"Unknown command: '{command}'. Use 'split' or 'combine'.")
		sys.exit(1)
