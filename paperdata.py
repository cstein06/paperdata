import sqlite3, json, numpy, pickle, bson, base64

import matplotlib.pyplot as plt
import matplotlib.figure
import numpy as np

import types, inspect, re, codecs

import requests
  
# print("*** Using local server. ***")
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
        elif isinstance(obj, types.MethodType):
            try: 
              source = inspect.getsource(obj)
            except:
              source = globals()[f"_source_{obj.__name__}"]
            return {"_TYPE_ITEM_METHOD": {"name":obj.__name__, "source":source}}
        elif isinstance(obj, types.FunctionType):
          raise Exception('Please set functions as methods of an Item.')
        #     try: 
        #       source = inspect.getsource(obj)
        #     except:
        #       source = globals()[f"_source_{obj.__name__}"]
        #     return {"_TYPE_PYTHON_FUNCTION": {"name":obj.__name__, "source":source}}
        elif isinstance(obj, matplotlib.figure.Figure):
            fig_pic = pickle.dumps(obj)
            encoded = base64.b64encode(fig_pic).decode("ascii")
            return {"_TYPE_MATPLOTLIB_FIG": encoded}
        elif isinstance(obj, bytes):
            return {"_TYPE_PICKLE_BYTES": base64.b64encode(obj).decode("ascii")} 
        else:
            return super(CustomEncoder, self).default(obj)
          
def custom_decoder(dct):
  if '_TYPE_NDARRAY_LIST' in dct:
    return np.array(dct['_TYPE_NDARRAY_LIST'])
  elif '_TYPE_ITEM_METHOD' in dct:
    method = dct['_TYPE_ITEM_METHOD']
    
    globals()[f"_source_{method['name']}"] = method['source']
    
    exec(method["source"], globals())
    return globals()[method["name"]]
#   elif '_TYPE_PYTHON_FUNCTION' in dct:
#     method = dct['_TYPE_PYTHON_FUNCTION']
    
#     globals()[f"_source_{method['name']}"] = method['source']
    
#     exec(method["source"], globals())
#     return {"_FUNCTION_WITH_SOURCE": [globals()[method["name"]], method["source"]]}
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

class Item:
  def __init__(self, initial_data=None):
    if initial_data is not None:
      for key in initial_data:
        if isinstance(initial_data[key], types.FunctionType):
          setattr(self, key, initial_data[key].__get__(self))
          name = initial_data[key].__name__
          setattr(self, "_source_"+key, globals()["_source_"+name])
        else:
          setattr(self, key, initial_data[key])

  def __str__(self):
    return f"PaperData item. Attributes: {list(self.__dict__.keys())}"
    # return "%s: %r" % (self.__class__, self.__dict__)
    
class Paper:
  
  def __init__(self):       
    self.name = None
    self.email = None
    self.token = None
  
  def __repr__(self):
      print_str = f"Paper {self.DOI}. Items: "
      return print_str + str(list(self.items.keys()))
      # return print_str + self.items.__str__()
    
  def new_item(self, item_name):
    item = Item()
    self.items[item_name] = item
    print(f"Added '{item_name}' to .items")
    return item
    
  def submit(self):

    print("Please enter your name:")
    self.name = input()
      
    print("Please enter your academic email (university domains only):")
    self.email = input()
        
    contents = self.__dict__.copy()
    contents["items"] = contents["items"].copy()
    
    for item in contents["items"]:
      contents["items"][item] = json.loads(json.dumps(contents["items"][item].__dict__,cls=CustomEncoder).encode("utf-8"))
    
#     temp_dict = json.dumps(contents["items"],cls=CustomEncoder).encode("utf-8")
#     contents["items"]  = json.loads(temp_dict)
    
    # contents = json.dumps({"paper": self.__dict__}, cls=CustomEncoder)#.encode("utf-8")    

    try:   
      response = requests.post(server + "submitdata", json={"paper": contents})
      # response = requests.post(server + "submitdata", data=contents)
      
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
      
def search_author(partial_name):
  '''Search if author names contains this string.'''
  try:
    response = requests.get(server + f'search_author?name={partial_name}')
  except Exception as e:
    print(e)
    return -2
  results = response.json()["result"]
  if len(results):
    print(f"Found the following data records for author '{partial_name}':")
  else:
    print(f"Found no records for author '{partial_name}''.")
  return results
  
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
    print("\nFor submitting additional data, change the data in `.items` or create new items with `.new_item()`, fill them with data and `.submit()`.")
    paper = Paper()
    paper._id = res["_id"]
    paper.DOI = res["DOI"]
    paper.title = res["title"]
    paper.metadata = res["metadata"]
    paper.updated_by = res["updated_by"]    
    paper.items = res["items"]
    for key,value in paper.items.items():
      paper.items[key] = Item(initial_data=value)
    
  elif response_json["status"] == "NO_DOI": # DOI invalid 
    print(res)
    return response_json["status"]
  else: # response_json["status"] == "NO_RECORD"
    print(f"Paper {DOI}: ", response_json["metadata"]["title"], "\n")
    # print(res)
    print("No data records found. Find the metadata in `.metadata`.\n\nFor submitting data, create new items with `.new_item()`, fill them with data and `.submit()`.")
    paper = Paper()
    paper.DOI = DOI
    paper.title = response_json["metadata"]["title"]
    paper.metadata = response_json["metadata"]
    paper.updated_by = {"update_count": 0}
    paper.items = {}
    return paper
  
  return paper

print("Welcome to PaperData!")
print("Call:")
print("`search_author(partial_name)` to list author papers with a data record.")
print("`get_paper(DOI)` to retrieve paper data.")
print("`submit_data(DOI)` to submit new paper data.")
