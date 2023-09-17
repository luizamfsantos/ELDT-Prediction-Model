import requests

class APIClient:
    def __init__(self, base_url, token_file):
        self.base_url = base_url
        self.token = self.load_token(token_file)

    def load_token(self, token_file):
        """
        Load API token from a text file.

        Args:
            token_file (str): The path to the text file containing the API token.

        Returns:
            str: The API token.
        """
        try:
            with open(token_file, "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            # Handle the case where the token file is not found
            print("Token file not found.")
            return None

    def make_request(self, endpoint, method="GET", params=None, data=None, headers=None):
        """
        Make a request to the REST API with the loaded token.

        Args:
            endpoint (str): The API endpoint to request.
            method (str): The HTTP method for the request (e.g., GET, POST, PUT, DELETE).
            params (dict): Query parameters to include in the request.
            data (dict): Request body data for POST or PUT requests.
            headers (dict): Additional headers to include in the request.

        Returns:
            dict: The JSON response from the API.
        """
        url = f"{self.base_url}/{endpoint}"

        if self.token:
            if headers is None:
                headers = {}
            headers["Authorization"] = f"Bearer {self.token}"

        try:
            response = requests.request(
                method,
                url,
                params=params,
                data=data,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            # Handle exceptions or errors here
            print(f"Request error: {e}")
            return None

# Example usage:
if __name__ == "__main__":
    base_url = "http://montreal.icea.decea.mil.br:5002/api/v1"
    token_file = "../virtual_token.txt"  # MODIFY THIS FOR YOUR TOKEN FILE
    api = APIClient(base_url, token_file)

    # Example GET request
    response = api.make_request("endpoint")

    if response:
        # Process the response data here
        print(response)
