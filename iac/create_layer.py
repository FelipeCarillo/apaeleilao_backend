import os
import shutil


def create_layer_directory():
    source_directory = "../src/shared"
    target_directory = os.path.join(os.getcwd(), "apaeleilao_layer")

    try:
        shutil.copytree(source_directory, target_directory)
        print("Directory copied successfully.")
    except shutil.Error as e:
        print("Error: %s" % e)
    except OSError as e:
        print("Error: %s" % e)
