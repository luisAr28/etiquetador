import os
import random, collections
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

@app.route('/etiquetadoCon',methods=['POST'])
def etiquetadoCon():
    return "/continueTag"

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

	else:
		return json.dumps({'html':'<span>Faltan !!</span>'})

@app.route("/fillF",methods=['POST'])
def fillF():
    name= request.form.get('nombre')
    rout= request.form.get('ruta')
    nImgs= request.form.get('nImags')
    orAlet= request.form.get('ordAlet')
    questions = int(request.form.get('nQuest'))
    checkBound = request.form.get('boundyBox')

    if orAlet:
        valAlet="1"
        orAlet="checked"
    else:
        orAlet="unchecked"
        valAlet="0"

    if checkBound:
        valBound="1"
        checkBound="checked"
    else:
        checkBound="unchecked"
        valBound="0"

    print(orAlet)
    #if name and rout and nImags and questions:
    return render_template('otro.html',questions=questions,nameI=name,rout=rout,nImgs=nImgs,orAlet=orAlet,valAlet=valAlet,checkBound=checkBound,valBound=valBound)
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
    nQuestions = request.form.get('nQuest',type=int)
    totalIm = request.form.get('ruta')
    jsonInf = "{\"category1\":{\"name\":\"" + str(request.form.get('nombre'))+"\",\"path\":\"images\/"+str(request.form.get('ruta'))+"\",\"quantity\":\""+str(request.form.get('nTotalImags'))+"\",\"numtags\":\""+str(request.form.get('nImags'))+"\",\"trak\":\""+str(request.form.get('ordAlet'))+"\",\"boundy\":\""+str(request.form.get('checkBound'))+"\",\"tags\":{"
    
    for i in range(0,nQuestions):
        jsonInf = jsonInf+"\"classname"+str(i)+"\":{"
        jsonInf = jsonInf+"\"question\":\""+str(request.form.get('q'+str(i+1)))+"\",\"type\":"
        
        typeQuest = str(request.form.get('select'+str(i+1)))
        
        jsonInf = jsonInf+"\""+typeQuest+"\""
        
        if typeQuest != "text":
            jsonInf = jsonInf+",\"opt\":["
            options = str(request.form.get('opcIn'+str(i+1))).split(",")
            for y in range(0,len(options)):                
                jsonInf = jsonInf+"\""+options[y]+"\""
                if (y+1) != len(options):
                    jsonInf = jsonInf+","
            jsonInf = jsonInf+"]"
            
        jsonInf = jsonInf+",\"text\":\""+str(request.form.get('chText'+str(i+1)))+"\"}"
        
        if(i+1)!=nQuestions:
            jsonInf = jsonInf+","
    
    jsonInf = jsonInf+"}}}"
    #print(complete)
    #print(dat)
    #print(jsonInf)
    
    fileName = str(request.form.get('nombre'))
    pathFile = "static/json/"+fileName+".json"
    
    with open(pathFile, 'w',encoding="utf-8") as outfile:
        outfile.write(jsonInf)

    return json.dumps({'urlI':'/'})

@app.route('/tagging')
def tagging():
       return render_template('tag.html')
    
@app.route('/loadTag')
def loadTag():
       return render_template('lTag.html')
        
@app.route('/continueTag')
def continueTag():
       return render_template('conTag.html')
    
@app.route('/jForm',methods=['POST']) 
def jForm():
    file = request.files['fileJson']

    jsonInfo = file.read()
    jsonInfo = jsonInfo.decode('utf-8')
    jsonInfo2 = json.loads(jsonInfo)
    hists = os.listdir(os.path.join(app.static_folder,jsonInfo2['category1']['path']))
    sorted(hists)
    hists = [jsonInfo2['category1']['path']+'/' + file for file in hists]
    
    return render_template('jsonForm.html',jsonInfo2=jsonInfo2,hists=hists)
    
@app.route('/conForm',methods=['POST']) 
def conForm():
    file = request.files['fileJson']
    file2 = request.files['contJson']

    jsonInfo = file.read()
    jsonInfo = jsonInfo.decode('utf-8')
    jsonInfo2 = json.loads(jsonInfo)
    
    jsonInfo3 = file2.read()
    jsonInfo3 = jsonInfo3.decode('utf-8')
    jsonInfo4 = json.loads(jsonInfo3, object_pairs_hook=collections.OrderedDict)
    print(jsonInfo4)
    hists = os.listdir(os.path.join(app.static_folder,jsonInfo2['category1']['path']))
    sorted(hists)
    hists = [jsonInfo2['category1']['path']+'/' + file for file in hists]

    
    return render_template('completeJson.html',jsonInfo2=jsonInfo2,hists=hists,jsonInfo4=jsonInfo4)

@app.route('/jsonDat',methods=['POST']) 
def jsonDat():
    print("entrando")
    
    dataJ = "{"
    
    totalIm = int(request.form.get('cantidad',type=int))
    questPerIm = request.form.get('preguntas',type=int)  

    boundyAble = str(request.form.get('checkBoundy'))
    print(boundyAble)
    stringBoundyAble = "" 

    for i in range(0,totalIm):
        dataJ = dataJ+'"'+obtieneNomImag(str(request.form.get('img'+str(i+1))))+'":[{'
        countBoundy = str(request.form.get('contadorBoundy'+str(i+1)))
        arrayBoundy = countBoundy.split(",")

        for j in range(0,len(arrayBoundy)):
            if boundyAble=='1':
                stringBoundyAble = "}]"
                dataJ = dataJ+'"ClassSet'+str(j+1)+'":[{'
                dataJ = dataJ+'"Coords":{'
                dataJ = dataJ+'"x1":"'+evaluaValor(str(request.form.get('x1-'+str(i+1)+'-'+str(arrayBoundy[j]))))+'",'
                dataJ = dataJ+'"x2":"'+evaluaValor(str(request.form.get('x2-'+str(i+1)+'-'+str(arrayBoundy[j]))))+'",'
                dataJ = dataJ+'"y1":"'+evaluaValor(str(request.form.get('y1-'+str(i+1)+'-'+str(arrayBoundy[j]))))+'",'
                dataJ = dataJ+'"y2":"'+evaluaValor(str(request.form.get('y2-'+str(i+1)+'-'+str(arrayBoundy[j]))))+'"'
                dataJ = dataJ+"},"
                if (j+1)!=len(arrayBoundy):
                    stringBoundyAble = stringBoundyAble+","
            else:
                stringBoundyAble = ""

            for k in range(0,questPerIm):
                dataJ = dataJ + '"Classname'+str(k+1)+'":{'
                dataJ = dataJ + '"opt":"'+evaluaValor(str(request.form.get('opt-'+str(i+1)+'-'+str((k+1)*int(arrayBoundy[j])))))+'",'
                dataJ = dataJ + '"text":"'+evaluaValor(str(request.form.get('text-'+str(i+1)+'-'+str((k+1)*int(arrayBoundy[j])))))+'"'
                dataJ = dataJ+"}"
                if (k+1)!=questPerIm:
                    dataJ=dataJ+","
            
            dataJ = dataJ+stringBoundyAble

        dataJ = dataJ + "}]"

        if (i+1)!=totalIm:
                dataJ=dataJ+","
        

    dataJ = dataJ + '}'
    
    pathName = obtieneNomImag(str(request.form.get('path')))
    pathFile = "static/temp/"+pathName+".json"
    
    with open(pathFile, 'w') as outfile:
        outfile.write(dataJ)
    

    return json.dumps({'urlI':'/'})

@app.route('/downloadF/<path_file>')
def downloadF(path_file):
    print(path_file)
    return render_template('downJson.html',nFile='temp/'+path_file+'.json')

def obtieneNomImag(rutIm):
    index = rutIm.rfind('/')
    nom = rutIm[index+1:]
    
    return nom

def evaluaValor(valor):
    if valor == 'None':
        return ""
    return valor

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.static_folder,'/images/'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
    
if __name__=="__main__":
    app.run(threaded=True,host="0.0.0.0", debug=True, port=5000)
