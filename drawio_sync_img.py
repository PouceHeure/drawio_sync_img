#!/usr/bin/python3

import os
import argparse
import xml.etree.ElementTree as ET

def extract_pages_name_information_from_drawio_file(drawio_file):
    """extract pages name from drawio xml file

    Args:
        drawio_file (str): drawio_file path

    Returns:
        dict: {page_number:page_name}
    """
    tree = ET.parse(drawio_file)
    root = tree.getroot()
    pages = {}
    page_n = 0
    for child in root:
        pages[page_n] = child.attrib["name"]
        page_n += 1
    return pages

def sync_img_from_drawio_file(drawio_file,output_folder,
                        sync_all_pages=False,
                        page_to_sync=-1,
                        format="png",
                        kwargs={}):
    """
    Synhronize images from drawio file.
    Args:
        drawio_file (str): drawio file path
        output_folder (str): output folder where image will be saved
        sync_all_pages (bool, optional): force all images to be saved. Defaults to False.
        page_to_sync (int, optional):  specific the page number to save. Defaults to -1.
        format (str, optional): format img generated. Defaults to "png".
        kwargs (dict, optional): others args to give to 'drawio' cmd. Defaults to {}.

    Returns:
        _type_: _description_
    """
    # sync possible ?
    if(not sync_all_pages and page_to_sync == -1): 
        print("sync impossible, chose all pages or a specific page")
        return -1
    # get information per page
    pages = extract_pages_name_information_from_drawio_file(drawio_file)
    # sync one page, check page exist
    if(not sync_all_pages): 
        if(pages.get(page_to_sync) == None):
            print("sync impossible, page number unknown")
            return -1
        else:
            pages = {page_to_sync: pages[page_to_sync]}
    # adapt other args
    kwargs_cmd = ""
    for arg, value in kwargs.items():
        kwargs_cmd += f"{arg} {value} "
    # check if the output folder exist 
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # run cmd per page
    for page_num, page_name in pages.items(): 
        path_img = os.path.join(output_folder,f"{page_name}.{format}")
        cmd = f"drawio -x {drawio_file} -o {path_img} -p {page_num} -format {format} {kwargs_cmd}"
        os.system(cmd)
    return 0
    

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="drawio file to sync",
                        type=str, required=True)
    parser.add_argument("-o", "--output", help="folder where image will be saved",
                        type=str,default="")
    parser.add_argument("-a", "--all-pages", help="sync all pages from the drawio file",
                        action="store_true",default=True)
    parser.add_argument("-p", "--page", help="sync specific page number from the drawio file",
                        type=int,default=-1)

    args, unknown = parser.parse_known_args()
        
    if(args.page != -1):
        args.all_pages = False

    unknown_args = {}
    for i in range(0,len(unknown),2):
        unknown_args[unknown[i]] = unknown[i+1]

    succes = sync_img_from_drawio_file(drawio_file=args.file,
            output_folder=args.output,
            sync_all_pages=args.all_pages,
            page_to_sync=args.page,
            kwargs=unknown_args)

    exit(succes)