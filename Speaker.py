from time import sleep 
from gpiozero import TonalBuzzer
from gpiozero.tones import Tone 

b =  TonalBuzzer(17)

b.play(Tone(800))
sleep(10)
