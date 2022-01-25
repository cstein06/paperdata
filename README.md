# PaperData

PaperData is a database with a simple python interface to record and access data contained in scientific papers, including figure data points, result tables, method parameters or raw data. 

Sharing paper contents allows for quantitative follow-up work, including comparisons between studies, computer modelling, meta-studies and reproducibility, for any scientific domain.  

[Usage demo notebook](https://colab.research.google.com/drive/1ekgu4QaY-OXwAiqG27GqWnB7V1N3QeQh?usp=sharing)

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

>>> print(paper.items)

{'Ext. Fig. 1-a': {'Vr': array([[ 0., -0.22517071,  0.11778803, ..., -1.59946409, -0.34829094,  1.0544314 ]]),
                   'Vrm': array([0.0262406 , 0.02080717, 0.01293134, ..., 0.03627794, 0.04352064, 0.03727998]),
                   'times': array([-0.1  , -0.099, -0.098, ...,  1.897,  1.898,  1.899])},
                   'caption': 'Membrane voltage relative to baseline of a single model OSN in response to a 10-ms odour pulse. Black traces are individual trials; red trace is average over 20 trials. OSN spike threshold has been set high enough to prevent spiking to illustrate the subthreshold voltage time course.'}
            
>>> fig = paper.items['Ext. Fig. 1-a']
>>> plt.plot(fig["times"], fig["Vr"], c="k");
```

## Upload Demo

You can organize your items freely, making sure the content is self-explanatory with the aid of the paper. You can include a range of content types, including dictionaries, lists, strings, numpy arrays, pickled data, pyplot figures and functions.

```python
import matplotlit.pyplot as plt
import paperdata

paper = paperdata.submit_data(DOI='123.1234')

paper.items["Fig. 1"] = {}
paper.items["Fig. 1"]["X"] = [0, 100, 200, 300, 400]
paper.items["Fig. 1"]["Y"] = [0.3, 0.5, 1.5, 3.5, 4.0]
paper.items["Fig. 1"]["plot_f"] = lambda X,Y: plt.plot(X,Y,c="k")

paper.submit()
```
