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
- [Acknowledgements](#acknowledgements)

## Introduction

`tk-katana` integrates ShotGrid with Katana, enabling a streamlined workflow for visual effects and animation production. By using this toolkit, users can easily manage assets, publish work, and track project progress within the Katana environment.

## Features

- Asset Management: Browse and load assets directly from ShotGrid.
- Publishing: Publish your work to ShotGrid with metadata and version control.
- Task Management: View and manage your ShotGrid tasks within Katana.
- Customizable UI: Tailor the toolkit interface to fit your pipeline needs.

## Installation

To install `tk-katana`, follow these steps:

#### 1. Clone the repository:
```sh
   git clone https://github.com/yourusername/tk-katana.git
```
#### 2. Navigate to the project directory:

```sh
   cd tk-katana
```
#### 3. Install the required dependencies:

```sh
   pip install -r requirements.txt
```
#### 4. Set up the environment variables:

```sh
   export SHOTGRID_SITE=https://yourshotgridsite.shotgunstudio.com
   export SHOTGRID_API_KEY=your_api_key
```

## Configuration
Configure tk-katana by editing the config.yml file located in the config directory. Set the appropriate values for your ShotGrid site and other necessary settings.

#### Example config.yml:
```yaml
   shotgrid_site: "https://yourshotgridsite.shotgunstudio.com"
   api_key: "your_api_key"
   project_id: 123
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

## Acknowledgements
Special thanks to the ShotGrid and Katana communities for their support and contributions.
