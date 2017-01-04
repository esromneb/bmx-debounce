# Python Debounce

This is a simple python class I put together to debounce calls.  I would consider this the same syle as many debounce implimentations found in javascript. I wrote this because the only other debounce code I could find called time.sleep()

### Features
* non-blocking
* Separates debounce timer from specific function
* keeps track of successful and rejected calls


### Example Code
This python file will only print the message twice

```python
from debounce import Debounce
import time

def mymessage():
    print "call went through"

deb = Debounce(1.0)
deb(mymessage)()
deb(mymessage)()
deb(mymessage)()
deb(mymessage)()
deb(mymessage)()
time.sleep(1)
deb(mymessage)()

```

Check the test file for more uses.
