import re
import sys
import json
import requests

class OpenseaIoNFT:
    def __init__(self, listing_url: str) -> None:
        self.listing_url = listing_url
        self.asset_id = self._get_asset_id_from_listing_url()

        self.metadata_json = self._download_opensea_io_metadata_json()
        self.creator = self._get_creator_from_metadata_json()
        self._set_nft_characteristics()

    #
    # Get the creator from the OpenSea.io json file
    #
    def _get_creator_from_metadata_json(self) -> str:
        if self.metadata_json['creator']['user']['username']:
            return self.metadata_json['creator']['user']['username']
        else:
            print(f"\t - Failed to find creator in opensea.io json information: {self.metadata_json}")
            sys.exit(1)

    #
    # Download OpenSea.io asset json from OpenSea.io API
    #
    def _download_opensea_io_metadata_json(self) -> dict:
        api_url = f"https://api.opensea.io/api/v1/asset/{self.asset_id}"
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"\t - Failed to download opensea.io metadata.json: {api_url}")
            sys.exit(1)

    #
    # Get OpenSea.io asset id from the OpenSea.io URL
    #
    def _get_asset_id_from_listing_url(self) -> str:
        parser = re.search(r'https://opensea.io/assets/(.*)', self.listing_url)
        if parser:
            return parser.group(1)
    
    #
    # Set the NFT characteristics
    #
    def _set_nft_characteristics(self) -> None:
        if self.metadata_json['name']:
            self.name = self.metadata_json['name'].replace('/', '-').rstrip()
        else:
            self.name = self.asset_id.replace('/', '-').rstrip()

        if self.metadata_json['description']:
            self.description = self.metadata_json['description']
        else:
            self.description = 'No description provided'
        
        if self.metadata_json['image_original_url'] and 'ipfs.io/ipfs' in self.metadata_json['image_original_url']:
            url = self.metadata_json['image_original_url']
        else:
            url = self.metadata_json['image_url'] + '=s0'

        self.links = {
            'listing_url': self.listing_url,
            'url': url,
        }

        url_headers = requests.head(self.links['url']).headers
        self.format = url_headers.get('Content-Type', "nope/nope").split("/")[1]

    #
    # Print summary of the opensea.io metadata
    #
    def _print_summary(self) -> None:
        print("\t - Opensea.io metadata summary:" + '\n')
        print("\t\t*********************************************************")
        print("\t\t\t* Opensea.io URL: " + self.listing_url + '\n')
        print("\t\t\t* Opensea.io User: " + self.creator + '\n')
        print("\t\t\t* NFT Name: " + self.name + '\n')
        print("\t\t\t* NFT Format: " + self.format + '\n')
        print("\t\t\t* NFT Description: " + self.description.replace('\n', '\n\t\t                   ')+ '\n')
        print("\t\t\t* NFT URL: " + self.links['url'] + '\n')
        print("\t\t*********************************************************" + '\n')