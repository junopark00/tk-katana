# tk-katana

`tk-katana` is a ShotGrid Toolkit engine for Katana, providing seamless integration with ShotGrid. 

This engine allows artists and technical directors to access ShotGrid functionality directly within Katana.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Environments](#environments)
- [Configuration](#configuration)
- [Contributing](#contributing)

## Introduction

`tk-katana` integrates ShotGrid with Katana, enabling a streamlined workflow for visual effects and animation production. 

By using this toolkit, users can easily manage assets, publish work, and track project progress within the Katana environment.

## Environments
tk-katana has been tested in this environment:
- Flow Production Tracking Desktop App 1.8.0
- Katana 6.0v4
  - Katana 6.0v4 uses PyQt5 but this engine converts the UI to PySide2.

## Features

- Asset Management: Browse and load assets directly from ShotGrid.
- Publishing: Publish your work to ShotGrid with metadata and version control.
- Task Management: View and manage your ShotGrid tasks within Katana.
- Customizable UI: Tailor the toolkit interface to fit your pipeline needs.

## Installation

#### You must be prepared for [Shotgrid](https://shotgrid.autodesk.com/)  and Advanced Project Settings in Shotgrid Desktop App to use `tk-katana`!

The official [ShotGrid Developer Help Center](https://help.autodesk.com/view/SGDEV/ENU/) and [Shotgrid Community](https://community.shotgridsoftware.com/) can be helpful.


## Configuration
To configure `tk-katana`, edit the environment yml files located in the `config` directory.
After adding the `tk-katana` engine, you can add various apps to `tk-katana`.


#### 1. Locate where you installed Pipeline Configuration

#### 2. Add KATANA_RESOURCES to recognition of init.py in tk-katana within Katana

```sh
export KATANA_RESOURCES="$KATANA_RESOURCES:/tk-katana/resources/Katana"
```

#### 2. Add engine descriptor section to `config/env/includes/engine_locations.yml`:

```yaml
engines.tk-katana.location:
  type: dev
  name: tk-katana
  version: v0.0.1
  path: "/path/to/tk-katana/engine"
```

#### 3. Then, create `config/env/includes/settings/tk-katana.yml`:

```yaml
includes:
#  - ../app_locations.yml
  - ../engine_locations.yml
#  - ./tk-multi-loader2.yml
#  - ./tk-multi-publish2.yml
  - ./tk-multi-workfiles2.yml

# asset_step
settings.tk-katana.asset_step:
apps:
   # tk-multi-about:
   #   location: "@apps.tk-multi-about.location"
   # tk-multi-loader2: "@settings.tk-multi-loader2.katana"
   # tk-multi-publish2: "@settings.tk-multi-publish2.katana.asset_step"
   tk-multi-workfiles2: "@settings.tk-multi-workfiles2.katana.asset_step"
menu_favourites:
  - {app_instance: tk-multi-workfiles2, name: File Open...}
  - {app_instance: tk-multi-workfiles2, name: File Save...}
#  - {app_instance: tk-multi-publish2, name: Publish...}
#  - {app_instance: tk-multi-loader2, name: Load}
location: '@engines.tk-katana.location'
```

#### 4. Update the apps using the `tank` command in your Pipeline Configurations folder:

```sh
./tank cache_apps
```

## Contributing
Welcome contributions to tk-katana.

To contribute:
1. Fork the repository.
2. Create a new branch (git checkout -b feature/your-feature-name).
3. Make your changes.
4. Commit your changes (git commit -m 'Add some feature').
5. Push to the branch (git push origin feature/your-feature-name).
6. Open a pull request.
