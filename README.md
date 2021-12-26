# PaperData

PaperData is a simple python interface to record and access data contained in scientific papers, including figure data points, result tables, method parameters or raw data. 

Sharing paper contents allows for quantitative follow-up work, including comparisons, computer modelling, meta-studies and reproducibility. 

[Usage demo notebook](https://colab.research.google.com/drive/1ekgu4QaY-OXwAiqG27GqWnB7V1N3QeQh?usp=sharing)

### Quick start

Simply download the `paperdata.py` file or clone the repo:
```bash
git clone https://github.com/cstein06/paperdata
cd paperdata
```

## Download Demo

The library is easy to access, with the content structured in python dictionaries and can be used for any scientific domain.  

```python
import matplotlit.pyplot as plt
import paperdata

paper = paperdata.get_paper(DOI='342.2932')

print(paper.items)

{'fig1': {
  'X': [0, 100, 200, 300, 400],
  'Y': [0.3, 0.5, 1.5, 3.5, 4.0],
  'conditions': {‘t_0(s)’ = 100, ‘t_final(s)’ = 1000}},
'fig2': {
  'plot_data': [[0, 200, 400], [0.4, 0.5, 0.9]],
  'raw_data': [3x100 Array]}}

plt.plot(paper.items["fig1"]["X"], paper.items["fig1"]["Y"])

plt.bar(paper.items["fig2"]["plot_data"][0], paper.items["fig2"]["plot_data"][1])
```

## Upload Demo

You can organize your items freely, making sure the content is self-explanatory with the aid of the paper. You can include a range of content types, including dictionaries, lists, strings, numpy arrays, pickled data, pyplot figures and functions.

```python
import matplotlit.pyplot as plt
import paperdata

paper = paperdata.submit_data(DOI='342.2932')

paper.items["Fig. 1"] = {}
paper.items["Fig. 1"]["X"] = [0, 100, 200, 300, 400]
paper.items["Fig. 1"]["Y"] = [0.3, 0.5, 1.5, 3.5, 4.0]
paper.items["Fig. 1"]["plotting"] = lambda X,Y: plt.plot(X,Y)

paper.submit()
```
