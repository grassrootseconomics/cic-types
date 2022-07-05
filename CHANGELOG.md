# CHANGELOG

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

##[0.2.6]

- Downgrade python dep from ^3.9 -> ^3.8

##[0.2.5]

- Revert chainlib-eth dep from ~0.3.0 -> ~0.1.0
- Add the ability to set MetadataRequestsHandler.auth_token = metadata_auth_token

##[0.2.2]

- fix: update deps

##[0.2.1]

##[0.2.0] - unreleased

- Use enumerated types for metadata pointer

##[0.1.0] - 02-12-2021

### ADDED

- Area names and types to location object in person object.
- Logic for loading of validation schemas from json files
- Methods to manage identity data.
- Means to serialize person object.
- Tests for system logic.
- Validation systems for person type object.
- Person type object.
- Initial setup for the cic types infrastructure.

### FIXED

- Error in build part of version string.
- Error in include definitions in setup.cfg file.

### CHANGED

- Moved validation schemas into json files.
- Network names to placeholder.
- Relaxed check for email in function to generate vcard.
- Lat/Lon in person validation schema to number type.
- Year attribute in person type schema to date of birth.
