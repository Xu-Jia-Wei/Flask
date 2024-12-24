from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 配置数据库（使用SQLite）
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db = SQLAlchemy(app)

# 玩家模型
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    score = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f"<Player {self.username}, Score {self.score}>"

# 创建数据库表
with app.app_context():
    db.create_all()

# 首页路由，渲染游戏页面
@app.route('/')
def index():
    players = Player.query.all()  # 获取所有玩家
    return render_template('index.html', players=players)

# 保存玩家得分
@app.route('/save_score', methods=['POST'])
def save_score():
    username = request.form['username']
    score = request.form['score']
    
    # 查找玩家
    player = Player.query.filter_by(username=username).first()
    if player:
        player.score = max(player.score, int(score))  # 保证玩家的分数不降低
    else:
        player = Player(username=username, score=score)
        db.session.add(player)
    
    db.session.commit()
    
    return jsonify(success=True, message="Score saved successfully!")

# 获取玩家得分历史
@app.route('/player_scores/<username>')
def player_scores(username):
    player = Player.query.filter_by(username=username).first()
    if player:
        return jsonify(username=player.username, score=player.score)
    return jsonify(message="Player not found"), 404

if __name__ == '__main__':
    app.run(debug=True)
