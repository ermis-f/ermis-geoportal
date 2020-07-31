# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2016 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

import os
import sys
import logging
import shutil
import base64
import traceback
import uuid
import decimal
import re
import logging
from requests import Request
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import home_login_required, user_passes_home_test
from django_cas_ng.decorators import user_passes_test
#from . import signals
logger = logging.getLogger("geonode.base.fields")

def retTrue(user):
    #logger.error("USER")
    #logger.error(user)
    #logger.error(user.mail)
    #logger.error(user.password)
    return  user.is_authenticated
    #return False
    #if user == 'AnonymousUser':
    #	return False
    #else:
    #    return True


def g_home(request, template='site_index.html'):
         #logger.error("HOME")
         #logger.error(request.user)
         #logger.error(retTrue(request.user))
         #logger.error("GET")
         #for key in request.GET:
              #logger.error(key)
         #     looger.error(request.GET[key])
         #logger.error("POST")
         #for key in request.POST:
         #     logger.error(key)
         #     looger.error(request.POST[key])
               
         #d=decorators.user_passes_test( 
		#lambda u: u.is_authenticated,
        	#login_url=None,
        	#redirect_field_name='next')
         #logger.error(d)
         #decorators.login_required()
         #logger.error(request.POST)
   #      logger.error(request.GET["username"])
         #logger.error(request.POST["is_active"])

         #if request.user.is_authenticated:
         #    return redirect('https://geoportal.ermis-f.eu/account/login')
         #else:
	 return render(request, template)
