# food2vec
Food vectors. Live demo at [https://altosaar.github.io/food2vec/](https://altosaar.github.io/food2vec/), blog post with more information and pretty plots here: https://jaan.io/food2vec-augmented-cooking-machine-intelligence/

## Usage
Train a model on the recipes dataset, replicate the results from the [blog post](https://jaan.io/food2vec-augmented-cooking-machine-intelligence/):
```
git clone git@github.com:altosaar/food2vec.git
echo "[submodule "src/sentence_word2vec"]
        path = src/sentence_word2vec
        url = https://github.com/altosaar/sentence_word2vec.git
[submodule "src/fastText"]
        path = src/fastText
        url = https://github.com/altosaar/fastText" > .gitmodules
git submodule update --init
cd food2vec/src
./blog_experiment.sh
```

## Visualization & embedding exploration tools
```
# run t-sne and make the plots for the ingredient embeddings
jupyter notebook ./src/plot_ingredients_recipes.ipynb
```

## Embedding plot.ly plots to host them yourself
https://gist.github.com/altosaar/67d8456ad28acd1abb497f1950d8de8a

## Contributing
Pull requests and all feedback welcome! Please file an issue if you run into problems replicating the results.

TODOs:
* get more data
* convert jupyter notebook for plotting into one python script
* write scripts to figure out the right vocabulary
* fit a better model (e.g. the exact multi-class regression implemented in this repo at [https://github.com/altosaar/food2vec/blob/master/src/food2vec.py](https://github.com/altosaar/food2vec/blob/master/src/food2vec.py)) -- if you manage to get better results than the live demo at https://altosaar.github.io/food2vec/ just submit a pull request with the new `assets/data/wordVecs.js` and I'll happily update it :)
* compare the above model embeddings to the `word2vec_optimized.py` embeddings
* make the UI of the website more user-friendly and mobile-friendly

## Acknowledgments
Thanks to Anthony for open-sourcing a [javascript embedding browser](https://github.com/turbomaze/word2vecjson) -- the one here is heavily based on it.
