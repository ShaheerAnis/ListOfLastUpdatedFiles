import os
import datetime
import multiprocessing



def scan_directory(root):
    files = []
    for root, _, filenames in os.walk(root):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            print(file_path)
            try:
                mod_time = os.path.getmtime(file_path)
                print("Last updated Time : {mod_time}" )
            except FileNotFoundError as e:
                print(f"File not found: {file_path}")
                continue
            files.append((file_path, mod_time))
    print("Total files: " + len(files))
    return files



def get_last_modified_files(drive_letter, num_files=5):
    drive_path = f"{drive_letter}:\\"

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    try:
        results = pool.map(scan_directory, [drive_path] * multiprocessing.cpu_count())
    finally:
        pool.close()
        pool.join()

    files = [file for result in results for file in result]
    files.sort(key=lambda x: x[1], reverse=True)
    return [file[0] for file in files[:num_files]]

if __name__ == "__main__":
    drive_to_search = "E"  # Replace with the drive letter you want to search in (e.g., "C", "D", etc.)
    num_last_files = 5

    last_modified_files = get_last_modified_files(drive_to_search, num_last_files)
    print("---------------------------------------------------------------------")
    if last_modified_files:
        print(f"Last {num_last_files} modified files:")
        for idx, file_path in enumerate(last_modified_files, start=1):
            print(f"{idx}. {file_path}")
    else:
        print("No files found or drive does not exist.")
