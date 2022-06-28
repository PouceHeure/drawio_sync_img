#!/usr/bin/python3

import xml.etree.ElementTree as ET
import argparse
import os


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

def sync_img(drawio_file,output_folder,sync_all_pages=False,page_to_sync=-1,format="png"):

    if(not sync_all_pages and page_to_sync == -1): 
        print("sync impossible, chose all pages or a specific page")
        return -1

    pages = extract_pages_name_information(drawio_file)
    if(not sync_all_pages): 
        if(pages.get(page_to_sync) == None):
            print("sync impossible, page number unknown")
            return -1
        else:
            pages = {page_to_sync: pages[page_to_sync]}

    for page_num, page_name in pages.items(): 
        path_img = os.path.join(output_folder,f"{page_name}.{format}")
        os.system(f"drawio -x {drawio_file} -o {path_img} -p {page_num} -format {format}")
    
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

    succes = sync_img(drawio_file=args.file,
            output_folder=args.output,
            sync_all_pages=args.all_pages,
            page_to_sync=args.page)

    exit(succes)

    
    

    

    