# Brownfield Licensing Tool

Brownfield Licensing tool is a tool to assist with gathering entitlement information and licensing devices 
for customers migrating to Cisco Smart Licensing. 


## Business/Technical Challenge
Customers who are upgrading software often find that they are now required to use Cisco Smart Licensing.
Upon completing the upgrade they realize that they do not have a Cisco Smart License in their Cisco
Smart account for the device they just upgraded. For customers who can take advantage of Device Led
Conversion this may not be a problem. However, customers who can not take advantage of Device Led Conversion 
(as is the case with many customers) will need to open a case with Cisco Global Licensing Operations. When opening a
case the customer will be required to provide the sales order numbers for the devices being upgraded. Often the 
only information the customer has is the serial number of the device. Sales orders are often not maintained by the customer 
but are required when trying to prove the level of entitlement.

Furthermore, once the entitlement is fixed by the Global Licensing Operations team the customer is now
faced with actually licensing the their devices. This number could be in the thousands of devices. The customer
has already licensed the device previously and is now faced with exhausting countless man hours to do it again.
Most customers find this unacceptable and are searching for a better way.

## Proposed Solution

The proposed solution is twofold.

1) Provide a solution to ease the collection of entitlement information and submission to Cisco
Global Licensing Operations for brownfield migrations to Cisco Smart Licensing.

2) Provide a mechanism for customers with closed networks to license their network infrastructure
devices without using device call-home to Cisco Smart Software Manager.


### Cisco Products Technologies/ Services

Our solution will leverage the following Cisco technologies

* [Cisco Commerce Workspace Order API](http://cisco.com/go/aci)
* [Cisco Commerce Subscriptions and Software Contract Administration API](http://cisco.com/go/dna)
* [Cisco IOS-XE](http://cisco.com/go/ios-xe)

## Team Members

* Aaron Warner <aawarner@cisco.com> - US Public Sector
* Kris Swanson <kriswans@cisco.como> - US Public Sector
* Justin Poole <jupoole@cisco.com> - Global Enterprise


## Solution Components


<!-- This does not need to be completed during the initial submission phase  

Provide a brief overview of the components involved with this project. e.g Python /  -->


## Usage

<!-- This does not need to be completed during the initial submission phase  

Provide a brief overview of how to use the solution  -->



## Installation

How to install or setup the project for use.


## Documentation

Pointer to reference documentation for this project.


## License

Provided under Cisco Sample Code License, for details see [LICENSE](./LICENSE.md)

## Code of Conduct

Our code of conduct is available [here](./CODE_OF_CONDUCT.md)

## Contributing

See our contributing guidelines [here](./CONTRIBUTING.md)
