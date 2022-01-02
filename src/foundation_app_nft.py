import re
import sys
import requests

class FoundationAppNFT:
    def __init__(self, listing_url: str) -> None:
        self.listing_url = listing_url
        self.creator = self._get_foundation_app_user_from_listing_url()

        self.metadata_json = self._download_foundation_app_metadata_json()
        self._set_nft_characteristics()
        
    #
    # Set the NFT characteristics
    #
    def _set_nft_characteristics(self) -> None:
        self.name = self.metadata_json['name'].replace('/', '-').rstrip()
        self.description = self.metadata_json['description']
        self.links = {
            'listing_url': self.listing_url,
            'url': self.metadata_json['image'].replace('ipfs://', 'https://ipfs.io/ipfs/'),
            'ipfs': self.metadata_json['image']
        }
        self.format = self.links['url'].split('.')[-1]

    #
    # Parse the foundation.app URL and return the user
    #
    def _get_foundation_app_user_from_listing_url(self) -> str:
        parser = re.search(r'https://foundation.app/([^/]+)', self.listing_url)
        if parser:
            if '@' in parser.group(1):
                return parser.group(1)
        
        print("\n\nError: Invalid foundation.app URL or user not found in URL: " + self.listing_url)
        sys.exit(1)

    #
    # Extract the href link from a page source that matches the patter ipfs.io/ipfs/*/metadata.json
    #
    def _get_foundation_app_metadata_url_from_listing_url(self) -> str:
        source = requests.get(self.listing_url).text
        metadata_url = re.search(r'https://ipfs.io/ipfs/.*?/metadata.json', source)
        if metadata_url:
            return metadata_url.group(0)
        else:
            print("\n\nError: Failed to find metadata.json URL in the foundation.app URL: " + self.listing_url)
            sys.exit(1)

    #
    # Download foundation.app metadata.json file
    #
    def _download_foundation_app_metadata_json(self) -> dict:
        metadata_url = self._get_foundation_app_metadata_url_from_listing_url()
        response = requests.get(metadata_url)
        if response.status_code == 200:
            return response.json()
        else:
            print("\n\nError: Failed to download foundation.app metadata.json: " + metadata_url)
            sys.exit(1)
    
    #
    # Print summary of the foundation.app metadata
    #
    def _print_summary(self) -> None:
        print("\t - Foundation.app metadata summary:" + '\n')
        print("\t\t*********************************************************")
        print("\t\t\t* Foundation.app URL: " + self.listing_url + '\n')
        print("\t\t\t* Foundation.app User: " + self.creator + '\n')
        print("\t\t\t* NFT Name: " + self.name + '\n')
        print("\t\t\t* NFT Format: " + self.format + '\n')
        print("\t\t\t* NFT Description: " + self.description.replace('\n', '\n\t\t                   ')+ '\n')
        print("\t\t\t* NFT IPFS: " + self.links['ipfs'] + '\n')
        print("\t\t\t* NFT IPFS URL: " + self.links['url'] + '\n')
        print("\t\t*********************************************************" + '\n')