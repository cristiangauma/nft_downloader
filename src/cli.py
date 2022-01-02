import os
import sys
import argparse
from nft_downloader import nft_downloader

def running_in_docker() -> bool:
    path = '/proc/self/cgroup'
    return (
        os.path.exists('/.dockerenv') or
        os.path.isfile(path) and any('docker' in line for line in open(path))
    )

def define_default_output_dir() -> str:
    if running_in_docker():
        return '/downloads'
    else:
        return os.path.dirname(os.path.realpath(__file__))

def define_default_list_file_path() -> str:
    if running_in_docker():
        return '/nft_list.txt'
    else:
        return 'ntf_list.txt'

def read_nft_list_file(list_file_path: str) -> list:
    with open(list_file_path, 'r') as f:
        lines = f.readlines()

    return lines

def delete_line_from_file(list_file_path: str, line: str) -> None:
    with open(list_file_path, 'r') as f:
        lines = f.readlines()

    with open(list_file_path, 'w') as f:
        for l in lines:
            if l != line:
                f.write(l)

if __name__ == '__main__':
    #
    # Parse command line arguments
    #
    parser = argparse.ArgumentParser(description='Download NFTs from foundation.app or opensea.io')
    parser.add_argument('-u', '--url', type=str, help='URL to download', required=False, default=None)
    parser.add_argument('-o', '--output', type=str, help='Output directory', required=False, default=define_default_output_dir())
    parser.add_argument('-l', '--list-file', type=str, help='List file path of NFTs URLs', required=False, default=define_default_list_file_path())
    args = parser.parse_args()

    
    nft_list = []
    if args.url:
        nft_list.append(args.url)
    else:
        nft_list_file_path = args.list_file
        if not os.path.exists(nft_list_file_path):
            print("\n\nError: URL not specified and list file does not exist: " + nft_list_file_path)
            sys.exit(1)

        #
        # Read nft_list.txt and create instances of nft_downloader for each line of the file
        #
        nft_list = read_nft_list_file(nft_list_file_path)
    
    for nft_url in nft_list:
        downloader = nft_downloader(nft_url, args.output)
        successfull = downloader.start()
        if successfull:
            #
            # Delete line from nft_list.txt
            #
            nft_list.remove(nft_url)
            delete_line_from_file(nft_list_file_path, nft_url)

    #
    # Show the remaining URLs that could not be downloaded
    #
    if len(nft_list) > 0:
        print("\n\nSome of the NFTs could not be downloaded. Please check the following URLs:")
        for nft_url in nft_list:
            print(nft_url)

    sys.exit(0)