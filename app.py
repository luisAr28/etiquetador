from flask import Flask, render_template,jsonify,request,redirect,url_for,json,Response,send_file,send_from_directory
from datetime import datetime
from werkzeug.datastructures import ImmutableMultiDict
from pprint import pprint
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

@app.route('/etiquetado',methods=['POST'])
def etiquetado():
    return "/loadTag"


@app.route("/reqF",methods=['POST'])
def signF():
	_name = request.form['nombre']
	_ruta = request.form['ruta']
	_nImags = request.form['nImags']
	_nQuest = request.form['nQuest']
	_ordAlet = request.form.get('ordAlet')

	print(_ordAlet)

	if _name and _ruta and _nImags and _nQuest:
		return json.dumps	({'pag':'tag.html','_name':_name,'_ruta':_name,'_nImags':_nImags,'_nQuest':_nQuest,'_ordAlet':_ordAlet,'questions':_nQuest});
		#return render_template("tag.html",'_name':_name,'_ruta':_name,'_nImags':_nImags,'_nQuest':_nQuest,'_ordAlet':_ordAlet,'questions':_nQuest);
	    #return json.dumps({'html':'<span>All fields good !!</span>'})
	else:
		return json.dumps({'html':'<span>Faltan !!</span>'})

@app.route("/fillF",methods=['POST'])
def fillF():
	name= request.form.get('nombre')
	rout= request.form.get('ruta')
	nImgs= request.form.get('nImags')
	orAlet= request.form.get('ordAlet')
	questions = int(request.form.get('nQuest'))
	if orAlet:
		valAlet="1"
		orAlet="checked"
	else:
		orAlet="unchecked"
		valAlet="0"
	print(orAlet)
	#if name and rout and nImags and questions:
	return render_template('otro.html',questions=questions,nameI=name,rout=rout,nImgs=nImgs,orAlet=orAlet,valAlet=valAlet)
	#else


@app.route("/saveJson",methods=['POST'])
def saveJson():
    now = datetime.now()
    complete = str(now.year)+str(now.month)+str(now.day)
    dat = request.form
    dat.to_dict(flat=False)
    #otro = str(request.form.get('nombre'))
    otro = str()
    otro = otro+complete
   
    print(complete)
    print(dat)
    print(otro)
   
   #createfolder = os.path.join('C:/Users/MyUser/Desktop/Project/', 'Fileuploads/', time_stamp,)
    #filename = request.form.get('nombre')
    #with open(filename, 'w') as f:
     #   json.dump(request.form, f)
    #return '/'
    return json.dumps({'urlI':'/'})

@app.route('/tagging')
def tagging():
       return render_template('tag.html')
    
@app.route('/loadTag')
def loadTag():
       return render_template('lTag.html')
    
@app.route('/jForm',methods=['POST']) 
def jForm():
    file = request.files['fileJson']
    #filename = secure_filename(file.filename) 
    #file.save(os.path.join(SITE_ROOT, "static/temp",filename))
    #filetype = magic.from_buffer(file.read())
    jsonInfo = file.read()
    jsonInfo = jsonInfo.decode('utf-8')
    jsonInfo2 = json.loads(jsonInfo)
    hists = os.listdir(os.path.join(app.static_folder,jsonInfo2['category1']['path']))
    hists = [jsonInfo2['category1']['path']+'/' + file for file in hists]
    #list = []
    #for i in range(jsonInfo2['category1']['quantity']):
    #      r=random.randint(1,100)
    #      if r not in list: list.append(r)
            
    print('\n'+jsonInfo)
    print(jsonInfo2['category1']['name'])
    
    return render_template('jsonForm.html',jsonInfo2=jsonInfo2,hists=hists)

@app.route('/jsonDat',methods=['POST']) 
def jsonDat():
    print("entrando")
    dat = request.form.get('opt1')
    prueba = request.form.get('text1')
   # dat.to_dict(flat=False)
#    dato = request.get_json()
    dat = request.form
    #dat = dict(request.form)
   # print(dato)
    print(dat)
    print(prueba)
    
    dataJ = "{"
    
    topQuest = request.form.get('preguntas',type=int)

    totalIm = request.form.get('cantidad',type=int)

    questPerIm =  topQuest / totalIm
    contIm = 1
    contClass =1

    dataJ = dataJ+obtieneNomImag(str(request.form.get('img'+str(contIm))))+":[{"

    for i in range(0,topQuest):
        dataJ = dataJ + "Classname"+str(contClass)+":{opt:"+ str(request.form.get('opt'+str(i+1)))+",text:"+str(request.form.get('text'+str(i+1)))+"}"

        if (i+1)==(contIm*questPerIm) and (i+1)!=topQuest:      
            contIm+=1
            contClass=1
            dataJ=dataJ+"}],"+obtieneNomImag(str(request.form.get('img'+str(contIm))))+":[{"
        else:
            if (i+1)!=topQuest:
                dataJ=dataJ+","
                contClass+=1
        
    
   # for i in range(request.form.get('numberQ')):
    #    dataJ = dataJ + request.form.get('img{i+1}')
    
    dataJ = dataJ+"}}"
    
    print("Es: "+dataJ)
    
    pathName = obtieneNomImag(str(request.form.get('path')))
    pathFile = "static/temp/"+pathName+".json"
    
    with open(pathFile, 'w') as outfile:
        outfile.write(dataJ)
    
    #fileSen = open(pathFile,'rb').read()
    
    
    #response.headers['Content-Type'] = 'application/json'
    #response.header['Content-Disposition'] = 'attatchment;filename='+pathName+'.json'
    
    #return response
    #print(Response(dataJ, mimetype='application/json',headers={'Content-Disposition':'attachment;filename=file.json'}))
    
    #return Response(dataJ, mimetype='application/json',headers={'Content-Disposition':'attachment;filename=file.json'})
    #response = Response(response=dataJ, status=200, mimetype="application/json")
    #return response
    #return send_file(pathFile, as_attachment=True)
    #return send_from_directory(directory='/static/temp', filename=pathName+'.json', as_attachment=True)
    #return send_file(json.dumps(dataJ), mimetype='application/json',attachment_filename='file.json',as_attachment=True)
    #return json.dumps({'urlI':'/downloadF','name':pathName})
    return json.dumps({'urlI':'/'})
    #return render_template('downJson.html');

#@app.route('/sendFile', methods=['POST'])
#def sendFile():
#    content = str(request.form['jsonval'])
#    return Response(content, 
#            mimetype='application/json',
#            headers={'Content-Disposition':'attachment;filename=file.json'})

@app.route('/downloadF/<path_file>')
def downloadF(path_file):
    print(path_file)
    return render_template('downJson.html',nFile='temp/'+path_file+'.json')

def obtieneNomImag(rutIm):
    index = rutIm.rfind('/')
    nom = rutIm[index+1:]
    
    return nom
    
if __name__=="__main__":
    app.run(debug = True)