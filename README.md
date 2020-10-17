# raspi_recorder
Records sound on a Raspberry Pi. You can use any USB-microphone that you might already have, or a cheap USB-soundcard with a headset or a standard USB webcam.

It records only when the sound level exceeds a predefined threshold (manually set or decided by calibration). 

initial script based on https://stackoverflow.com/a/16385946/11736660

# installation

If there is [gcc-related problem](https://stackoverflow.com/questions/20023131/cannot-install-pyaudio-gcc-error) with pyaudio, install this stuff: 

`sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0`

Run test_levels.py to check it works. It should show "LOUD" when you speak something into your mic.

Run record_and_crop.py to record. 
