from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
app.users = {}
app.posts = {}
app.idCnt = 1

@app.route('/')
def root():
    return """
    <h1>mainSNS</h1>
    <div>
        <button>메인 페이지</button>
        <button>회원 가입</button>
        <button>포스팅</button>
    </div>
    """
    
@app.route('/main', method=['GET'])
def main():
    return render_template('main.html', users=app.users)

@app.route('/sign-up', methods=['GET'])
def signUp():
    return render_template('signup.html')

@app.route('/sign-up', methods=['POST'])
    newUser = request.json
    newUser['id'] = app.idCnt
    app.users[app.idCnt] = newUser
    app.idCnt += 1
    return jsonify(newUser)

@app.route('/post', methods=['POST'])
def post():
    payload = request.json
    userID = int(payload['id'])
    msg = payload['msg']
    
    if userID not in app.users:
        return '사용자가 존재하지 않습니다', 400
    if len(msg) > 300:
        return '30자를 초과했습니다', 400
    
    app.posts.append({
        'user_id' : userID,
        'post' : msg
    })
    return '성공', 200

@app.route('/follow', methods=['post'])
def follow():
    payload = request.json
    userID = int (payload['id'])
    userIDToFollow = int(payload['follow'])
    
    if userID not in app.users or userIDToFollow not in app.users:
        return '사용자가 존재하지 않습니다', 400
    
    user = app.users[userID]
    if user.get('follow'):
        user['follow'].append(userIDToFollow)
        user['follow'] = list(set(user['follow']))
    else:
        user['follow'] = [userIDToFollow]
    return jsonify(user)

@app.route('/unfollow', methods=['post'])
def follow():
    payload = request.json
    userID = int (payload['id'])
    userIDToFollow = int(payload['unfollow'])
    
    if userID not in app.users or userIDToFollow not in app.users:
        return '사용자가 존재하지 않습니다', 400
    
    user = app.users[userID]
    if user.get('follow'):
        try:     user['follow'].remove(userIDToFollow)
        except:  pass
    else:
        user['follow'] = []
    return jsonify(user)

@app.route('/timeline/<int:userID>', methods=['GET'])
def timeline(userID):
    if userID not in app.users:
        return '사용자가 존재하지 않습니다', 400
    if app.users[userID].get('follow'):
        followList = set(app.users[userID]['follow'])
    else:
        followList = set()
    followList.add(userID)
    timeline= [msg for msg in app.posts if msg['userID'] in followList]
    
    return jsonify({
        'userID': userID,
        'timeline': timeline
    })

if __name__ == '__main__':
    app.run()