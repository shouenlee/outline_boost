import subprocess
import os
import sys
import shutil
 
default_build_artifact_directory = "aarch64-unknown-linux-gnu"

def build_swift(directory, clean):
    try:
        # Change the current working directory to the specified directory
        os.chdir(directory)

        # if clean is True, then delete previous build artifacts
        if clean:
            print("Deleting previous builds.")
            subprocess.run(["rm", "-rf", ".build"], stdout = subprocess.DEVNULL)

        # Run the swift build command
        result = subprocess.run(["swift", "build", "-c", "release"], stdout = subprocess.DEVNULL)
        print(f"Build succeeded for {directory}!")

        # move binaries to Release folder
        source = f".build/{default_build_artifact_directory}/release/{directory}"
        destination = "../Release"

        # check if source file exists
        if not os.path.exists(source):
            raise FileNotFoundError(f"Source file: {source} does not exist.")
        if os.path.exists(f"{destination}/{directory}"):
            os.remove(f"{destination}/{directory}")

        shutil.copy(source, destination)
        print(f"{directory} has been moved to {destination}")

    except subprocess.CalledProcessError as e:
        print(f"Build failed in {directory}!")
        print(e.stderr)
    except FileNotFoundError as e:
        print(f"Directory '{destination}' not found!", {e})
    except Exception as e:
        print(f"An unexpected error occurred in {directory}: {e}")
    finally:

        # Change back to the original directory
        os.chdir("..")

clean = False
args = sys.argv[1:]
if len(args) > 0 and args[0] == '-c':
    clean = True


for dir_name in ["verse_requestor", "verse_search"]:
    build_swift(dir_name, clean)
 
 
