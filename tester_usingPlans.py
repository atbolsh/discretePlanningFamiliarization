# For brief demo, copy-paste this into terminal from home dir.

from tester import *
from strips.strips import *

s = main('strips/oldFormatFiles/eat_apple_v8.txt')
q.executePlan(s)

