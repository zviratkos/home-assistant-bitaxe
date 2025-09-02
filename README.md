# Bitaxe Home Assistant Integration

[![Release Downloads](https://img.shields.io/github/downloads/zviratkos/home-assistant-bitaxe/total)](https://github.com/zviratkos/home-assistant-bitaxe/releases)
[![GitHub issues](https://img.shields.io/github/issues/zviratkos/home-assistant-bitaxe)](https://github.com/zviratkos/home-assistant-bitaxe/issues)
[![Version - 1.0.4](https://img.shields.io/badge/version-1.0.4-blue)](https://github.com/zviratkos/home-assistant-bitaxe/releases)

This is a custom integration for Bitaxe miners in Home Assistant.

## Features

- **Real-time Monitoring**: Keep track of power, temperature, hashrate, and other mining metrics in real-time.
- **Easy Configuration**: Configure your Bitaxe device effortlessly through Home Assistant's user interface.

## Manual Installation

1. Navigate to your Home Assistant configuration directory. This is usually the `/config` directory in your Home Assistant setup.

2. Clone the repository directly into the `custom_components` folder (create the folder if it doesn't exist):
   ```bash
   mkdir -p custom_components
   git clone https://github.com/zviratkos/home-assistant-bitaxe.git /config/custom_components/bitaxe
   ```

3.  Restart Home Assistant.

## HACS Installation

1. Open the HACS section in your Home Assistant.

2. Go to **Integrations** and select **Add Repository**.

3. Enter the URL for this repository: `https://github.com/zviratkos/home-assistant-bitaxe`.

4. Install the integration and follow the configuration steps.

## Configuration

To set up the integration, follow these steps:

1. Go to Settings > Devices & Services > Add Integration.
2. Search for "Bitaxe" and select it.
3. Enter the IP address of your Bitaxe miner.
4.  Choose a name for your Bitaxe miner (this can be any name you prefer).
5.  Complete the setup.

## Version
This is the first stable version (v1.0.4) compatible with HACS!

## Screenshots

### Setup Screen
<img src="custom_components/bitaxe/images/Setup.png" alt="Setup Screen" style="max-width: 100%; height: auto;">

### Sensor Data Screen
<img src="custom_components/bitaxe/images/Sensor.png" alt="Sensor Data Screen" style="max-width: 100%; height: auto;">

## Credits
This is fork of DerMika Bitaxe Integration https://github.com/DerMiika/Bitaxe-HA-Integration
