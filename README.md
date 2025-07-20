# Large File Splitter and Combiner

This Python script provides a command-line utility to split large files into smaller, manageable chunks and then combine those chunks back into the original file. This is particularly useful for handling files that exceed size limits for version control systems like Git, or for easier transfer.

## Features

* **Splitting:** Divides a large file into multiple smaller chunks of a specified size.
* **Combining:** Reassembles all chunks back into the original file.
* **Organized Output:** Creates a dedicated subfolder for the generated chunks in the current working directory.
* **Progress Indicator:** Displays real-time progress during both splitting and combining operations.
* **Platform Independent:** Works seamlessly on Windows, macOS, and Linux.
* **Relative Path Support:** Handles input file paths relative to the script's execution location.

## How It Works

When a file is split, a new directory named `[original_filename]_chunks` (e.g., `my_large_file.zip_chunks`) is created in the directory where the script is run. Inside this folder, chunks are named like `original_filename.chunk_0000`, `original_filename.chunk_0001`, and so on, ensuring proper ordering.

When combining, the script looks for this `_chunks` folder in the current working directory, gathers all the chunks, sorts them, and writes them sequentially to the specified output file.

## Getting Started

### Prerequisites

* Python 3.x installed on your system.

### Installation

1.  Save the provided Python code into a file named `file_splitter.py` (or any other `.py` name you prefer).
2.  Place this `file_splitter.py` script in a convenient directory on your system.

## Usage

Open your terminal or command prompt and navigate to the directory where you saved `file_splitter.py`.

### 1. Splitting a File

To split a large file into smaller chunks:

```bash
python file_splitter.py split <input_filepath> <chunk_size_mb>
````

  * `<input_filepath>`: The path to the large file you want to split. This can be an absolute path or a relative path (e.g., `./my_file.iso`, `../archives/backup.tar.gz`).
  * `<chunk_size_mb>`: The desired size of each chunk in megabytes (e.g., `90` for 90MB chunks).

**Example:**

```bash
python file_splitter.py split my_large_video.mp4 90
```

This command will:

  * Split `my_large_video.mp4` into approximately 90MB chunks.
  * Create a folder named `my_large_video.mp4_chunks` in your current working directory.
  * Place the chunks (e.g., `my_large_video.mp4.chunk_0000`, `my_large_video.mp4.chunk_0001`, etc.) inside this new folder.
  * Display a progress line like `Progress: X/Y chunks created...`

### 2\. Combining Files

To combine previously split file chunks back into the original file:

```bash
python file_splitter.py combine <output_filepath> <original_input_filepath_prefix>
```

  * `<output_filepath>`: The desired path and filename for the reassembled file (e.g., `recombined_video.mp4`).
  * `<original_input_filepath_prefix>`: The **original full path and filename** of the file that was *initially split* (e.g., `my_large_video.mp4`). The script uses this to locate the correct `_chunks` folder and identify the chunk files. **Ensure the `_chunks` folder is in the same directory where you run the combine command.**

**Example:**

```bash
python file_splitter.py combine new_full_video.mp4 my_large_video.mp4
```

This command will:

  * Look for the `my_large_video.mp4_chunks` folder in your current working directory.
  * Combine all chunks found within that folder.
  * Save the reassembled file as `new_full_video.mp4` in your current working directory.
  * Display a progress line like `Progress: X/Y chunks combined...`

## Important Notes

  * **File Integrity:** The script handles files in binary mode, preserving the integrity of any file type (archives, videos, executables, etc.).
  * **GitHub and Large Files:** While this script helps manage large files, for seamless integration with Git, consider using **Git Large File Storage (Git LFS)**. It's designed specifically for versioning large files efficiently without storing their full content directly in your Git repository.
  * **Web Interface (Advanced):** While a web interface is possible, hosting a service that combines and serves very large files (e.g., 4GB+) on cloud platforms like Render can be challenging due to server memory/CPU limits, ephemeral storage, and network bandwidth costs. A robust solution for a web interface would typically involve:
      * Using a **background worker/task queue** (like Celery) for the combination process to prevent web server timeouts.
      * Storing the combined large files in **dedicated object storage** (e.g., AWS S3, Google Cloud Storage, DigitalOcean Spaces) and providing pre-signed URLs for direct download, offloading the bandwidth from your web server.
      * Utilizing **persistent disks** on your hosting provider if you need the combined files to remain on the server's filesystem after restarts (this is usually a paid feature).
