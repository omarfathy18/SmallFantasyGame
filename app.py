# needs a check for session on my_team/...
# needs a check for session on control
import datetime

from flask import Flask, render_template, request, flash, session, redirect
from flask_mysqldb import MySQL
from datetime import date

fantasy = Flask(__name__)

fantasy.config['SECRET_KEY'] = 'Secret'
fantasy.config['MYSQL_USER'] = 'root'
fantasy.config['MYSQL_PASSWORD'] = '12345'
fantasy.config['MYSQL_HOST'] = 'localhost'
fantasy.config['MYSQL_DB'] = 'fantasy'
fantasy.config['MYSQL_CURSORCLASS'] = 'DictCursor'
db = MySQL(fantasy)


@fantasy.route('/', methods=['POST', 'GET'])
def home():
    new_line = db.connection.cursor()
    new_line.execute('select * from egyptian_table where position=1 or position=2 or position=3')
    egyptian_table = new_line.fetchall()
    new_line.execute('select * from egyptian_matches where team1="alahly" or team1="zamalek"')
    egyptian_matches = new_line.fetchall()
    new_line.execute('select * from premier_table where position=1 or position=2 or position=3')
    premier_table = new_line.fetchall()
    new_line.execute('select * from premier_matches where team1="arsenal" or team1="man city" or team1="man united"'
                     ' or team1="liverpool" or team1="chelsea"')
    premier_matches = new_line.fetchall()
    return render_template('home.html', egyptian_table=egyptian_table, egyptian_matches=egyptian_matches,
                           premier_table=premier_table, premier_matches=premier_matches)


@fantasy.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login.html')


@fantasy.route('/register', methods=['POST', 'GET'])
def register():
    return render_template('register.html')


@fantasy.route('/check_register', methods=['POST', 'GET'])
def check_register():
    if request.method == 'POST':
        name1 = request.form['name1']
        name2 = request.form['name2']
        name = name1 + ' ' + name2
        email = request.form['email']
        pwd1 = request.form['pwd1']
        pwd2 = request.form['pwd2']
        team_name = request.form['team']
        new_line = db.connection.cursor()
        new_line.execute('select email from users')
        list1 = [email['email'] for email in new_line]
        while email in list1:
            flash('Used email try another one')
            return redirect('/register')
        while True:
            if pwd1 == pwd2:
                break
            else:
                flash('Passwords are not the same')
                return redirect('/register')
        new_line = db.connection.cursor()
        new_line.execute('select team_name from users')
        list2 = [team['team_name'] for team in new_line]
        while team_name in list2:
            flash('Used team name try another one')
            return redirect('/register')
        new_line = db.connection.cursor()
        sql = 'insert into users (name,email,pwd,team_name) values (%s,%s,%s,%s)'
        values = (name, email, pwd1, team_name)
        new_line.execute(sql, values)
        sql = 'insert into premier_teams (team_name) values (%s)'
        values = (team_name,)
        new_line.execute(sql, values)
        sql = 'insert into egyptian_teams (team_name) values (%s)'
        values = (team_name,)
        new_line.execute(sql, values)
        db.connection.commit()
        return redirect('/login')


@fantasy.route('/about', methods=['POST', 'GET'])
def about():
    return render_template('about.html')


@fantasy.route('/egyptian_matches', methods=['POST', 'GET'])
def egyptian_matches():
    new_line = db.connection.cursor()
    new_line.execute('select * from egyptian_matches')
    matches = new_line.fetchall()
    return render_template('egyptian_matches.html', matches=matches)


@fantasy.route('/premier_matches', methods=['POST', 'GET'])
def premier_matches():
    new_line = db.connection.cursor()
    new_line.execute('select * from premier_matches')
    matches = new_line.fetchall()
    return render_template('premier_matches.html', matches=matches)


@fantasy.route('/egyptian_table', methods=['POST', 'GET'])
def egyptian_table():
    new_line = db.connection.cursor()
    new_line.execute('select * from egyptian_table')
    table = new_line.fetchall()
    return render_template('egyptian_table.html', table=table)


@fantasy.route('/premier_table', methods=['POST', 'GET'])
def premier_table():
    new_line = db.connection.cursor()
    new_line.execute('select * from premier_table')
    table = new_line.fetchall()
    return render_template('premier_table.html', table=table)


@fantasy.route('/egyptian_results', methods=['POST', 'GET'])
def egyptian_results():
    new_line = db.connection.cursor()
    new_line.execute('select * from egyptian_results')
    results = new_line.fetchall()
    return render_template('egyptian_results.html', results=results)


@fantasy.route('/premier_results', methods=['POST', 'GET'])
def premier_results():
    new_line = db.connection.cursor()
    new_line.execute('select * from premier_results')
    results = new_line.fetchall()
    return render_template('premier_results.html', results=results)


@fantasy.route('/control', methods=['POST', 'GET'])
def control():
    return render_template('control.html')


@fantasy.route('/my_team', methods=['POST', 'GET'])
def my_team():
    global team_name
    if request.method == 'POST':
        email = request.form['email']
        new_line = db.connection.cursor()
        new_line.execute('select email from users')
        list1 = [email['email'] for email in new_line]
        if email == 'control@control.com':
            pwd = request.form['pwd']
            new_line = db.connection.cursor()
            new_line.execute(f"select pwd from users where email='{email}'")
            list2 = [pwd['pwd'] for pwd in new_line]
            if pwd in list2:
                return redirect('/control')
            else:
                flash('Wrong password please try again')
                return redirect('/login')
        elif email in list1:
            pwd = request.form['pwd']
            new_line = db.connection.cursor()
            new_line.execute(f"select pwd from users where email='{email}'")
            list2 = [pwd['pwd'] for pwd in new_line]
            if pwd in list2:
                new_line = db.connection.cursor()
                new_line.execute(f"select team_name from users where email='{email}'")
                list3 = [name['team_name'] for name in new_line]
                team_name = list3[0]
                session['team_name'] = team_name
                return redirect('/my_team')
            else:
                flash('Wrong password please try again')
                return redirect('/login')
        else:
            flash('Email not found please register first')
            return redirect('/login')
    else:
        if 'team_name' in session:
            new_line = db.connection.cursor()
            new_line.execute('select * from egyptian_table where position=1 or position=2 or position=3')
            egyptian_table = new_line.fetchall()
            new_line.execute('select * from egyptian_matches where team1="alahly" or team1="zamalek"')
            egyptian_matches = new_line.fetchall()
            new_line.execute('select * from premier_table where position=1 or position=2 or position=3')
            premier_table = new_line.fetchall()
            new_line.execute(
                'select * from premier_matches where team1="arsenal" or team1="man city" or team1="man united"'
                ' or team1="liverpool" or team1="chelsea"')
            premier_matches = new_line.fetchall()
            return render_template('home2.html', egyptian_table=egyptian_table, egyptian_matches=egyptian_matches,
                                   premier_table=premier_table, premier_matches=premier_matches, team_name=team_name)
        else:
            return redirect('/login')


@fantasy.route('/my_team/egyptian/pick_team', methods=['POST', 'GET'])
def egyptian_pick_team():
    date1 = date.today()
    date1 = str(date1)
    date1 = date1.split('-')
    date1.reverse()
    date1 = '-'.join(date1)
    if date1 < '20-10-2024':
        return render_template('egyptian_pick_team.html', team_name=team_name)
    else:
        flash('The new league will start in 15-10-2022')
        return redirect('/my_team/egyptian')


@fantasy.route('/my_team/premier/pick_team', methods=['POST', 'GET'])
def premier_pick_team():
    date1 = date.today()
    date1 = str(date1)
    date1 = date1.split('-')
    date1.reverse()
    date1 = '-'.join(date1)
    if date1 < '20-10-2024':
        return render_template('premier_pick_team.html', team_name=team_name)
    else:
        flash('The deadline was 01-09-2022...The new week will start in 05-10-2022 and its deadline is 08-10-2022')
        return redirect('/my_team/premier')


@fantasy.route('/my_team/egyptian/players', methods=['POST', 'GET'])
def egyptian_players():
    new_line = db.connection.cursor()
    new_line.execute('select * from egyptian_players')
    players = new_line.fetchall()
    return render_template('egyptian_players.html', players=players)


@fantasy.route('/my_team/premier/players', methods=['POST', 'GET'])
def premier_players():
    new_line = db.connection.cursor()
    new_line.execute('select * from premier_players')
    players = new_line.fetchall()
    return render_template('premier_players.html', players=players)


@fantasy.route('/my_team/egyptian/points', methods=['POST', 'GET'])
def my_team_egyptian_points():
    global pgk, pd1, pd2, pd3, pd4, pm1, pm2, pm3, pm4, pf1, pf2, gk, d1, d2, d3, d4, m1, m2, m3, m4, f1, f2, extra, \
        captain
    if request.method == 'POST':
        new_line = db.connection.cursor()
        new_line.execute(f'select * from egyptian_teams where team_name="{team_name}"')
        for i in new_line:
            if i['gk'] == 'empty' or i['d1'] == 'empty' or i['d1'] == 'empty' or i['d1'] == 'empty' or\
                    i['d1'] == 'empty' or i['d1'] == 'empty' or i['d1'] == 'empty' or i['d1'] == 'empty' or\
                    i['d1'] == 'empty' or i['d1'] == 'empty' or i['d1'] == 'empty' or i['d1'] == 'empty':
                flash('Pick a team first')
                return redirect('/my_team/egyptian')
            gk = i['gk']
            d1 = i['d1']
            d2 = i['d2']
            d3 = i['d3']
            d4 = i['d4']
            m1 = i['m1']
            m2 = i['m2']
            m3 = i['m3']
            m4 = i['m4']
            f1 = i['f1']
            f2 = i['f2']
            captain = i['captain']
            new_line.execute(f'select * from egyptian_players')
            for j in new_line:
                if j['player'] == gk:
                    pgk = j['week_points']
                    if j['player'] == captain:
                        extra = j['week_points']
                elif j['player'] == d1:
                    pd1 = j['week_points']
                    if j['player'] == captain:
                        extra = j['week_points']
                elif j['player'] == d2:
                    pd2 = j['week_points']
                    if j['player'] == captain:
                        extra = j['week_points']
                elif j['player'] == d3:
                    pd3 = j['week_points']
                    if j['player'] == captain:
                        extra = j['week_points']
                elif j['player'] == d4:
                    pd4 = j['week_points']
                    if j['player'] == captain:
                        extra = j['week_points']
                elif j['player'] == m1:
                    pm1 = j['week_points']
                    if j['player'] == captain:
                        extra = j['week_points']
                elif j['player'] == m2:
                    pm2 = j['week_points']
                    if j['player'] == captain:
                        extra = j['week_points']
                elif j['player'] == m3:
                    pm3 = j['week_points']
                    if j['player'] == captain:
                        extra = j['week_points']
                elif j['player'] == m4:
                    pm4 = j['week_points']
                    if j['player'] == captain:
                        extra = j['week_points']
                elif j['player'] == f1:
                    pf1 = j['week_points']
                    if j['player'] == captain:
                        extra = j['week_points']
                elif j['player'] == f2:
                    pf2 = j['week_points']
                    if j['player'] == captain:
                        extra = j['week_points']
        score = pgk + pd1 + pd2 + pd3 + pd4 + pm1 + pm2 + pm3 + pm4 + pf1 + pf2 + extra
        # every week the points restart
        new_line.execute(f'update users set points="{score}" where team_name="{team_name}"')
        db.connection.commit()
        new_line.execute('select * from users')
        average = 0
        for k in new_line:
            average = (average + int(k['points']))
        average = average // 3
        new_line.execute('select points from users')
        new_line.fetchall()
        list1 = [i['points'] for i in new_line]
        highest = max(list1)
        return render_template('egyptian_points.html', gk=gk, d1=d1, d2=d2, d3=d3, d4=d4, m1=m1, m2=m2, m3=m3, m4=m4,
                               f1=f1, f2=f2, captain=captain, team_name=team_name, pgk=pgk, pd1=pd1, pd2=pd2, pd3=pd3,
                               pd4=pd4, pm1=pm1, pm2=pm2, pm3=pm3, pm4=pm4, pf1=pf1, pf2=pf2, score=score,
                               average=average, highest=highest, extra=extra)


@fantasy.route('/my_team/premier/points', methods=['POST', 'GET'])
def my_team_premier_points():
    global pgk, pd1, pd2, pd3, pd4, pm1, pm2, pm3, pm4, pf1, pf2, gk, d1, d2, d3, d4, m1, m2, m3, m4, f1, f2, extra, \
        captain
    if request.method == 'POST':
        new_line = db.connection.cursor()
        new_line.execute(f'select * from premier_teams where team_name="{team_name}"')
        for i in new_line:
            if i['gk'] == 'empty' or i['d1'] == 'empty' or i['d1'] == 'empty' or i['d1'] == 'empty' or\
                    i['d1'] == 'empty' or i['d1'] == 'empty' or i['d1'] == 'empty' or i['d1'] == 'empty' or\
                    i['d1'] == 'empty' or i['d1'] == 'empty' or i['d1'] == 'empty' or i['d1'] == 'empty':
                flash('Pick a team first')
                return redirect('/my_team/premier')
            gk = i['gk']
            d1 = i['d1']
            d2 = i['d2']
            d3 = i['d3']
            d4 = i['d4']
            m1 = i['m1']
            m2 = i['m2']
            m3 = i['m3']
            m4 = i['m4']
            f1 = i['f1']
            f2 = i['f2']
            captain = i['captain']
            new_line.execute(f'select * from premier_players')
            for j in new_line:
                if j['player'] == gk:
                    pgk = j['week_points']
                    if j['player'] == captain:
                        extra = j['week_points']
                elif j['player'] == d1:
                    pd1 = j['week_points']
                    if j['player'] == captain:
                        extra = j['week_points']
                elif j['player'] == d2:
                    pd2 = j['week_points']
                    if j['player'] == captain:
                        extra = j['week_points']
                elif j['player'] == d3:
                    pd3 = j['week_points']
                    if j['player'] == captain:
                        extra = j['week_points']
                elif j['player'] == d4:
                    pd4 = j['week_points']
                    if j['player'] == captain:
                        extra = j['week_points']
                elif j['player'] == m1:
                    pm1 = j['week_points']
                    if j['player'] == captain:
                        extra = j['week_points']
                elif j['player'] == m2:
                    pm2 = j['week_points']
                    if j['player'] == captain:
                        extra = j['week_points']
                elif j['player'] == m3:
                    pm3 = j['week_points']
                    if j['player'] == captain:
                        extra = j['week_points']
                elif j['player'] == m4:
                    pm4 = j['week_points']
                    if j['player'] == captain:
                        extra = j['week_points']
                elif j['player'] == f1:
                    pf1 = j['week_points']
                    if j['player'] == captain:
                        extra = j['week_points']
                elif j['player'] == f2:
                    pf2 = j['week_points']
                    if j['player'] == captain:
                        extra = j['week_points']
        score = pgk + pd1 + pd2 + pd3 + pd4 + pm1 + pm2 + pm3 + pm4 + pf1 + pf2 + extra
        # every week the points restart
        new_line.execute(f'update users set points="{score}" where team_name="{team_name}"')
        db.connection.commit()
        new_line.execute('select * from users')
        average = 0
        for k in new_line:
            average = (average + int(k['points']))
        average = average // 3
        new_line.execute('select points from users')
        new_line.fetchall()
        list1 = [i['points'] for i in new_line]
        highest = max(list1)
        return render_template('premier_points.html', gk=gk, d1=d1, d2=d2, d3=d3, d4=d4, m1=m1, m2=m2, m3=m3, m4=m4,
                               f1=f1, f2=f2, captain=captain, team_name=team_name, pgk=pgk, pd1=pd1, pd2=pd2, pd3=pd3,
                               pd4=pd4, pm1=pm1, pm2=pm2, pm3=pm3, pm4=pm4, pf1=pf1, pf2=pf2, score=score,
                               average=average, highest=highest, extra=extra)


@fantasy.route('/egyptian/points', methods=['POST', 'GET'])
def egyptian_points():
    if request.method == 'POST':
        gk = request.form['gk']
        d1 = request.form['d1']
        d2 = request.form['d2']
        d3 = request.form['d3']
        d4 = request.form['d4']
        m1 = request.form['m1']
        m2 = request.form['m2']
        m3 = request.form['m3']
        m4 = request.form['m4']
        f1 = request.form['f1']
        f2 = request.form['f2']
        captain = request.form['captain']
        new_line = db.connection.cursor()
        new_line.execute(f'update egyptian_teams set gk="{gk}" where team_name="{team_name}"')
        new_line.execute(f'update egyptian_teams set d1="{d1}" where team_name="{team_name}"')
        new_line.execute(f'update egyptian_teams set d2="{d2}" where team_name="{team_name}"')
        new_line.execute(f'update egyptian_teams set d3="{d3}" where team_name="{team_name}"')
        new_line.execute(f'update egyptian_teams set d4="{d4}" where team_name="{team_name}"')
        new_line.execute(f'update egyptian_teams set m1="{m1}" where team_name="{team_name}"')
        new_line.execute(f'update egyptian_teams set m2="{m2}" where team_name="{team_name}"')
        new_line.execute(f'update egyptian_teams set m3="{m3}" where team_name="{team_name}"')
        new_line.execute(f'update egyptian_teams set m4="{m4}" where team_name="{team_name}"')
        new_line.execute(f'update egyptian_teams set f1="{f1}" where team_name="{team_name}"')
        new_line.execute(f'update egyptian_teams set f2="{f2}" where team_name="{team_name}"')
        new_line.execute(f'update egyptian_teams set captain="{captain}" where team_name="{team_name}"')
        db.connection.commit()
        flash('Picked team successfully')
        return redirect('/my_team/egyptian')


@fantasy.route('/premier/points', methods=['POST', 'GET'])
def premier_points():
    if request.method == 'POST':
        gk = request.form['gk']
        d1 = request.form['d1']
        d2 = request.form['d2']
        d3 = request.form['d3']
        d4 = request.form['d4']
        m1 = request.form['m1']
        m2 = request.form['m2']
        m3 = request.form['m3']
        m4 = request.form['m4']
        f1 = request.form['f1']
        f2 = request.form['f2']
        captain = request.form['captain']
        new_line = db.connection.cursor()
        new_line.execute(f'update premier_teams set gk="{gk}" where team_name="{team_name}"')
        new_line.execute(f'update premier_teams set d1="{d1}" where team_name="{team_name}"')
        new_line.execute(f'update premier_teams set d2="{d2}" where team_name="{team_name}"')
        new_line.execute(f'update premier_teams set d3="{d3}" where team_name="{team_name}"')
        new_line.execute(f'update premier_teams set d4="{d4}" where team_name="{team_name}"')
        new_line.execute(f'update premier_teams set m1="{m1}" where team_name="{team_name}"')
        new_line.execute(f'update premier_teams set m2="{m2}" where team_name="{team_name}"')
        new_line.execute(f'update premier_teams set m3="{m3}" where team_name="{team_name}"')
        new_line.execute(f'update premier_teams set m4="{m4}" where team_name="{team_name}"')
        new_line.execute(f'update premier_teams set f1="{f1}" where team_name="{team_name}"')
        new_line.execute(f'update premier_teams set f2="{f2}" where team_name="{team_name}"')
        new_line.execute(f'update premier_teams set captain="{captain}" where team_name="{team_name}"')
        db.connection.commit()
        flash('Picked team successfully')
        return redirect('/my_team/premier')


@fantasy.route('/my_team/egyptian', methods=['POST', 'GET'])
def my_team_egyptian():
    new_line = db.connection.cursor()
    new_line.execute('select * from egyptian_table where position=1 or position=2 or position=3')
    egyptian_table = new_line.fetchall()
    new_line.execute('select * from egyptian_matches where team1="alahly" or team1="zamalek"')
    egyptian_matches = new_line.fetchall()
    return render_template('my_team_egyptian.html', egyptian_table=egyptian_table, egyptian_matches=egyptian_matches,
                           team_name=team_name)


@fantasy.route('/my_team/premier', methods=['POST', 'GET'])
def my_team_premier():
    new_line = db.connection.cursor()
    new_line.execute('select * from premier_table where position=1 or position=2 or position=3')
    premier_table = new_line.fetchall()
    new_line.execute('select * from premier_matches where team1="arsenal" or team1="man city" or team1="man united"'
                     ' or team1="liverpool" or team1="chelsea"')
    premier_matches = new_line.fetchall()
    return render_template('my_team_premier.html', premier_table=premier_table, premier_matches=premier_matches,
                           team_name=team_name)


@fantasy.route('/logout', methods=['POST', 'GET'])
def logout():
    if request.method == 'POST':
        session.pop('team_name')
        return redirect('/')


@fantasy.route('/control_egyptian_players', methods=['POST', 'GET'])
def control_egyptian_players():
    if request.method == 'POST':
        new_line = db.connection.cursor()
        new_line.execute('select * from egyptian_players')
        players = new_line.fetchall()
        return render_template('control_egyptian_players.html', players=players)


@fantasy.route('/control_premier_players', methods=['POST', 'GET'])
def control_premier_players():
    new_line = db.connection.cursor()
    new_line.execute('select * from premier_players')
    players = new_line.fetchall()
    return render_template('control_premier_players.html', players=players)


@fantasy.route('/control_egyptian_players2', methods=['POST', 'GET'])
def control_egyptian_players2():
    global total_points, week_points
    if request.method == 'POST':
        player = request.form['player']
        added_points = request.form['points']
        week_points = int(added_points)
        new_line = db.connection.cursor()
        new_line.execute(f'select total_points from egyptian_players where player="{player}"')
        for points in new_line:
            total_points = points['total_points'] + int(added_points)
        new_line.execute(f'update egyptian_players set total_points={total_points} where player="{player}"')
        new_line.execute(f'update egyptian_players set week_points={week_points} where player="{player}"')
        db.connection.commit()
        return redirect('/control_egyptian_players')


@fantasy.route('/control_premier_players2', methods=['POST', 'GET'])
def control_premier_players2():
    global total_points, week_points
    if request.method == 'POST':
        player = request.form['player']
        added_points = request.form['points']
        week_points = int(added_points)
        new_line = db.connection.cursor()
        new_line.execute(f'select total_points from premier_players where player="{player}"')
        for points in new_line:
            total_points = points['total_points'] + int(added_points)
        new_line.execute(f'update premier_players set total_points={total_points} where player="{player}"')
        new_line.execute(f'update premier_players set week_points={week_points} where player="{player}"')
        db.connection.commit()
        return redirect('/control_premier_players')


@fantasy.route('/control_egyptian_table', methods=['POST', 'GET'])
def control_egyptian_table():
    # if request.method == 'POST':
    new_line = db.connection.cursor()
    new_line.execute('select * from egyptian_table')
    table = new_line.fetchall()
    return render_template('control_egyptian_table.html', table=table)


@fantasy.route('/control_premier_table', methods=['POST', 'GET'])
def control_premier_table():
    # if request.method == 'POST':
    new_line = db.connection.cursor()
    new_line.execute('select * from premier_table')
    table = new_line.fetchall()
    return render_template('control_premier_table.html', table=table)


@fantasy.route('/control_egyptian_table2', methods=['POST', 'GET'])
def control_egyptian_table2():
    if request.method == 'POST':
        club1 = request.form['club']
        position1 = request.form['position']
        win1 = request.form['win']
        draw1 = request.form['draw']
        lose1 = request.form['lose']
        points1 = request.form['points']
        gd1 = request.form['gd']
        new_line = db.connection.cursor()
        new_line.execute(f'select * from egyptian_table where club="{club1}"')
        table = new_line.fetchall()[0]
        played = table['played']
        win = table['win']
        draw = table['draw']
        lose = table['lose']
        points = table['points']
        gd = table['gd']
        played = played + 1
        win = win + int(win1)
        draw = draw + int(draw1)
        lose = lose + int(lose1)
        points = points + int(points1)
        gd = gd + int(gd1)
        new_line.execute(f'update egyptian_table set position="{position1}" where club="{club1}"')
        new_line.execute(f'update egyptian_table set played="{played}" where club="{club1}"')
        new_line.execute(f'update egyptian_table set win="{win}" where club="{club1}"')
        new_line.execute(f'update egyptian_table set draw="{draw}" where club="{club1}"')
        new_line.execute(f'update egyptian_table set lose="{lose}" where club="{club1}"')
        new_line.execute(f'update egyptian_table set points="{points}" where club="{club1}"')
        new_line.execute(f'update egyptian_table set gd="{gd}" where club="{club1}"')
        db.connection.commit()
        return redirect('/control_egyptian_table')


@fantasy.route('/control_premier_table2', methods=['POST', 'GET'])
def control_premier_table2():
    if request.method == 'POST':
        club1 = request.form['club']
        position1 = request.form['position']
        win1 = request.form['win']
        draw1 = request.form['draw']
        lose1 = request.form['lose']
        points1 = request.form['points']
        gd1 = request.form['gd']
        new_line = db.connection.cursor()
        new_line.execute(f'select * from premier_table where club="{club1}"')
        table = new_line.fetchall()[0]
        played = table['played']
        win = table['win']
        draw = table['draw']
        lose = table['lose']
        points = table['points']
        gd = table['gd']
        played = played + 1
        win = win + int(win1)
        draw = draw + int(draw1)
        lose = lose + int(lose1)
        points = points + int(points1)
        gd = gd + int(gd1)
        new_line.execute(f'update premier_table set position="{position1}"+20 where position="{position1}"')
        new_line.execute(f'update premier_table set position="{position1}" where club="{club1}"')
        new_line.execute(f'update premier_table set played="{played}" where club="{club1}"')
        new_line.execute(f'update premier_table set win="{win}" where club="{club1}"')
        new_line.execute(f'update premier_table set draw="{draw}" where club="{club1}"')
        new_line.execute(f'update premier_table set lose="{lose}" where club="{club1}"')
        new_line.execute(f'update premier_table set points="{points}" where club="{club1}"')
        new_line.execute(f'update premier_table set gd="{gd}" where club="{club1}"')
        db.connection.commit()
        return redirect('/control_premier_table')


@fantasy.route('/egyptian_reset', methods=['POST', 'GET'])
def egyptian_reset():
    if request.method == 'POST':
        new_line = db.connection.cursor()
        # new_line.execute('update egyptian_teams set gk="empty"')
        # new_line.execute('update egyptian_teams set d1="empty"')
        # new_line.execute('update egyptian_teams set d2="empty"')
        # new_line.execute('update egyptian_teams set d3="empty"')
        # new_line.execute('update egyptian_teams set d4="empty"')
        # new_line.execute('update egyptian_teams set m1="empty"')
        # new_line.execute('update egyptian_teams set m2="empty"')
        # new_line.execute('update egyptian_teams set m3="empty"')
        # new_line.execute('update egyptian_teams set m4="empty"')
        # new_line.execute('update egyptian_teams set f1="empty"')
        # new_line.execute('update egyptian_teams set f2="empty"')
        # new_line.execute('update egyptian_teams set captain="empty"')
        new_line.execute('update egyptian_teams set points=0')
        new_line.execute('update egyptian_players set week_points=0')
        new_line.execute('delete from egyptian_matches')
        new_line.execute('delete from egyptian_results')
        db.connection.commit()
        return redirect('/control')


@fantasy.route('/premier_reset', methods=['POST', 'GET'])
def premier_reset():
    if request.method == 'POST':
        new_line = db.connection.cursor()
        # new_line.execute('update premier_teams set gk="empty"')
        # new_line.execute('update premier_teams set d1="empty"')
        # new_line.execute('update premier_teams set d2="empty"')
        # new_line.execute('update premier_teams set d3="empty"')
        # new_line.execute('update premier_teams set d4="empty"')
        # new_line.execute('update premier_teams set m1="empty"')
        # new_line.execute('update premier_teams set m2="empty"')
        # new_line.execute('update premier_teams set m3="empty"')
        # new_line.execute('update premier_teams set m4="empty"')
        # new_line.execute('update premier_teams set f1="empty"')
        # new_line.execute('update premier_teams set f2="empty"')
        # new_line.execute('update premier_teams set captain="empty"') (all^ not to change the team every week)
        # new_line.execute('update premier_teams set points=0') (needs to be deleted)
        new_line.execute('update premier_players set week_points=0')
        new_line.execute('delete from premier_matches')
        new_line.execute('delete from premier_results')
        db.connection.commit()
        return redirect('/control')


@fantasy.route('/control_egyptian_matches', methods=['POST', 'GET'])
def control_egyptian_matches():
    if request.method == 'POST':
        new_line = db.connection.cursor()
        new_line.execute('select * from egyptian_matches')
        matches = new_line.fetchall()
        return render_template('control_egyptian_matches.html', matches=matches)
    else:
        new_line = db.connection.cursor()
        new_line.execute('select * from egyptian_matches')
        matches = new_line.fetchall()
        return render_template('control_egyptian_matches.html', matches=matches)


@fantasy.route('/control_premier_matches', methods=['POST', 'GET'])
def control_premier_matches():
    if request.method == 'POST':
        new_line = db.connection.cursor()
        new_line.execute('select * from premier_matches')
        matches = new_line.fetchall()
        return render_template('control_premier_matches.html', matches=matches)
    else:
        new_line = db.connection.cursor()
        new_line.execute('select * from premier_matches')
        matches = new_line.fetchall()
        return render_template('control_premier_matches.html', matches=matches)


@fantasy.route('/control_egyptian_matches2', methods=['POST', 'GET'])
def control_egyptian_matches2():
    if request.method == 'POST':
        team1 = request.form['team1']
        team2 = request.form['team2']
        day = request.form['day']
        date = request.form['date']
        hour = request.form['hour']
        new_line = db.connection.cursor()
        sql = 'insert into egyptian_matches(team1,team2,day,date,hour)values(%s,%s,%s,%s,%s)'
        values = (team1, team2, day, date, hour)
        new_line.execute(sql, values)
        db.connection.commit()
        return redirect('/control_egyptian_matches')


@fantasy.route('/control_premier_matches2', methods=['POST', 'GET'])
def control_premier_matches2():
    if request.method == 'POST':
        team1 = request.form['team1']
        team2 = request.form['team2']
        day = request.form['day']
        date = request.form['date']
        hour = request.form['hour']
        new_line = db.connection.cursor()
        sql = 'insert into premier_matches(team1,team2,day,date,hour)values(%s,%s,%s,%s,%s)'
        values = (team1, team2, day, date, hour)
        new_line.execute(sql, values)
        db.connection.commit()
        return redirect('/control_premier_matches')


@fantasy.route('/control_egyptian_results', methods=['POST', 'GET'])
def control_egyptian_results():
    if request.method == 'POST':
        new_line = db.connection.cursor()
        new_line.execute('select * from egyptian_results')
        results = new_line.fetchall()
        return render_template('control_egyptian_results.html', results=results)
    else:
        new_line = db.connection.cursor()
        new_line.execute('select * from egyptian_results')
        results = new_line.fetchall()
        return render_template('control_egyptian_results.html', results=results)


@fantasy.route('/control_premier_results', methods=['POST', 'GET'])
def control_premier_results():
    if request.method == 'POST':
        new_line = db.connection.cursor()
        new_line.execute('select * from premier_results')
        results = new_line.fetchall()
        return render_template('control_premier_results.html', results=results)
    else:
        new_line = db.connection.cursor()
        new_line.execute('select * from premier_results')
        results = new_line.fetchall()
        return render_template('control_premier_results.html', results=results)


@fantasy.route('/control_egyptian_results2', methods=['POST', 'GET'])
def control_egyptian_results2():
    if request.method == 'POST':
        team1 = request.form['team1']
        team2 = request.form['team2']
        result = request.form['result']
        new_line = db.connection.cursor()
        sql = 'insert into egyptian_results(team1,team2,result)values(%s,%s,%s)'
        values = (team1, team2, result)
        new_line.execute(sql, values)
        db.connection.commit()
        return redirect('/control_egyptian_results')


@fantasy.route('/control_premier_results2', methods=['POST', 'GET'])
def control_premier_results2():
    if request.method == 'POST':
        team1 = request.form['team1']
        team2 = request.form['team2']
        result = request.form['result']
        new_line = db.connection.cursor()
        sql = 'insert into premier_results(team1,team2,result)values(%s,%s,%s)'
        values = (team1, team2, result)
        new_line.execute(sql, values)
        db.connection.commit()
        return redirect('/control_premier_results')


if __name__ == '__main__':
    fantasy.run(debug=True)
