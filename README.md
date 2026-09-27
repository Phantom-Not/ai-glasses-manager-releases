# AI Glasses Manager

**A glasses-first home for apps, media, files, device tools, and everyday controls on Rokid Glasses.**

[Download the latest release](https://github.com/Phantom-Not/ai-glasses-manager-releases/releases/latest) · [Report an issue](https://github.com/Phantom-Not/ai-glasses-manager-releases/issues)

AI Glasses Manager brings the tools that are usually scattered across Android into one interface designed around the way Rokid Glasses are actually used: left, right, and tap. It is built for quick navigation on a compact display, with readable focus states, restrained AR-friendly visuals, and direct access to the features that matter most on the glasses.

The project began as **Rokid Manager**. As it grew beyond settings and device shortcuts, it became AI Glasses Manager—a broader effort to explore what a useful, dependable software ecosystem for Rokid Glasses can look like.

<table>
  <tr>
    <td width="33%" align="center"><img src="docs/images/home.png" alt="AI Glasses Manager Home screen" width="260"></td>
    <td width="33%" align="center"><img src="docs/images/app-store.png" alt="AI Glasses Manager App Store" width="260"></td>
    <td width="33%" align="center"><img src="docs/images/manager-settings.png" alt="AI Glasses Manager settings" width="260"></td>
  </tr>
  <tr>
    <td align="center"><strong>One place for everyday tools</strong></td>
    <td align="center"><strong>App discovery built for glasses</strong></td>
    <td align="center"><strong>Clear, focused controls</strong></td>
  </tr>
</table>

## Why it exists

Smart-glasses software is still young. A good ecosystem needs more than a launcher: people need a reliable way to discover software, manage updates, move files, work with photos and video, understand the hardware, and reach system controls without fighting a phone-shaped interface.

AI Glasses Manager is a practical attempt to build that missing layer. Features are shaped by real use on the glasses, with an emphasis on predictable navigation, useful offline behavior, and tools that feel at home on a wearable display.

## Features

### App Store and app management

- Browse thousands of Android apps from a glasses-friendly catalog.
- Explore curated, developer, global, and China-friendly selections.
- Search by name and move through categories without leaving the main interface.
- Review app details before downloading or installing.
- See available updates for supported installed apps.
- Keep browsing previously loaded information when the network is unavailable.
- Receive clear offline guidance instead of waiting on a connection that is not there.

### Camera and Gallery

- Take photos or record video from a purpose-built Camera interface.
- Adjust capture mode, framing, zoom, and grid controls without leaving the viewfinder.
- Choose whether Camera shutter and recording sounds are used.
- Get immediate visual confirmation when a capture succeeds or fails.
- Browse photos and videos in Album, with media viewing and video playback designed for the glasses display.

### Files and wireless transfer

- Browse local storage with navigation tuned for the Rokid touchpad and directional input.
- Open common files and move through folders without relying on a phone-style touch interface.
- Use Wi-Fi Drop for convenient wireless file transfer between supported devices.
- Reach storage information and Android's related system tools from the same Manager.

### Device controls and diagnostics

- Open Rokid and Android settings from a consistent glasses-first menu.
- Reach Wi-Fi, Bluetooth, sound, keyboard, installed apps, storage, and battery tools.
- Use Cleaner for one-tap maintenance or to review running apps.
- View live compass, accelerometer, gyroscope, pitch, and roll information in Live IMU.
- Calibrate or zero sensor readings when working with motion and orientation.

### AI and hands-free access

- Enable an optional AI microphone control from Manager Settings.
- Use supported voice actions when hands-free operation is more practical than the touchpad.
- Keep AI access hidden from Home when it is not needed.

### Manager Shortcuts

Camera, Album, App Store, and File Explorer can be added as optional Manager Shortcuts in the Rokid launcher. Each shortcut opens the matching Manager feature directly, while the Manager remains the single place to enable or remove them.

<table>
  <tr>
    <td width="33%" align="center"><img src="docs/images/manager-shortcuts.png" alt="Optional Manager Shortcuts" width="260"></td>
    <td width="33%" align="center"><img src="docs/images/cleaner.png" alt="Cleaner tools" width="260"></td>
    <td width="33%" align="center"><img src="docs/images/live-imu.png" alt="Live IMU compass and motion readings" width="260"></td>
  </tr>
  <tr>
    <td align="center"><strong>Optional launcher shortcuts</strong></td>
    <td align="center"><strong>Simple maintenance tools</strong></td>
    <td align="center"><strong>Live motion and orientation data</strong></td>
  </tr>
</table>

## Designed for the glasses

- **Simple input:** primary flows work with left, right, and tap/enter.
- **Visible focus:** the selected action stays obvious without depending on color alone.
- **AR-aware presentation:** high-contrast content and restrained surfaces remain readable against the real world.
- **Offline consideration:** cached information and local tools remain useful when Wi-Fi is unavailable.
- **Consistent language:** the same interaction patterns carry across apps, settings, and utilities.
- **Localized interface:** English, Simplified Chinese, Traditional Chinese, Cantonese (Hong Kong), Japanese, Korean, Russian, French, German, and Spanish are supported.

## Install

1. Open the [latest release](https://github.com/Phantom-Not/ai-glasses-manager-releases/releases/latest).
2. Download the AI Glasses Manager APK.
3. Install it with the Android package installer, or from a connected computer with:

   ```bash
   adb install -r AI-Glasses-Manager-<version>.apk
   ```

Once installed, open **AI Glasses Manager** from the Rokid launcher. Future Manager releases can also be checked from **Manager Settings → App Update**.

For safety, download Manager builds only from this repository or from an official mirror listed in [`manager-update.json`](manager-update.json).

## Compatibility

AI Glasses Manager is designed and tested for Rokid Glasses. Available system actions can vary with glasses firmware and Android version because some controls are provided by the underlying system.

The Manager requires Android 8.0 (API 26) or later. Features that use the camera, microphone, storage, nearby devices, or network request the corresponding Android permission when needed.

## Feedback and issue reports

Real-hardware feedback is what moves the project forward. If something does not behave correctly on your glasses, [open an issue](https://github.com/Phantom-Not/ai-glasses-manager-releases/issues) with:

- your Manager version;
- glasses model and firmware version;
- the feature you were using;
- the steps that reproduce the problem;
- a screenshot, if it does not contain personal information.

Please remove device identifiers, network names, activation details, and personal files before posting.

## About this repository

This repository hosts official AI Glasses Manager release metadata, APK downloads, screenshots, and public documentation. It is not the application source repository.

AI Glasses Manager is an independent project and is not affiliated with or endorsed by Rokid.
