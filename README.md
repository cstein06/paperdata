# PaperData

PaperData is a database with a simple python interface to record and access data contained in scientific papers, including figure data points, result tables, method parameters or raw data. 

Sharing paper contents allows for quantitative follow-up work, including comparisons between studies, computer modelling, meta-studies and reproducibility, for any scientific domain.  

[Click here for an online usage demo](https://colab.research.google.com/drive/1ekgu4QaY-OXwAiqG27GqWnB7V1N3QeQh?usp=sharing)

### Quick start

Simply download the `paperdata.py` file or clone the repo:
```bash
git clone https://github.com/cstein06/paperdata
cd paperdata
```

## Download Demo

The library is easy to access, with the content indexed by DOI and structured in python dictionaries.

```pycon
>>> import matplotlib.pyplot as plt
>>> import paperdata

>>> paper = paperdata.get_paper(DOI='10.1038/s41586-021-03514-2')

Paper: 10.1038/s41586-021-03514-2 Fast odour dynamics are encoded in the olfactory system and guide behaviour. 

Paper data record found! Find the data in `.items` and `.metadata`.

>>> fig = paper.items['Ext. Fig. 1-a']
>>> print(fig)

PaperData item. Attributes: ['Vr', 'Vrm', 'times', 'caption', 'plot']

>>> plt.plot(fig.times, fig.Vr, c="k");     ### Easily access or plot the data

>>> fig.plot();     ### Or use plot function provided by the authors
```

![Plot figure](https://github.com/cstein06/paperdata/blob/main/sina.png?raw=true)

## Upload Demo

You can organize your items freely, making sure the content is self-explanatory with the aid of the paper. You can include a range of content types, including dictionaries, lists, strings, numpy arrays, pickled data, pyplot figures and functions.

```python
import matplotlit.pyplot as plt
import paperdata

paper = paperdata.submit_data(DOI='123.1234')

figure = paper.new_item("Fig1")

figure.X = [0, 100, 200, 300, 400]
figure.Y = [0.3, 0.5, 1.5, 3.5, 4.0]
figure.title = "Demo data"

paper.submit()
```
