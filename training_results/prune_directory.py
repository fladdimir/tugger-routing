import os
import glob
import shutil

dir_path = os.path.dirname(os.path.realpath(__file__))

EXCLUDE = ["prune_directory.py", "plot_monitor.py", "plot_all.py"]

contents = [
    fn
    for fn in glob.glob(dir_path + "/**")
    if not any(os.path.basename(fn).startswith(ex) for ex in EXCLUDE)
]
for f in contents:
    try:
        shutil.rmtree(f)  # directory?
    except:
        try:
            os.remove(f)  # file?
        except:
            raise Exception("neither file nor directory: " + f)

print("deleted contents from: " + dir_path)
