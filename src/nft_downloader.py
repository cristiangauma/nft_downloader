import os
import sys
import json
import time
import requests

from typing import Union
from foundation_app_nft import FoundationAppNFT
from opensea_io_nft import OpenseaIoNFT

class nft_downloader:
    def __init__(self, url: str, output_directory: str) -> None:
        self.url = url
        self.base_dir = output_directory
        self.provider_domain = self._get_provider_domain_from_url().replace('.', '_')
        self.nft = self._get_nft_information()
        

    #
    # Get all NFT information using the NFT URL
    #
    def _get_nft_information(self) -> Union[FoundationAppNFT, None]:
        if 'foundation.app' in self.url:
            return FoundationAppNFT(self.url)
        elif 'opensea.io' in self.url:
            return OpenseaIoNFT(self.url)
        else:
            print("\n\nError: Invalid URL: " + self.url)
            sys.exit(1)

    #
    # Get the provider domain from the URL
    #
    def _get_provider_domain_from_url(self) -> str:
        if 'foundation.app' in self.url:
            return 'foundation.app'
        elif 'opensea.io' in self.url:
            return 'opensea.io'
        else:
            print("\n\nError: Invalid URL: " + self.url)
            sys.exit(1)

    #
    # Set the download outputs
    #
    def _set_download_outputs(self) -> None:
        if self.base_dir:
            if os.path.exists(self.base_dir):
                self.output_dir = self.base_dir + '/' + self.provider_domain + '/' + self.nft.creator + '/' + self.nft.name
            else:
                print("\n\nError: Invalid base dir path, it does not exist: " + self.base_dir)
        else:
            self.output_dir = os.path.dirname(os.path.realpath(__file__)) + '/' + self.provider_domain + '/' + self.nft.creator + '/' + self.nft.name

        self.output_file_name = self.nft.name + '.' + self.nft.format
        self.output_metadata_file_name = 'metadata.json'
        self.output_markdown_file_name = 'README.md'

        self.output_file_path = self.output_dir + '/' + self.output_file_name
        self.output_metadata_file_path = self.output_dir + '/' + self.output_metadata_file_name
        self.output_readme_file_path = self.output_dir  + '/' + self.output_markdown_file_name

    #
    # Download NFT to the directory showing a progress bar
    #
    def _download_nft(self, retry: int = 0, max_retry: int = 5) -> None:
        print(f"\t - Downloading NFT (retry {retry}): " + self.nft.links['url'])
        if retry < max_retry:
            try:
                response = requests.get(self.nft.links['url'], stream=True)
                
                total_length = 0
                with open(self.output_file_path, 'wb') as out_file:
                    total_length = response.headers.get('content-length')

                    if total_length is None:
                        out_file.write(response.content)
                    else:
                        downloaded = 0
                        total_length = int(total_length)
                        for data in response.iter_content(chunk_size=4096):
                            downloaded += len(data)
                            out_file.write(data)
                            done = int(50 * downloaded / total_length)
                            sys.stdout.write(f"\r\t   [{'=' * done}{' ' * (50-done)}]")
                            sys.stdout.flush()
                        print("\n")
            
                if not os.path.exists(self.output_file_path) or (total_length != os.stat(self.output_file_path).st_size):
                    if retry < max_retry:
                        print("\t   Failed!. Will try to download it again in 5 seconds.")
                        time.sleep(5)
                        self._download_nft(retry + 1)
            
            except Exception as e:
                print(f"\t   Failed!. Will try to download it again in 5 seconds.\n")
                time.sleep(5)
                self._download_nft(retry + 1)

        else:
            print("\t   Error: Failed to download NFT: " + self.nft.links['url'])

    #
    # Create output directory
    #
    def _create_output_dir(self) -> None:
        print("\t - Creating directory: " + self.output_dir + '\n')
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    #
    # Convert metadata dictionary to a readable markdown
    #
    def _write_readme_md(self) -> None:
        print("\t - Converting metadata to markdown and writing to README.md: " + self.output_readme_file_path + '\n')
        with open(self.output_readme_file_path, 'w') as file:
            file.write('# ' + self.nft.name + '\n')
            file.write(self.nft.description + '\n')
            file.write('\n')
            file.write('## NFT Links \n')
            for link_description, link in self.nft.links.items():
                file.write(' - ' + link_description + ': ' + link + '\n\n')
    
    #
    # Writing raw metadata to the directory
    #
    def _write_metadata(self) -> None:
        print("\t - Writing metadata to: " + self.output_metadata_file_path + '\n')
        with open(self.output_metadata_file_path, 'w') as file:
            json.dump(self.nft.metadata_json, file, indent=4)

    #
    # Used only for output readability purposes
    #
    def _print_hard_line(self) -> None:
        print('\n' + "###############################################################################" + '\n')

    #
    # Download NFT
    #
    def start(self) -> bool:
        self._print_hard_line()

        print("\t - New listing_url detected: " + self.nft.listing_url + '\n')
        self.nft._print_summary()
        self._set_download_outputs()
        self._create_output_dir()
        self._download_nft()        
        self._write_metadata()
        self._write_readme_md()
        print("\t - NFT downloaded successfully!" + '\n')
        
        self._print_hard_line()

        return True