from flask import Flask, jsonify, request
app = Flask(__name__);
import base64
import pytesseract as tess
from PIL import Image
import cv2
import numpy as np
#myconfig = r'--psm 11 --oem 3'


@app.route('/getTextfromImg', methods = ['POST'])
def home():
    converted_string = ''
    if(request.method == 'POST'):

        # with open("imagetotext3.jpg", "rb") as image2string:
        #     converted_string = base64.b64encode(image2string.read())
        
        def getregistrationno(text):
            regno= text.find('REGN')
            startpoint = text.find(':', regno)
            if(startpoint == -1):
                return ''
        
            endpoint= text.find('\n',startpoint)
            
            registrationnum = text[startpoint+1 : endpoint].replace(" ","");
            regno=''
            counter=0
            for check in registrationnum:
                counter+=1
                if not (check.isalnum()) or counter > 11:
                    break
                regno += check
            return regno

        def getchasisNo(text):
            text = text.upper()
            startpoint2= text.find('CH NO')
            
            startpoint2 = startpoint2 + 8
            endpoint2 = text.find('\n' , startpoint2)
            chasisnum = text[startpoint2 : endpoint2]
            registrationdate = text[startpoint2-19 : startpoint2-11]
            if startpoint2 == 7:
                return '',registrationdate
            return chasisnum, registrationdate
        
        
        def getEngineNo(text):
            startpoint = text.find('ENO') + 6
            #endpoint = text.find('\n', startpoint)
            if startpoint == 5:
                return ''
            endpoint = startpoint+18
            engNo = text[startpoint:endpoint]
            engineNo = ''
            counter=0
            for check in engNo:
                
                if( (check == ' ' or check == '\n')  and counter>0):
                    break 
                else:
                    engineNo+=check
                    counter+=1
                
            return engineNo


        def getManufactureDate(text):
            test = text.upper()
            manufactureDate = ['MFG.DT','MFGO','MFGD','MFG.','MFG']
            startpoint=0
            for manufact in manufactureDate:
                k=text.find(manufact)
                if(k!=-1):
                    startpoint=k
                    break
            startpoint = startpoint + 10
            return text[startpoint : startpoint+ 7]
        
        def getName(text):
            startpoint = text.find('NAME') + 6
            endpoint = text.find('\n', startpoint)
            return text[startpoint:endpoint]
        
        def getFuelType(text):
            startpoint = text.find('FUEL') + 7
            return text[startpoint : startpoint + 7].replace(" ","")
        
        def getSNo(text):
            startpoint = text.find('OSNO') + 7
            return text[startpoint : startpoint+2].replace(" ","");
        def getModel(text):
            startpoint = text.find('MODEL') + 10
            endpoint =text.find('\n', startpoint)

            return text[startpoint : endpoint ]

        myconfig = r'--psm 4 --oem 3'
        #image reading

        # print('$$$$$', request.form.image)
        # fh = open("imageToSave.png", "wb")
        # fh.write(base64.b64decode(converted_string))
        # fh.close()
        img = Image.open('./imagetotext3.jpg');
        #img = Image.open('./imageToSave.png')

        text = tess.image_to_string(img, config=myconfig);

        manufactureDate = getManufactureDate(text)
        registrationNumber = getregistrationno(text)
        chasisNumber, registrationdate = getchasisNo(text)
        engineNumber = getEngineNo(text)
        name = getName(text)
        fuel = getFuelType(text)
        osNo = getSNo(text)
        model = getModel(text)
        data = {
            'RegistrationNumber' : registrationNumber,
            'Chasis Number' : chasisNumber,
            'EngineNumber'  : engineNumber,
            'RegistrationDate' : registrationdate,
            'ManufactureDate' : manufactureDate,
            'Name' : name,
            'FuelType' : fuel,
            'OsNo' : osNo,
            'Model' : model
        }
        print(text)       
        
        return jsonify({'data': data})


if __name__ == '__main__':
    app.run(debug = True)
    