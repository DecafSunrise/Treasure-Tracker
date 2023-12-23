import time
import board
import pwmio

# Create piezo buzzer PWM output.
buzzer = pwmio.PWMOut(board.D5, variable_frequency=True)

# Define a list of tones/music notes to play.
notes = {'C4': 262, 'D4': 294, 'E4': 330, 'F4': 349, 'G4': 392, 'A4': 440, 'B4': 494,
 'C5': 523,
 'D5': 587,
 'E5': 659,
 'F5': 698,
 'G5': 784,
 'A5': 880,
 'B5': 988,
 'C6': 1047,
 'D6': 1175,
 'E6': 1319,
 'F6': 1397,
 'G6': 1568,
 'A6': 1760,
 'B6': 1976}

song = """CDEFGAB"""

for i in [4,5,6]:
    for note in song:

        print(note)
        buzzer.duty_cycle = 2**15  # 32768 value is 50% duty cycle, a square wave.
        buzzer.frequency = notes[f"{note}{i}"]
        time.sleep(0.1)
        buzzer.duty_cycle = 0
        time.sleep(0.05)
