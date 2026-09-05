from pathlib import Path
import shutil

FILE_TYPES = {
    "Images": [
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".heic", ".svg"
    ],
    "Videos": [
        ".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm"
    ],
    "Documents": [
        ".pdf", ".doc", ".docx", ".txt", ".rtf",
        ".xls", ".xlsx", ".csv",
        ".ppt", ".pptx"
    ],
    "Archives": [
        ".zip", ".rar", ".7z", ".tar", ".gz"
    ],
    "Music": [
        ".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg"
    ],
    "Programs": [
        ".exe", ".msi"
    ]
}


def get_category(file_path):
    extension = file_path.suffix.lower()

    for category, extensions in FILE_TYPES.items():
        if extension in extensions:
            return category

    return "Others"


def get_unique_destination(folder, file_name):
    destination = folder / file_name

    if not destination.exists():
        return destination

    original = Path(file_name)
    number = 1

    while True:
        new_name = f"{original.stem}_{number}{original.suffix}"
        destination = folder / new_name

        if not destination.exists():
            return destination

        number += 1


def organize_downloads():
    downloads = Path.home() / "Downloads"

    if not downloads.exists():
        print("Downloads folder was not found.")
        return

    print("Windows File Organizer")
    print("----------------------")
    print(f"Target folder: {downloads}")
    print()

    files = [
        item for item in downloads.iterdir()
        if item.is_file()
    ]

    if not files:
        print("No files found in Downloads.")
        return

    print(f"Files found: {len(files)}")
    print()

    for file in files:
        print(f"- {file.name}")

    print()
    confirmation = input(
        "Type YES to organize these files: "
    )

    if confirmation != "YES":
        print("Cancelled.")
        return

    moved = 0
    failed = 0

    for file in files:
        try:
            category = get_category(file)

            target_folder = downloads / category
            target_folder.mkdir(exist_ok=True)

            destination = get_unique_destination(
                target_folder,
                file.name
            )

            shutil.move(
                str(file),
                str(destination)
            )

            print(
                f"{file.name} -> {category}"
            )

            moved += 1

        except Exception as error:
            print(
                f"Failed: {file.name} | {error}"
            )
            failed += 1

    print()
    print("----------------------")
    print("Finished")
    print(f"Moved: {moved}")
    print(f"Failed: {failed}")


if __name__ == "__main__":
    organize_downloads()
