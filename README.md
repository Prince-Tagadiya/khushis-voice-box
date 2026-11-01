# Voice Box

> **Tactile Speech Assistant for Focused Cognitive Processing & Single-Touch Clarity**  
> Designed & Developed by **Creato4 Lab**

---

## 🌟 Overview

**Voice Box** is an assistive hardware speech box engineered for individuals with speech processing delays, apraxia, or cognitive hesitation. 

It provides **physical tactile buttons** connected to an ESP32-C3 microcontroller and a crystal-clear MAX98357A I2S amplifier with a built-in shouting engine. Users can take all the time they need to formulate intent, then press a single tactile button to speak clearly and loudly through the physical speaker.

This repository contains both:
1. **The Apple-style Web Studio Dashboard** (Web Bluetooth, Live Voice Recording, Custom Speech synthesis, PIN management, Setup Wizard).
2. **The ESP32-C3 Firmware** (BLE GATT service, LittleFS audio storage, synthesized chimes, deep sleep power management).

---

## 🌐 Live Web Studio Dashboard

Open the live Web Bluetooth studio directly from Google Chrome, Microsoft Edge, or Opera:

👉 **[https://prince-tagadiya.github.io/khushis-voice-box/](https://prince-tagadiya.github.io/khushis-voice-box/)**

*(Ensure Bluetooth is enabled on your computer or mobile phone).*

---

## ✨ Features

- **Apple-Grade Minimal Interface**: Smooth animations, calm minimalist color palette, and native Light / Dark mode support.
- **First-Time Setup Wizard**: 3-step setup to name the device, choose a 4-digit security PIN, and perform an interactive physical hardware button check.
- **Live Button Press Sync**: Pressing any physical button on the hardware box highlights live on screen with matching acoustic chimes.
- **Voice Recording & Preview**: Record voice directly through the browser microphone (with real-time countdown), listen before sending, and flash it to the speaker.
- **Text-to-Speech (TTS)**: Convert any word into loud, crystal-clear 16 kHz 16-bit PCM and transfer over Bluetooth Low Energy.
- **Local Audio Upload**: Upload any WAV / MP3 / M4A / FLAC file; automatically resampled and normalized to 16 kHz PCM.
- **Security PIN Protection**: 4-digit PIN authentication to prevent unauthorized tampering. PIN update flow requires confirmation.
- **Factory Reset & Format**: Safe wipe of LittleFS and NVS storage directly from the authenticated dashboard.
- **Ultra-Low Power**: Automatic deep sleep when idle, waking up instantly on any physical button press.

---

## 🛠️ Hardware Requirements

- **Microcontroller**: ESP32-C3 Super Mini
- **I2S DAC / Amplifier**: MAX98357A (BCLK GPIO 6, LRC GPIO 7, DIN GPIO 10)
- **Speaker**: 16-Ohm, 0.25W / 8-Ohm, 1W
- **Tactile Buttons**: 5 momentary push buttons to GND (Apple GPIO 4, Banana GPIO 3, Mango GPIO 2, Grapes GPIO 1, Orange GPIO 0) with internal pull-ups

---

## 📄 License & Support

Designed & Developed by **Creato4 Lab**.  
Support Active: **Till 31 Dec 2026**.

