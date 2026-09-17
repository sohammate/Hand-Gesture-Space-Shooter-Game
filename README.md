# 🚀 Hand Gesture Space Shooter Game

A Python-based space shooter game that allows players to control a spaceship using **real-time hand gestures** instead of a traditional keyboard or mouse.

The project combines **computer vision, hand tracking, and game development** to create an interactive gaming experience where the player's hand movements are detected through a webcam and converted into game controls.

---

## 🎮 About the Project

**Hand Gesture Space Shooter Game** is a simple but interactive 2D space shooter game developed using Python.

In a traditional space shooter, the player uses a keyboard or controller to move the spaceship and shoot enemies. In this project, the player's **hand becomes the controller**.

A webcam captures the player's hand movements, and a hand-tracking system detects the position and gestures of the hand. These gestures are then used to control the spaceship, fire bullets, and activate special shooting abilities.

The project demonstrates how **computer vision can be integrated with game development** to create a more natural and engaging human-computer interaction.

---

## ✨ Features

- 🖐️ **Hand Gesture Control**
  - Control the spaceship using hand movements.
  - No keyboard or mouse is required for basic gameplay.

- 🚀 **Spaceship Movement**
  - Move the spaceship around the game area using your hand position.

- 🔫 **Gesture-Based Shooting**
  - Use specific hand gestures to fire bullets at enemies.

- 💥 **Rapid Shooting**
  - Allows the player to shoot bullets rapidly during gameplay.

- 🌟 **Multi-Directional Shooting**
  - A special three-finger gesture can activate multi-directional bullet firing.

- 👾 **Enemy System**
  - Enemies continuously spawn and move toward the player.

- ❤️ **Player Health / Lives**
  - The player must avoid enemy attacks and survive as long as possible.

- 🎯 **Score System**
  - Destroying enemies increases the player's score.

- 🎮 **Real-Time Interaction**
  - Hand movements and gestures are detected in real time through the webcam.

- 🔊 **Sound Effects**
  - Shooting and game events can include sound effects for a better gaming experience.

---

## 🛠️ Technologies Used

The project is developed using the following technologies:

- **Python**
- **Pygame** – Used to develop the game, graphics, movement, collision detection, and gameplay mechanics.
- **OpenCV** – Used to access and process webcam input.
- **MediaPipe** – Used for real-time hand landmark detection and gesture recognition.

---

## 🧠 How It Works

The game follows a simple computer-vision-based control pipeline:

```text
Webcam
   ↓
Capture Video
   ↓
Hand Detection
   ↓
Hand Landmark Tracking
   ↓
Gesture Recognition
   ↓
Convert Gesture into Game Action
   ↓
Control Spaceship
   ↓
Gameplay
