import pigpio

class PWM_reader:
    def __init__(self, pi, gpio):
        self._high_tick = None
        self._high = None
    
        self._cb = pi.callback(gpio, pigpio.EITHER_EDGE, self._cbf)     # soort van event detector
 
    def _cbf(self, gpio, level, tick):
        if level == 1:          
            if self._high_tick is not None:
                t = pigpio.tickDiff(self._high_tick, tick)
            self._high_tick = tick
    
        elif level == 0:    
            if self._high_tick is not None:
                t = pigpio.tickDiff(self._high_tick, tick)
                self._high = t
 
    def pulse_width(self):
        """
        Returns the PWM pulse width in microseconds.
        """
        if self._high is not None:
            if self._high > 2000:
                self._high = 2000
            elif self._high < 1000:
                self._high = 1000
            return self._high
        else:
            return 0.0
 
    def cancel(self):
        """
        Cancels the reader and releases resources.
        """
        self._cb.cancel()