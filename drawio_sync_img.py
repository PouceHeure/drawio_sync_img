#!/usr/bin/python3

import os
import argparse
import xml.etree.ElementTree as ET

def extract_pages_name_information(drawio_file):
    """extract pages name from drawio xml file

    Args:
        drawio_file (str): drawio_file

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

def sync_img(drawio_file,output_folder,sync_all_pages=False,page_to_sync=-1,format="png",kwargs={}):
    # sync possible ?
    if(not sync_all_pages and page_to_sync == -1): 
        print("sync impossible, chose all pages or a specific page")
        return -1
    # get information per page
    pages = extract_pages_name_information(drawio_file)
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
    # run cmd per page
    for page_num, page_name in pages.items(): 
        path_img = os.path.join(output_folder,f"{page_name}.{format}")
        cmd = f"drawio -x {drawio_file} -o {path_img} -p {page_num} -format {format} {kwargs_cmd}"
        os.system(cmd)
    return 0
    

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="drawio to sync",
                        type=str, required=True)
    parser.add_argument("-o", "--output", help="folder",
                        type=str,default="")
    parser.add_argument("-a", "--all-pages", help="sync all pages",
                        action="store_true",default=True)
    parser.add_argument("-p", "--page", help="sync specific page",
                        type=int,default=-1)

    args, unknown = parser.parse_known_args()
        
    if(args.page != -1):
        args.all_pages = False

    unknown_args = {}
    for i in range(0,len(unknown),2):
        unknown_args[unknown[i]] = unknown[i+1]

    succes = sync_img(drawio_file=args.file,
            output_folder=args.output,
            sync_all_pages=args.all_pages,
            page_to_sync=args.page,
            kwargs=unknown_args)

    exit(succes)

    
    

    

    