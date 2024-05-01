import os

def create_unique_directory():
  # Directory name
  directory_name = "unique"

  # Path
  path = os.path.join(os.getcwd(), directory_name)

  # Create the directory in the current directory
  try:
      os.mkdir(path)
      print(f"Directory '{directory_name}' created")
  except FileExistsError:
      print(f"Directory '{directory_name}' already exists")