# tk-katana

`tk-katana` is a ShotGrid Toolkit engine for Katana, providing seamless integration with ShotGrid. This engine allows artists and technical directors to access ShotGrid functionality directly within Katana.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

`tk-katana` integrates ShotGrid with Katana, enabling a streamlined workflow for visual effects and animation production. By using this toolkit, users can easily manage assets, publish work, and track project progress within the Katana environment.

## Features

- Asset Management: Browse and load assets directly from ShotGrid.
- Publishing: Publish your work to ShotGrid with metadata and version control.
- Task Management: View and manage your ShotGrid tasks within Katana.
- Customizable UI: Tailor the toolkit interface to fit your pipeline needs.

## Installation

#### You must be prepared for [Shotgrid](https://shotgrid.autodesk.com/)  and Advanced Project Settings in Shotgrid Desktop App to use `tk-katana`!

The official [ShotGrid Developer Help Center](https://help.autodesk.com/view/SGDEV/ENU/) and [Shotgrid Community](https://community.shotgridsoftware.com/) can be helpful.

#### Clone this repository:
```sh
   git clone https://github.com/junopark00/tk-katana
```

## Configuration
To configure `tk-katana`, edit the environment yml files located in the `config` directory.
After adding the `tk-katana` engine, you can add various apps to `tk-katana`.


#### Example engine_locations.yml:
```yaml
engines.tk-katana.location:
  type: dev
  name: tk-katana
  version: v0.0.1
  path: "/path/to/tk-katana/engine"
```
## Usage
To use `tk-katana` within Katana:

Launch Katana.
Open the tk-katana panel from the ShotGrid menu.
Log in with your ShotGrid credentials.
Start managing your assets, tasks, and publish your work directly from Katana.
## Contributing
We welcome contributions to tk-katana. To contribute:

Fork the repository.
Create a new branch (git checkout -b feature/your-feature-name).
Make your changes.
Commit your changes (git commit -m 'Add some feature').
Push to the branch (git push origin feature/your-feature-name).
Open a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
