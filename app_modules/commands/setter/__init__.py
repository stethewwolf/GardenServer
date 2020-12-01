# MIT License stefano-prina@outlook.it
# 
# Copyright (c) 2019 Stefano Prina stethewwolf@gmail.com  stefano-prina@outlook.it
# 
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#   
#   The above copyright notice and this permission notice shall be included in all
#   copies or substantial portions of the Software.
#   
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#   SOFTWARE.

__all__ = [
    'Set_env', 
    'Set_conf',
    'Set_Baud_Rate',
    'Set_Device',
    'Set_Cicle_Min',
    'Set_Time2Water'
    ]

# deprecated to keep older scripts who import this from breaking
from app_modules.commands.setter.set_env       import Set_env
from app_modules.commands.setter.set_conf    import Set_conf
from app_modules.commands.setter.set_baud_rate  import Set_Baud_Rate
from app_modules.commands.setter.set_device import Set_Device
from app_modules.commands.setter.set_cicle_min import Set_Cicle_Min
from app_modules.commands.setter.set_time_to_watering import Set_Time2Water
from app_modules.commands.setter.set_threshold import Set_Threshold

