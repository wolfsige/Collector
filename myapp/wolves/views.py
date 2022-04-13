from flask import render_template, url_for, flash, request, redirect, Blueprint, abort
from flask_login import current_user, login_required
from myapp import db 
from myapp.models import Wolves
from myapp.wolves.forms import WolvesForm

wolves = Blueprint('wolves', __name__)

@wolves.route('/create', methods=['GET', 'POST'])
@login_required
def create_wolf():
    form = WolvesForm()
    if form.validate_on_submit():
        wolves = Wolves(name=form.name.data, description=form.description.data, user_id=current_user.id)
        db.session.add(wolves)
        db.session.commit()
        flash('Wolf Created')
        print('Wolf was created')
        return redirect(url_for('core.index'))
    return render_template('create_wolf.html', form=form)

@wolves.route('/<int:wolf_id>')
def wolf(wolf_id):
    wolf = Wolves.query.get_or_404(wolf_id) 
    return render_template('wolf.html', name=wolf.name, date=wolf.date, wolf=wolf)

# @wolves.route('/<int:wolves_id>/update',methods=['GET','POST'])
# @login_required
# def update_wolf(wolves_id):
#     wolves = Wolves.query.get_or_404(wolves_id)

#     if wolves.author != current_user:
#         abort(403)

#     form = WolvesForm()

#     if form.validate_on_submit():
#         wolves.name = form.name.data
#         wolves.description = form.description.data
#         db.session.commit()
#         flash('Wolf Updated')
#         return redirect(url_for('wolves.wolf',wolves_id=wolf.id))

#     elif request.method == 'GET':
#         form.name.data = wolves.name
#         form.description.data = wolves.description

#     return render_template('create_wolf.html',name='Updating',form=form, id=wolves_id)

@wolves.route('/<int:wolves_id>/delete',methods=['GET','POST'])
@login_required
def delete_wolf(wolves_id):

    wolves = Wolves.query.get_or_404(wolves_id)
    if wolves.author != current_user:
        abort(403)

    db.session.delete(wolves)
    db.session.commit()
    flash('Wolf Deleted')
    return redirect(url_for('core.index'))


