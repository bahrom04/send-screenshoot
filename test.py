import os
import sys

title = "plan_Designing_lecture"
sliced_title = title.replace("plan_", "", 1)  # The '1' means only replace the first occurrence
print(sliced_title)


file_name = os.path.join("rasm/", os.path.basename("photo/file.jpg"))
print(file_name)

