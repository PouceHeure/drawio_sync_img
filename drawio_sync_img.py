#!/usr/bin/python3

import os
import yaml
import argparse
import xml.etree.ElementTree as ET
import threading
import hashlib


# methods: get information about drawio document


def extract_pages_information_from_drawio_file(drawio_file):
    """extract pages information from drawio xml file
    Args:
        drawio_file (str): drawio_file path

    Returns:
        dict: information about document
    """
    tree = ET.parse(drawio_file)
    root = tree.getroot()
    pages = {}
    page_n = 0
    for child in root:
        pages[page_n] = {}
        pages[page_n]["name"] = child.attrib["name"]
        pages[page_n]["hash"] = int(hashlib.sha1(
            child.text.encode('utf-8')).hexdigest(), 16)
        page_n += 1
    return pages


# methods: execute command


def execute_pool_commands(cmds):
    """save pages into images from cmd instructions

    Args:
        cmds (list(str)): list of cmd to execute 
    """
    for cmd in cmds:
        os.system(cmd)


# methods: sync


def define_sync_file_path(drawio_file):
    drawio_file_name = os.path.splitext(os.path.basename(drawio_file))[0]
    drawio_folder = os.path.dirname(drawio_file)
    sync_file_name = f".sync.{drawio_file_name}.yaml"
    return os.path.join(drawio_folder, sync_file_name)


def save_sync_information(sync_information_file, pages_information):
    with open(sync_information_file, 'w') as outfile:
        yaml.dump(pages_information, outfile, default_flow_style=False)


def load_sync_information(sync_information_file):
    data = None
    if(not os.path.exists(sync_information_file)):
        return {}
    with open(sync_information_file) as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    return data


# methods: utils


def devide_list_into_n_sublists(raw_list, n_sublists):
    sublists = [[] for _ in range(n_sublists)]
    for i in range(len(raw_list)):
        sublists[i % n_sublists].append(raw_list[i])
    return sublists

# methods: pipeline


def sync_img_from_drawio_file(drawio_file, output_folder,
                              sync_all_pages=False,
                              page_to_sync=-1,
                              format="png",
                              n_threads=4,
                              force_sync=False,
                              kwargs={}):
    """
    Synhronize images from drawio file.
    Args:
        drawio_file (str): drawio file path
        output_folder (str): output folder where image will be saved
        sync_all_pages (bool, optional): force all images to be saved. Defaults to False.
        page_to_sync (int, optional):  specific the page number to save. Defaults to -1.
        format (str, optional): format img generated. Defaults to "png".
        n_threads (int, optional): threads number. Defaults to 4.
        force_sync (bool, optional): force sync even the img is already update. Defaults to False.
        kwargs (dict, optional): others args to give to 'drawio' cmd. Defaults to {}.

    Returns:
        int: success
    """
    # sync possible ?
    if(not sync_all_pages and page_to_sync == -1):
        print("sync impossible, chose all pages or a specific page")
        return -1
    sync_file_path = define_sync_file_path(drawio_file)
    previous_sync_information = load_sync_information(
        sync_information_file=sync_file_path)
    # get information per page
    pages_information = extract_pages_information_from_drawio_file(drawio_file)
    # sync one page, check page exist
    if(not sync_all_pages):
        page_to_sync_information = pages_information.get(page_to_sync) 
        if(page_to_sync_information == None):
            print("sync impossible, page number unknown")
            return -1
        else:
            pages_information = {page_to_sync: page_to_sync_information}
    # adapt other args
    kwargs_cmd = ""
    for arg, value in kwargs.items():
        kwargs_cmd += f"{arg} {value} "
    # check if the output folder exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # create all cmds (1 cmd per page)
    cmds = []
    for page_num, page_information in pages_information.items():
        page_name = page_information["name"]
        path_img = os.path.join(output_folder, f"{page_name}.{format}")
        page_information["path"] = os.path.join(os.getcwd(), path_img)
        page_was_updated = previous_sync_information.get(
            page_num) != page_information
        # sync only if the image isn't sync (or in force mode)
        if(force_sync or page_was_updated):
            cmd = f"drawio -x {drawio_file} -o \"{path_img}\" -p {page_num} -format {format} {kwargs_cmd}"
            cmds.append(cmd)
    # handle case where n_threads is upper then len(pages)
    n_threads = min(n_threads, len(pages_information))
    # define cmds by thread
    cmds_by_thread = devide_list_into_n_sublists(cmds, n_sublists=n_threads)
    threads = []
    # create thread and start it
    for i_thread in range(n_threads):
        thread = threading.Thread(
            target=execute_pool_commands, args=(cmds_by_thread[i_thread],))
        threads.append(thread)
        thread.start()
    # join threads
    for thread in threads:
        thread.join()
    save_sync_information(sync_file_path, pages_information)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="drawio file to sync",
                        type=str, required=True)
    parser.add_argument("-o", "--output", help="folder where image will be saved",
                        type=str, default="")
    parser.add_argument("-a", "--all-pages", help="sync all pages from the drawio file",
                        action="store_true", default=True)
    parser.add_argument("-p", "--page", help="sync specific page number from the drawio file",
                        type=int, default=-1)
    parser.add_argument("-t", "--threads", help="threads number",
                        type=int, default=4)
    parser.add_argument("--force", help="force sync all images",
                        action="store_true", default=False)

    args, unknown = parser.parse_known_args()

    if(args.page != -1):
        args.all_pages = False

    unknown_args = {}
    for i in range(0, len(unknown), 2):
        unknown_args[unknown[i]] = unknown[i+1]

    succes = sync_img_from_drawio_file(drawio_file=args.file,
                                       output_folder=args.output,
                                       sync_all_pages=args.all_pages,
                                       page_to_sync=args.page,
                                       n_threads=args.threads,
                                       force_sync=args.force,
                                       kwargs=unknown_args)

    exit(succes)