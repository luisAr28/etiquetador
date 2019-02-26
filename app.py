import os
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
    nQuestions = request.form.get('nQuest',type=int)
    totalIm = request.form.get('ruta')
    jsonInf = "{\"category1\":{\"name\":\"" + str(request.form.get('nombre'))+"\",\"path\":\"images\/"+str(request.form.get('ruta'))+"\",\"quantity\":\""+str(request.form.get('nTotalImags'))+"\",\"numtags\":\""+str(request.form.get('nImags'))+"\",\"trak\":\""+str(request.form.get('ordAlet'))+"\",\"tags\":{"
    
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
    
    with open(pathFile, 'w') as outfile:
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
    jsonInfo4 = json.loads(jsonInfo3)
    hists = os.listdir(os.path.join(app.static_folder,jsonInfo2['category1']['path']))
    sorted(hists)
    hists = [jsonInfo2['category1']['path']+'/' + file for file in hists]

    
    return render_template('completeJson.html',jsonInfo2=jsonInfo2,hists=hists,jsonInfo4=jsonInfo4)

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
    #print(dat)
    #print(prueba)
    
    dataJ = "{"
    
    totalIm = request.form.get('cantidad',type=int)
    topQuest = totalIm*request.form.get('preguntas',type=int)
    #print(topQuest)

    questPerIm =  topQuest / totalIm
    contIm = 1
    contClass =1
    ultimoIndice = 0

    dataJ = dataJ+'"'+obtieneNomImag(str(request.form.get('img'+str(contIm))))+'"'+":[{"

    for i in range(0,topQuest):

        dataJ = dataJ +'"'+ "Classname"+str(contClass)+'":{"opt":"' 
        reqOpt = str(request.form.get('opt'+str(i+1)))
        if reqOpt != 'None':
            dataJ = dataJ+reqOpt
        
        dataJ=dataJ+'","text":"'+str(request.form.get('text'+str(i+1)))+'"}'

        if (i+1)==(contIm*questPerIm) and (i+1)!=topQuest:      
            contIm+=1
            contClass=1
            dataJ=dataJ+"}],"+'"'+obtieneNomImag(str(request.form.get('img'+str(contIm))))+'":[{'
        else:
            if (i+1)!=topQuest:
                dataJ=dataJ+","
                contClass+=1
        
    
   # for i in range(request.form.get('numberQ')):
    #    dataJ = dataJ + request.form.get('img{i+1}')
    
    dataJ = dataJ+"}]}"
    
    #print("Es: "+dataJ)
    
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

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.static_folder,'/images/'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
    
if __name__=="__main__":
    app.run(threaded=True,host="0.0.0.0", debug=True, port=5000)
