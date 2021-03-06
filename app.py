from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

main = Flask(__name__)
main.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(main)


class Todo(db.Model):
    identity = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.identity


@main.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        pass
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "Error by adding Task"

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@main.route('/delete/<identity>')
def delete(identity):
    task_to_delete = Todo.query.get_or_404(identity)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Problem deleting task'


@main.route('/update/<identity>', methods=['GET', 'POST'])
def update(identity):
    task = Todo.query.get_or_404(identity)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Issue updating task'
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    main.run(debug=True)
