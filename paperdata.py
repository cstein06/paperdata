import sqlite3, json, numpy, pickle, bson, base64

import matplotlib.pyplot as plt
import matplotlib.figure
import numpy as np

import types, inspect, re, codecs

import requests
  
# server = 'http://127.0.0.1:8080/'
server = 'https://lateral-attic-335719.nw.r.appspot.com/'

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return {"_TYPE_NDARRAY_LIST": obj.tolist()}
        elif isinstance(obj, types.FunctionType):
            return {"_TYPE_PYTHON_FUNCTION": inspect.getsource(obj)}
        elif isinstance(obj, Function):
            return {"_TYPE_PYTHON_FUNCTION": obj.source}
        elif isinstance(obj, matplotlib.figure.Figure):
            fig_pic = pickle.dumps(obj)
            encoded = base64.b64encode(fig_pic).decode("ascii")
            return {"_TYPE_MATPLOTLIB_FIG": encoded}
        elif isinstance(obj, bytes):
            return {"_TYPE_PICKLE_BYTES": base64.b64encode(obj).decode("ascii")} 
        else:
            return super(CustomEncoder, self).default(obj)

class Function():
  def __init__(self, source):
    self.source = source
    import re
    if re.search("def", self.source):
      self.name = re.search("def *([^ (]*)", self.source).group(1)
    elif re.search("lambda", self.source):
      self.name = re.search(" *([^ (]*)", self.source).group(1)
    else:
      print("Warning: Could not parse function name.")
      self.name = ""
    
  def run(self, *args):
    exec(self.source, globals())
    # print(type(args))
    return eval(self.name + f"(*args)")
  
  def __repr__(self):
    return f"PaperData Function Object.\nCall `.run(*args)` to run the function.\nSource:\n{self.source}"

def custom_decoder(dct):
  if '_TYPE_NDARRAY_LIST' in dct:
    return np.array(dct['_TYPE_NDARRAY_LIST'])
  elif '_TYPE_PYTHON_FUNCTION' in dct:
    source = dct['_TYPE_PYTHON_FUNCTION']
    func = Function(source)
    return func 
  elif '_TYPE_MATPLOTLIB_FIG' in dct:
    pickled = dct['_TYPE_MATPLOTLIB_FIG']
    decoded = base64.b64decode(pickled.encode("ascii"))
    fig = pickle.loads(decoded)
    return fig 
  elif '_TYPE_PICKLE_BYTES' in dct:
    pickled = dct['_TYPE_PICKLE_BYTES']
    decoded = base64.b64decode(pickled.encode("ascii"))
    return decoded 
  return dct

class Paper:
  
  def __init__(self):       
    self.name = None
    self.email = None
    self.token = None
  
  def __str__(self):
      print_str = f"Paper {self.DOI}:\n"
      return print_str + self.items.__str__()

  def submit(self):

    if self.name is None:
      print("Please enter your name:")
      self.name = input()
      
    if self.email is None:
      print("Please enter your academic email (university domains only):")
      self.email = input()
    
    contents = self.__dict__.copy()
    temp_dict = json.dumps(contents["items"],cls=CustomEncoder).encode("utf-8")
    contents["items"]  = json.loads(temp_dict)
    # contents = json.dumps({"paper": self.__dict__}, cls=CustomEncoder)#.encode("utf-8")

    try:   
      response = requests.post(server + "submitdata", json={"paper": contents})
      response_json = json.loads(response.text)
      if response_json['status'] == 'FAILED':
        print("Submission failed.", response_json['result'])
      elif response_json['status'] == 'TOKEN':
        print("Please check your email to get the authorization token, and enter it here:")
        contents["token"] = input()
        
        response = requests.post(server + "submitdata", json={"paper": contents})
        # response = requests.post(server + "submitdata", contents)
        response_json = json.loads(response.text)

        if response_json['status'] == 'FAILED':
          print("Submission failed.", response_json['result'])
        elif response_json['status'] == "SUCCEEDED":
          print("Submission succeded!")
        else: 
          print("Error: Wrong code.")
      
      elif response_json['status'] == "SUCCEEDED":
          print("Submission succeded!")
      else: 
        print("Error: Wrong code.")
      
    except Exception as e:
      print(e)
      print("Submission failed.")
      
      
def get_paper(DOI):
  try:
    response = requests.get(server + f'getpaper?DOI={DOI}')
  except Exception as e:
    print(e)
    return -2

  response_json = json.loads(response.text, object_hook=custom_decoder)
  res = response_json['result']
    
  if type(res) is dict:
    # fill with db
    print(f"Paper: {res['DOI']}", res["title"], "\n")
    print(f"Paper data record found! Find the data in `.items` and `.metadata`.")
    paper = Paper()
    paper._id = res["_id"]
    paper.DOI = res["DOI"]
    paper.title = res["title"]
    paper.metadata = res["metadata"]
    paper.updated_by = res["updated_by"]    
    paper.items = res["items"]
    
  elif response_json["status"] == "NO_DOI": # DOI invalid 
    print(res)
    return response_json["status"]
  else: # response_json["status"] == "NO_RECORD"
    print(f"Paper {DOI}: ", response_json["metadata"]["title"], "\n")
    print(res)
    paper = Paper()
    paper.DOI = DOI
    paper.title = response_json["metadata"]["title"]
    paper.metadata = response_json["metadata"]
    paper.updated_by = {"update_count": 0}
    paper.items = {}
    return paper
  
  return paper

def submit_data(DOI):
  
  paper = get_paper(DOI)
  
  if paper == "NO_DOI": # DOI invalid 
    return
  elif paper.updated_by["update_count"] == 0:
    # create new paper 
    print("Creating new record.")
    print("Update `.items` dictionary with new data and `.submit()`.")
  else: # paper found
    print("Update `.items` dictionary with new data and `.submit()`.")
    
  return paper

print("Welcome to PaperData!")
print("Call `get_paper(DOI)` to retrieve a paper's data.")
print("Call `submit_data(DOI)` to submit new paper data.")
