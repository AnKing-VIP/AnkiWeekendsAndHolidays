## Configuration

###dates [string]
<b>Values:</b> "YYYY-MM-DD"
<b>Default:</b> ["1970-01-01"]
<b>Example:</b> ["2020-12-01", "2020-12-02", "2020-12-03"]

###max_change_days [positive Integer]
<b>Default:</b> 7

Intervals won't be changed by more than the amount 

###max_days_lookahead [positive integer]
<b>Values:</b> 1-365 Positive Integer
<b>Default:</b> 365

Maximum lookup days - nothing will be rescheduled at any day later than (today + {max_days}).
Safe to leave at default value.

###Shortcut [string]
<b>Values:</b> Should be a valid shortcut string (QT), or empty ('')
<b>Default:</b> "Ctrl+Shift+r"
