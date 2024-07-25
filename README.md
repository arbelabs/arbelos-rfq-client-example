# arbelos-rfq-client-example

## Usage

To use the API client, you need your public and private API keys. These can be obtained by contacting clientsupport@arbelos.xyz. Make sure to store these keys securely and do not hard-code them in your codebase.

## Endpoints
- Check Authentication: /status
- Get Tradable Instruments: /instruments
- Get Quotes: /quotes
- Execute Trade: /trade
- Get Balances: /balances
- List Trades: /trades
- Get Trading Volume Info: /volumes

For detailed specifications, please refer to the Arbelos RFQ API Specification PDF.

## Authentication
The API uses HMAC signatures for authentication. Ensure that your API requests include the following headers:

- x-api-key: Your public API key.
- x-signature: A signature generated using your private API key and the request parameters.

## Generating Signatures
To generate a signature, sort the request parameters alphabetically, concatenate them into a string, hash the string using SHA-256, and sign it using your private key. This is handled for you within the provided example.

## Rate Limits and Quotas
- Rate Limits: 10 requests per second.
- Burst Limits: 5 requests per second.
- Daily Quota: 10,000 requests per day.

## Contact
For any questions or issues, please contact clientsupport@arbelos.xyz.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
