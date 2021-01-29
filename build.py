import os

os.environ["environment"] = "environment"

if not os.path.isdir(os.environ["environment"]):
    os.system("virtualenv " + os.environ["environment"])

os.system("bash install")
