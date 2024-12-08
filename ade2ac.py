import json
from pathlib import Path
import sys
import os
import shutil
import zipfile

# Here's a statement to determine whether you have Yaml or not
# They use the ANSI escape sequence for different colors
try:
    import yaml
except ImportError:
    print("Module \033[1mPyYaml\033[0m is not installed. \nPlease use \033[1;36mpip install pyyaml\033[0m to install it.")
    sys.exit()

args = sys.argv

difficulty_colors = ["#3A6B78FF", "#566947FF", "#482B54FF", "#7C1C30FF"]
skins = ["light", "conflict", "colorless"]
colors = {
    "trace": "#9178AA7A",
    "shadow": "#5A5A5A5A",
    "arc": [
        '#0CD4D4D9',
        '#FF96DCD9',
        '#23FF6CD9'
    ],
    "arcLow": [
        '#19A0EBD9',
        '#F0699BD9',
        '#28C81ED9'
    ]
}

proj_path = Path(args[1])

adeproj_path = proj_path / "Arcade" / "Project.arcade"

adeproj_exist = adeproj_path.is_file()

if adeproj_exist:
    with open(f"{proj_path}/Arcade/Project.arcade", "r", encoding='utf-8') as f:
        adeproj = json.load(f)
else:
    adeproj = {}

def default_text(key):
    if adeproj_exist:
        # If a person does not fill in a place, automatically returns nothing (means he/she should fill in one)
        if adeproj[key] == 'null':
            return ""
        else:
            return f"(Empty for: {adeproj[key]})"
    else:
        return ""


# This step fills in the audio name
audio = input("Audio file name: ")

# This step fills in the preview_start and preview_end and checks if they are legal or not
# We store the original (previous loop) data via a variable preview_start_backup
# This is to enable the following procedure (see note below)
preview_start = input("Preview start(Empty for 0): ")
preview_start_backup = preview_start

while 1:
    # Borrowing from preview_start here, when the value is "Pass" (case insensitive)
    # So if preview_start == pass, 
    #   we're going to reassign the value to preview_start by using preview_start_backup
    if preview_start == "pass" or preview_start == "Pass":
        preview_start = int(preview_start_backup)
        break
    elif preview_start == '':
        preview_start = 0
        preview_start_backup = 0
    else:
        preview_start = int(preview_start)
        preview_start_backup = preview_start

    preview_end = input("Preview end(Empty for 10000): ")
    if preview_end == '':
        preview_end = 10000
    else:
        preview_end = int(preview_end)
    
    #print(preview_start, preview_end, preview_end <= preview_start)

    # Here two quantities are tested
    # When they are not legal, the two quantities are re-entered.
    # We have a mandatory exit: 
    #   when there is an error in the determination, it will borrow preview_start as the exit: 
    #       force the exit when the preview_start is entered as "Pass" (case-insensitive)
    if preview_end <= preview_start:
        print("\n\nEntered the wrong number and please re-enter: \033[4mpreview_start should be less than preview_end\033[0m")
        print("If you are confident that you have not made a mistake, please fill in 'Pass' in the preview_start box below.\n")
        preview_start = input("Preview start(Empty for 0): ")
    else:
        break
#print(preview_start, preview_end); print(preview_end <= preview_start)

jacket = input("Jacket file name: ")
illustrator = input("Jacket illustrator: ")
bg_path = Path(input("Background Path: ").strip())
base_bpm = float(input(f"BaseBPM{default_text('BaseBpm')}: ") or default_text('BaseBpm') and adeproj['BaseBpm'])
base_bpm = base_bpm if base_bpm % 1 else int(base_bpm)
bpm_text = input(f"BPM Text(Empty for: {base_bpm}): ") or f"{base_bpm}"
title = input(
    f"Song title{default_text('Title')}: ") or default_text('Title') and adeproj['Title']
artist = input(
    f"Song Artist{default_text('Artist')}: ") or default_text('Artist') and adeproj['Artist']
charter = input("Charter: ")
skin = int(input("Skin(0, 1 or 2): "))

diffs_num = list(
    map(int, input("Containing Difficulties(Format:\"0 1 2 3\"): ").split(" ")))
diffs = ["", "", "", ""]

for i in diffs_num:
    if adeproj_exist:
        diff_text = str(adeproj['Difficulties'][i]['Rating'])
        df_text = f"(Empty for:{diff_text})"
    else:
        diff_text = ""
        df_text = ""
    diffs[i] = input(
        f"Difficulty Text {i}{df_text}: ") or diff_text

print("Confirm informations:")
print(f"Title: {title}")
print(f"Artist: {artist}")
print(f"Audio: {audio}")
print(f"Preview: {preview_start}-{preview_end}")
print(f"Jacket: {jacket}")
print(f"Illustrator: {illustrator}")
print(f"Background: {bg_path}")
print(f"BaseBPM: {base_bpm}")
print(f"BPMText: {bpm_text}")
print(f"Skin: {skins[skin]}")
print("Difficulties:")
for i in diffs_num:
    print(f"  {i}: {diffs[i]}")
input("Enter to continue...")

arcproj = {
    "lastOpenedChartPath": "CreateByArcCreatePackageConvertor.aff",
    "charts": []
}

for i in diffs_num:
    arcproj["charts"].append({
        "chartPath": f"{i}.aff",
        "audioPath": audio,
        "jacketPath": jacket,
        "baseBpm": base_bpm,
        "bpmText": bpm_text,
        "syncBaseBpm": True,
        "backgroundPath": bg_path.name,
        "title": title,
        "composer": artist,
        "charter": charter,
        "alias": "",
        "illustrator": illustrator,
        "difficulty": diffs[i],
        "difficultyColor": difficulty_colors[i],
        "skin": {
            "side": skins[skin],
            "singleLine": "none"
        },
        "colors": colors,
        "lastWorkingTiming": 0,
        "previewStart": preview_start,
        "previewEnd": preview_end
    })

package_name = input("Package name: ").lower()
select_identifier = input("Selection identifier: ").lower()
package_identifier = f"{select_identifier}.{package_name}"
print(f"Package identifier: {package_identifier}")

os.mkdir(f"./{package_name}")
os.mkdir(f"./{package_name}/{package_name}")
shutil.copy(Path(proj_path) / audio,
            Path(f"./{package_name}/{package_name}/"))
shutil.copy(Path(proj_path) / jacket,
            Path(f"./{package_name}/{package_name}/"))
shutil.copy(bg_path, Path(
    f"./{package_name}/{package_name}/"))
for i in diffs_num:
    shutil.copy(Path(proj_path) /
                f"{i}.aff", Path(f"./{package_name}/{package_name}/"))

index = [{
    "directory": package_name,
    "identifier": package_identifier,
    "settingsFile": "project.arcproj",
    "type": "level"
}]

with open(f"./{package_name}/{package_name}/project.arcproj", "w") as f:
    yaml.dump(arcproj, f)

with open(f"./{package_name}/index.yml", "w") as f:
    yaml.dump(index, f)

def zip_dir(dirname, zipfilename):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else:
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))

    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        zf.write(tar, arcname)
    zf.close()

zip_dir(f"./{package_name}", f"./{package_identifier}")

shutil.rmtree(f"./{package_name}")

print("Done!")
print(f"Output file: {Path(f'./{package_identifier}').absolute()}")