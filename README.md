# Emulator Step Simulator (`mockstep.py`)

## Overview

This Python script simulates realistic walking steps on an Android emulator. It connects to the emulator's console via Telnet and sends accelerometer data that mimics the rhythmic, forceful pattern of a firm walk.

It is designed to help test and debug applications that rely on Android's step counter sensor, providing a consistent and repeatable stream of data. The script also provides a live visualization of the generated sensor data directly in the command line.

## Features

*   **Realistic Simulation:** Generates a sine wave of accelerometer data corresponding to a firm walk at **120 steps per minute (2 steps/second)**.
*   **Triple Visualization:** 
    - **Accelerometer Bar Graph:** Shows the actual sensor values (7.8-11.8 range) being sent to the emulator
    - **Dual Step Lines:** Continuous walking state animation + explicit step landing notifications
    - **Mathematical Sine Wave:** Displays the pure sine function (-1 to +1) that drives the simulation
*   **Live Step Detection:** Visual markers and explicit notifications when foot impacts are detected (sine wave peaks)
*   **Flexible Display Sizes:** Four presets (small, medium, large, xl) plus custom dimension options
*   **Emulator Integration:** Connects directly to the Android emulator's Telnet port for sensor manipulation.
*   **Authentication:** Automatically handles authentication by reading the token from the default location (`~/.emulator_console_auth_token`).

## Requirements

*   Python 3
*   An Android emulator running on the same machine.

## How to Use

The script is run from your command line.

### 1. Find Emulator Port and Token

*   **Port:** The title bar of the emulator window shows the port it is running on (e.g., "Android Emulator - Pixel_6_API_33: **5554**"). The default is `5554`.
*   **Token:** The emulator requires an authentication token for console commands. This script automatically reads the token from the `~/.emulator_console_auth_token` file, which is the standard location where Android Studio stores it. You typically do not need to provide this manually.

### 2. Run the Script

Open a terminal or command prompt, navigate to the directory containing `mockstep.py`, and run the following command.

**Basic Usage (most common):**
This command connects to the default port (`5554`) and uses the automatically found auth token.

```bash
python3 mockstep.py
```

**Display Size Options:**
Choose from four preset sizes or customize individual dimensions.

```bash
python3 mockstep.py --size small     # Quick testing (30x40x12)
python3 mockstep.py --size medium    # Standard demo (50x60x16) - default
python3 mockstep.py --size large     # Detailed analysis (80x100x25)
python3 mockstep.py --size xl        # Maximum visibility (120x150x35)
```

**Custom Dimensions:**
Override individual dimensions for specific needs.

```bash
python3 mockstep.py --bar-width 100 --sine-height 20
```

**Connecting to a Different Port:**
If your emulator is running on a different port (e.g., `5556`), use the `--port` argument.

```bash
python3 mockstep.py --port 5556
```

**Providing the Token Manually:**
If the script cannot find your auth token file, you can provide it directly with the `--token` argument.

```bash
python3 mockstep.py --token <your_auth_token>
```

### 3. Stop the Simulation

To stop sending data, press `Ctrl+C` in the terminal. The script will gracefully disconnect from the emulator and reset the sensor data to its default resting state.

## How It Works

The simulation is based on generating a sine wave to represent the vertical acceleration of a person walking.

*   `AMPLITUDE`: Controls the force or "firmness" of the step. A higher value creates a stronger, more easily detectable signal.
*   `FREQUENCY` & `time.sleep`: These values are tuned together to control the pace of the walk. The current settings produce a signal that completes exactly two full cycles (steps) every second.
*   **Impact Detection:** The script tracks the `y-value` of the sine wave. When it detects that the value has just peaked (i.e., it was rising and has now started to fall), it prints the "impact" of the foot hitting the ground.


```
~/mockstep main* ❯ python3 mockstep.py --size large                                   
Read auth token from /Users/boydypd/.emulator_console_auth_token
Connected and authenticated with emulator on port 5554.

Simulating walking steps and displaying live graph...
Display size: Bar=80, Sine=100x25
Walking parameters: frequency=2.5, sleep=0.1s, amplitude=2.0
------------------------------------------------------------------------------------------------------------------------

Accel: 10.43 | ####################################################
👟 Step: [▬▬▬] Ready
🦶 STEP LANDED! 🦶

 1.00|       .    .    .    .    .    .    .    .    .
 0.92|  .                                                 .    .    .                      ·    ·    •
 0.83|                                                                   .    .  .    .
 0.75|                                                                 .    .      .    .
 0.67|                                                       .    .                          ·    ·
 0.58|    .                                             .                                              •
 0.50|         .    .                         .    .
 0.42|                   .               .
 0.33|                        .     .
 0.25|                    .    .   .    .
 0.17|               .                       .
 0.08|          .                                 .
 0.0 |     .                                           .                                                •
-0.08|.                                                     .    .                                 ·
-0.17|                                                                .                  .    ·
-0.25|                                                                     .        .
-0.33|                                                                         ..    .
-0.42|                                                               .    .               .
-0.50|                                                          .                              ·
-0.58| .    .                                         .    .                                        ·    ● ← Current: -0.60
-0.67|           .                               .
-0.75|                .    .           .    .
-0.83|                  .    .  . .  .    .
-0.92|   .    .    .                           .    .    .
-1.00|                                                        .    .    .    .    .    .    ·    ·    •
```

## Enhanced Visualization Features

The current version provides a comprehensive triple visualization:

### **1. Accelerometer Bar Graph**
Shows the actual sensor values (7.8-11.8 m/s²) being sent to the Android emulator - this is what your step-counting app will receive.

### **2. Dual Step Lines**
- **Top Line**: Continuous walking state animation showing all transitions:
  - `👟 Step: [▬▬▬] Ready` - Foot flat on ground
  - `👟 Step: [▬▬▬] Lifting...` - Foot lifting off
  - `👟 Step: [▬▬▬] ↗ Striding` - Foot in air, approaching peak
  - `👟 Step: [▬▬▬] ↘ Landing!` - Foot landing (step detected)
- **Bottom Line**: Explicit step notifications - `🦶 STEP LANDED! 🦶` appears only when a step is detected

### **3. Mathematical Sine Wave**
A scrolling visualization of the pure sine function (-1 to +1) that drives the simulation, with trail effects showing temporal progression:
- `●` Current position (solid dot)
- `•` Recent trail (medium dot)
- `·` Older trail (light dot)  
- `.` Very old trail (faint dot)

This triple display helps you understand:
- How the mathematical sine wave translates to physical accelerometer readings
- The exact timing and detection of each step impact
- The relationship between walking states and sensor data
- The frequency and amplitude of the walking simulation in real-time
