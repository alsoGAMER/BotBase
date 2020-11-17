"""
Copyright 2020 Nocturn9x & alsoGAMER

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from pyrogram import Client, CallbackQuery, InlineQuery
from pyrogram.errors import RPCError
import logging
from typing import Union


class MethodWrapper(object):
    """A class that that implements a wrapper around ``pyrogram.Client`` methods.
       To access a pyrogram method just call ``MethodWrapper.method_name``.
       All method calls are performed in a try/except block and either return
       the exception object if an error occurs, or the result of the called
       method otherwise. All errors are automatically logged to stderr.

       :param instance: The ``pyrogram.Client`` or ``pyrogram.CallbackQuery`` or ``pyrogram.InlineQuery`` instance (not class!)
       :type instance: Union[Client, CallbackQuery, InlineQuery]
    """

    def __init__(self, instance: Union[Client, CallbackQuery, InlineQuery]):
        """Object constructor"""

        self.instance = instance

    def __getattr__(self, attribute: str):
        if attribute in self.__dict__:
            return self.__dict__[attribute]
        else:
            def wrapper(*args, **kwargs):
                if hasattr(self.instance, attribute):
                    try:
                        return getattr(self.instance, attribute)(*args, **kwargs)
                    except RPCError as rpc_error:
                        logging.error(f"An exception occurred -> {type(rpc_error).__name__}: {rpc_error}")
                        return rpc_error
                else:
                    raise AttributeError(self.instance, attribute)
            return wrapper
