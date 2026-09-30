<div align="center">
  <h1>AI Glasses Manager</h1>
  <p><strong>Formerly Rokid Manager</strong></p>
  <p><strong>Apps, photos, files, and settings, all on your Rokid Glasses.</strong></p>
  <p>
    <a href="https://github.com/Phantom-Not/ai-glasses-manager-releases/releases/latest">Download the latest release</a>
    &nbsp;&nbsp;•&nbsp;&nbsp;
    <a href="https://github.com/Phantom-Not/ai-glasses-manager-releases/issues">Report an issue</a>
  </p>
</div>

Hi, I'm Bruce. You might know this app as **Rokid Manager**, especially the old 1.5 version shared around the community.

It's now called **AI Glasses Manager**, and I've kept working on it since then, fixing bugs and adding features like camera tools, wireless file transfers, and app updates.

It costs **$1.99 per device, paid once**, about the price of a coffee. Payments go through Stripe, with support for international payments. See [Pricing and activation](#pricing-and-activation) for the activation terms.

<p align="center">
  <img src="docs/images/home.png" alt="AI Glasses Manager Home screen" width="30%">
  <img src="docs/images/app-store.png" alt="AI Glasses Manager App Store" width="30%">
  <img src="docs/images/manager-settings.png" alt="AI Glasses Manager settings" width="30%">
</p>
<p align="center"><sub>Home&nbsp;&nbsp;•&nbsp;&nbsp;App Store&nbsp;&nbsp;•&nbsp;&nbsp;Manager Settings</sub></p>

## What's changed lately

- The App Store handles connection problems better, and you can pause or cancel downloads.
- Camera settings now include shutter sounds and clearer feedback when taking photos or recording video.
- File browsing is smoother, Gallery menus take up less space, and you can add shortcuts to your most-used tools.

You can find the full changes in the [release notes](https://github.com/Phantom-Not/ai-glasses-manager-releases/releases).

## Why I built it

I wanted to do more directly on the glasses without reaching for my phone every time. That started with opening settings, then grew into managing apps, moving files, viewing photos and videos, and adding other tools I found useful.

I'm still working on it, and feedback from people using it helps me decide what to fix or add next.

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
- Delete photos and videos directly from Album when cleaning up local storage.

<p align="center">
  <img src="docs/images/gallery.png" alt="Album picture and video categories" width="30%">
  <img src="docs/images/camera-photo.png" alt="Camera photo controls and viewfinder" width="30%">
  <img src="docs/images/camera-modes.png" alt="Camera photo and video mode chooser" width="30%">
</p>
<p align="center"><sub>Gallery&nbsp;&nbsp;•&nbsp;&nbsp;Zoom controls in the viewfinder&nbsp;&nbsp;•&nbsp;&nbsp;Photo and video mode selector</sub></p>

### Files and wireless transfer

- Browse local storage and open common files directly on the glasses.
- Move through folders without relying on a separate phone interface.
- Use Wi-Fi Drop to transfer files between the glasses and supported phones or computers without connecting through ADB each time.
- Reach storage information and Android's related system tools from the same Manager.

### Device controls and diagnostics

- Open Rokid and Android settings from a consistent glasses-first menu.
- Reach Wi-Fi, Bluetooth, sound, keyboard, installed apps, storage, and battery tools.
- Adjust system volume and glasses volume separately, or lock the glasses volume at a fixed level.
- Configure swipe feedback from the Manager.
- Use Cleaner for one-tap maintenance or to review running apps.
- View live compass, accelerometer, gyroscope, pitch, and roll information in Live IMU.
- Calibrate or zero sensor readings when working with motion and orientation.

<p align="center">
  <img src="docs/images/device-settings-connectivity.png" alt="Connectivity, sound, keyboard, and app settings" width="30%">
  <img src="docs/images/device-settings-system.png" alt="Sound, keyboard, apps, files, storage, and battery settings" width="30%">
  <img src="docs/images/sound-controls.png" alt="Separate system and glasses volume controls" width="30%">
</p>
<p align="center"><sub>Connectivity and input&nbsp;&nbsp;•&nbsp;&nbsp;System tools&nbsp;&nbsp;•&nbsp;&nbsp;Sound controls</sub></p>

### AI and hands-free access

- Enable an optional AI microphone control from Manager Settings.
- Use supported voice actions when hands-free operation is more practical than the touchpad.
- Check the built-in AI command guide for supported English and Chinese examples.
- Keep AI access hidden from Home when it is not needed.

### Manager Shortcuts

Camera, Album, App Store, and File Explorer can be added as optional Manager Shortcuts in the Rokid launcher. Each shortcut opens the matching Manager feature directly, while the Manager remains the single place to enable or remove them.

<p align="center">
  <img src="docs/images/manager-shortcuts.png" alt="Optional Manager Shortcuts" width="30%">
  <img src="docs/images/cleaner.png" alt="Cleaner tools" width="30%">
  <img src="docs/images/live-imu.png" alt="Live IMU compass and motion readings" width="30%">
</p>
<p align="center"><sub>Manager Shortcuts&nbsp;&nbsp;•&nbsp;&nbsp;Cleaner&nbsp;&nbsp;•&nbsp;&nbsp;Live IMU</sub></p>

## Designed for the glasses

- Clear focus states keep the selected action visible without depending on color alone.
- AR Mode for obstructive and better viewing on the glasses display.
- Local tools remain useful when Wi-Fi is unavailable.
- Consistent interaction patterns carry across apps, settings, and utilities.
- The interface supports English, Simplified Chinese, Traditional Chinese, Cantonese (Hong Kong), Japanese, Korean, Russian, French, German, and Spanish. 

## Pricing and activation

This is a one-time purchase for one device, with no recurring subscription.

- Activation is normally restored automatically after uninstalling and reinstalling on the same device.
- A factory reset may prevent automatic restoration. If that happens, contact me privately with your purchase record and current activation code so I can review restoring your access. A factory reset does not automatically mean you need to buy the app again.

Please don't post purchase records or activation codes in public issues.

If you're coming from Rokid Manager 1.5, the current version requires paid activation.

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

## More to come

I'll keep fixing bugs and adding features as they're ready. Check the release notes to see what's new.

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



