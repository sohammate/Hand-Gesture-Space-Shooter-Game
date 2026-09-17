import wave
import math
import random
import os
import struct

SAMPLE_RATE = 44100

os.makedirs("sounds", exist_ok=True)


def create_sound(filename, duration, start_freq, end_freq, volume=0.4):
    samples = int(SAMPLE_RATE * duration)

    with wave.open(filename, "w") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)

        for i in range(samples):

            progress = i / samples

            frequency = (
                start_freq +
                (end_freq - start_freq) * progress
            )

            value = (
                math.sin(
                    2 * math.pi *
                    frequency *
                    i /
                    SAMPLE_RATE
                )
                * volume
            )

            # Fade out
            fade = 1 - progress

            value *= fade

            data = struct.pack(
                "<h",
                int(value * 32767)
            )

            wav.writeframes(data)


def create_explosion(filename):
    duration = 0.35
    samples = int(SAMPLE_RATE * duration)

    with wave.open(filename, "w") as wav:

        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)

        for i in range(samples):

            progress = i / samples

            frequency = random.randint(
                50,
                180
            )

            noise = random.uniform(
                -1,
                1
            )

            envelope = 1 - progress

            value = (
                noise *
                envelope *
                0.6
            )

            value += (
                math.sin(
                    2 * math.pi *
                    frequency *
                    i /
                    SAMPLE_RATE
                )
                * envelope
                * 0.25
            )

            data = struct.pack(
                "<h",
                int(value * 32767)
            )

            wav.writeframes(data)


# Shooting sound
create_sound(
    "sounds/shoot.wav",
    0.12,
    900,
    250,
    0.35
)

# Shield sound
create_sound(
    "sounds/shield.wav",
    0.35,
    300,
    900,
    0.35
)

# Rapid fire sound
create_sound(
    "sounds/rapid.wav",
    0.30,
    500,
    1200,
    0.35
)

# Extra life sound
create_sound(
    "sounds/life.wav",
    0.40,
    500,
    1000,
    0.4
)

# Game over sound
create_sound(
    "sounds/gameover.wav",
    0.8,
    500,
    100,
    0.4
)

# Explosion sound
create_explosion(
    "sounds/explosion.wav"
)

print("Sound files created successfully!")
