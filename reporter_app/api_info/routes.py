"""przez przypadek zmodyfikowalam glowna galaz, sprawdz czy moja galaz sie uaktualnila ze zmianami"""
"""czy to jest polozone z database???"""
from flask import Flask, render_template, url_for, redirect
#sprawdz co robi url_for 
from reporter_app.api_info import bp
from reporter_app import db
#sprawdz czy musze miec odniesienie do kazego zrodla osobno czy musze je pogrupowac, czy 'AIMLAC HQ Llanwrtyd Wells' to wszystkie???
from reporter_app.models import User
#sprawdz czy to potrzebuje
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
#sprawdz definicje
from flask_security import auth_required, roles_required
from sqlalchemy import func
from datetime import datetime, timedelta
import sys
from flask_security import hash_password
from reporter_app import db
from reporter_app.api_info.utils import get_average_power
from reporter_app.models import power_gen
@bp.route('/live_system')
@auth_required("token", "session")
@roles_required('verified')
def live_system():
 last_30m_start = datetime.now() - timedelta(minutes=30)
 average_power = get_average_power(last_30m_start)
 if average_power is not None:
  new_power_gen = power_gen(
   date_time=last_30m_start,
   location='llanwrtyd-wells',
   power=average_power
  )
  db.session.add(new_power_gen)
  db.session.commit()
 
 return render_template('api_info/live_system.html', title='Live system')
    
