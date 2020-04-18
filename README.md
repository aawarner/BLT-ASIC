[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/aawarner/BLT-ASIC)

# Brownfield Licensing Tool

Brownfield Licensing tool is a tool to assist with gathering entitlement information and licensing devices 
for customers migrating to Cisco Smart Licensing. 


## Business/Technical Challenge
Customers who are upgrading software often find that they are now required to use Cisco Smart Licensing.
Upon completing the upgrade they realize that they do not have a Cisco Smart License in their Cisco
Smart account for the device they just upgraded. For customers who can take advantage of Device Led
Conversion this may not be a problem. However, customers who can not take advantage of Device Led Conversion 
(as is the case with many customers) will need to open a case with Cisco Global Licensing Operations (GLO). When opening a
case the customer will be required to provide the sales order numbers for the devices being upgraded. Often the 
only information the customer has is the serial number of the device. Sales orders are often not maintained by the customer 
but are required when trying to prove the level of entitlement.

## Proposed Solution

The proposed solution is to leverage three techniques to gather entitlement information for creation of licensing cases
with GLO.

1) Live scan of netework connected devices for serial number retrieval
2) Search of serial number either inputed to a webpage or imported in the form of a .CSV
3) Search of a sales order number inputed to a webpage

### Cisco Products Technologies/ Services

Our solution will leverage the following Cisco technologies

* [Cisco Commerce Workspace Order API](https://apiconsole.cisco.com)
* [Cisco Commerce Subscriptions and Software Contract Administration API](https://apiconsole.cisco.com)
* [Cisco IOS-XE](https://www.cisco.com/c/en/us/products/ios-nx-os-software/ios-xe/index.html)

## Team Members

* Aaron Warner <aawarner@cisco.com> - US Public Sector
* Kris Swanson <kriswans@cisco.como> - US Public Sector
* Justin Poole <jupoole@cisco.com> - Global Enterprise


## Solution Components

Python\
Cisco-UI Kit

## Usage

See [BLT-User-Guide](docs/BLT-Install-Guide.pdf)

## Installation

See [BLT-Installation-Guide](docs/BLT-Install-Guide.pdf)


## Documentation

[Documentation](docs/)

## License

Provided under Cisco Sample Code License, for details see [LICENSE](./LICENSE)

## Code of Conduct

Our code of conduct is available [here](./CODE_OF_CONDUCT.md)

## Contributing

See our contributing guidelines [here](./CONTRIBUTING.md)
