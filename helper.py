import os
import random



'''''
extensions = [".mp4", ".webm", "mkv"]

endpath = "../repositories/container_"
target_path = "../playlist/"
sentence_1 = "cd " + target_path
sentence_2 = " && mv"
for ext in extensions:
    sentence_2 += " *" + ext
sentence_2 += " " + endpath
'''''