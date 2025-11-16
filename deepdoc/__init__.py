#
#  Copyright 2025 The InfiniFlow Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

# Monkey patch to fix Python 3.10 logging flush parameter issue
# Some dependencies call logging methods with flush=True, but Logger._log() doesn't accept it
import logging

_original_log = logging.Logger._log

def _patched_log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, stacklevel=1, **kwargs):
    """Patched _log method that filters out the 'flush' parameter."""
    # Remove flush from kwargs before passing to original _log
    kwargs.pop('flush', None)
    # Call original _log with filtered kwargs
    if exc_info is not None or extra is not None or stack_info or stacklevel != 1:
        return _original_log(self, level, msg, args, exc_info=exc_info, extra=extra, 
                           stack_info=stack_info, stacklevel=stacklevel)
    else:
        return _original_log(self, level, msg, args)

logging.Logger._log = _patched_log

from beartype.claw import beartype_this_package
beartype_this_package()
