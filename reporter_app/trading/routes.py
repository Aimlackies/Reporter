from flask import Flask, render_template, url_for, redirect
from flask_security import auth_required, roles_required
from reporter_app.trading import bp
from reporter_app.trading.utils import post_bids, get_bids, get_surplus, get_untraded_volume, see_get_market_data, get_gen_use
from reporter_app import db
from reporter_app import users
from reporter_app.models import Trading,PredictedLoad,ActualLoad
from datetime import datetime, timedelta


@bp.route('/trading')
@auth_required("token", "session")
@roles_required('verified')
def trading():
    #query the database
    # connect the template to the data item from the query
    start_date = datetime.now() - timedelta(hours=24)
    # Gets rows that match the filter
    bid_entries=Trading.query.filter(Trading.date_time>start_date).all()

    return render_template('trading/trading.html', bid_entries=bid_entries, title="Trading")

# when the text pointing to this ref is clicked render the template from the path defined below
@bp.route('/trading/predicted_load')
@auth_required("token", "session")
@roles_required('verified')
def trading_predicted_load():
    start_date = datetime.now() - timedelta(hours=24)
    predicted_load_entry=PredictedLoad.query.filter(PredictedLoad.date_time>start_date).all()
    # predicted_load is what's called from the template, the template to be rendered is defined here
    return render_template('trading/predicted.html', predicted_load=predicted_load_entry, title= "Predicted Load")

@bp.route('/trading/actual_load')
@auth_required("token", "session")
@roles_required('verified')
def trading_actual_load():
    start_date = datetime.now() - timedelta(hours=24)
    actual_load=ActualLoad.query.filter(ActualLoad.date_time>start_date).all()
    return render_template('trading/trading.html', bid_entries=actual_load, title= "Actual Load")

@bp.route('/trading/gen')
@auth_required("token", "session")
@roles_required('verified')
def trading_gen():
    start_date = datetime.now() + timedelta(hours=24)
    gen,dem=get_gen_use()
    print(gen)
    return render_template('trading/actual.html',bid_entries=gen,title="test")
