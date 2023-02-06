from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView
from django.contrib.auth.hashers import make_password, check_password
import datetime

from .forms import *
from .models import *
# from patient_sector.models import Patient
# from patient_sector.forms import PatientForm
from django.contrib.auth.models import Group
from calendar import Calendar
from utils.month_name import month
from django.contrib.auth.mixins import LoginRequiredMixin
