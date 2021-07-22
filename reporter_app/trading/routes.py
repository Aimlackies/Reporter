from flask import Flask, render_template, url_for, redirect

from reporter_app.trading import bp
from reporter_app.trading.Bid_sell_functions import post_bids,get_bids,get_surplus,get_untraded, see_get_market_data
from reporter_app import db
from reporter_app import User
import pandas as pd
from flask_security import auth_required, roles_required

@bp.route('/trading')
@auth_required("token", "session")
@roles_required('verified')



