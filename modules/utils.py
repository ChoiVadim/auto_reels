import os
import shutil
import colorama


def delete_all_files_in_directory(directory_path):
    if os.path.exists(directory_path):
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(e)
    else:
        print(f"Directory {directory_path} does not exist")


def progress_bar(
    iteration,
    total,
    prefix="",
    suffix="",
    decimals=1,
    length=80,
    fill="█",
    printEnd="\r",
):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + "-" * (length - filledLength)

    print(
        colorama.Fore.YELLOW + f"\r{prefix} |{bar}| {percent}% {suffix}",
        end=printEnd,
    )

    if iteration == total:
        print(
            colorama.Fore.GREEN + f"\r{prefix} |{bar}| {percent}% {suffix}",
            end=printEnd,
        )
        print(colorama.Fore.RESET)
