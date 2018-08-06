from flask import Flask, render_template,jsonify,request,redirect,url_for
app = Flask(__name__)

@app.route('/')
def main():
        return render_template('index.html');
    
@app.route('/processjson',methods=['POST'])
def processjson():
    
    data = request.get_json()
    
    name = data['name']
    location = data['location']
    randomlist = data['randomlist']
    
    return jsonify({'result':'Success','name':name, 'location':location,'randomin':randomlist[1]})

@app.route('/prueba',methods=['POST'])
def prueba():
    return "/tagging"


@app.route("/reqF",methods=['POST'])
def signF():
	_name = request.form['nombre']
	_ruta = request.form['ruta']
	_nImags = request.form['nImags']
	_nQuest = request.form['nQuest']
	_ordAlet = request.form.get('ordAlet')

	print(_ordAlet)

	if _name and _ruta and _nImags and _nQuest:
		return render_template('tag.html',_name=_name,_ruta=_name,_nImags=_nImags,_nQuest=_nQuest,_ordAlet=_ordAlet,questions=_nQuest);
	    #return json.dumps({'html':'<span>All fields good !!</span>'})
	else:
		return json.dumps({'html':'<span>Faltan !!</span>'})


@app.route('/tagging')
def tagging():
       return render_template('tag.html');
    
if __name__=="__main__":
    app.run(debug = True)