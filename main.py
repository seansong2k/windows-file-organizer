from pathlib import Path
import shutil

FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".pptx"],
    "Archives": [".zip", ".rar", ".7z"],
    "Music": [".mp3", ".wav", ".flac"],
}


def get_category(filename):
    extension = Path(filename).suffix.lower()

    for category, extensions in FILE_TYPES.items():
        if extension in extensions:
            return category

    return "Others"


def organize(folder):
    folder = Path(folder)

    for file in list(folder.iterdir()):
        if not file.is_file():
            continue

        category = get_category(file.name)

        target_folder = folder / category
        target_folder.mkdir(exist_ok=True)

        destination = target_folder / file.name

        number = 1
        while destination.exists():
            destination = target_folder / f"{file.stem}_{number}{file.suffix}"
            number += 1

        shutil.move(str(file), str(destination))

        print(f"{file.name} -> {category}")


test_folder = Path("test_files")
test_folder.mkdir(exist_ok=True)

test_files = [
    "photo.jpg",
    "picture.png",
    "homework.pdf",
    "document.docx",
    "movie.mp4",
    "music.mp3",
    "backup.zip",
    "program.exe",
]

for filename in test_files:
    file_path = test_folder / filename

    if not file_path.exists():
        file_path.write_text("test file", encoding="utf-8")


print("Before:")

for file in test_folder.iterdir():
    print(" -", file.name)


print("\nOrganizing...\n")

organize(test_folder)


print("\nDone.")
print("\nFolders:")

for folder in test_folder.iterdir():
    if folder.is_dir():
        print(f"\n{folder.name}/")

        for file in folder.iterdir():
            print("   ", file.name)
