# food2vec
Food vectors. Live demo at [https://altosaar.github.io/food2vec/](https://altosaar.github.io/food2vec/), blog post with more information and pretty plots here: https://jaan.io/food2vec-augmented-cooking-machine-intelligence/

## Data
Get the data and preprocess it:
```
cd dat
./download_data.sh
./preprocess_data.sh
```

## Usage
Train a model on the recipes dataset:
```
git clone git@github.com:altosaar/food2vec.git
cd food2vec
git submodule update --init
cd food2vec/src/sentence_word2vec
git submodule update --init
./compile_ops.sh
# run word2vec with the recipes as context
python word2vec_optimized.py --train_data ../../dat/recipes --interactive --save_path /tmp --subsample 0 --eval 0 --interactive --embedding_size 100
```

## Visualization & embedding exploration tools
```
# make the t-SNE plot
cd ../../
# run t-sne and make the plots for the ingredient embeddings
jupyter notebook ./src/plot_ingredients_recipes.ipynb
# view the analogy tool on a browser
open index.html
```

## Contributing

Pull requests and all feedback welcome! Please file an issue if you run into problems replicating the results.

TODOs:
* fit a better model (e.g. the exact multi-class regression implemented in this repo at [https://github.com/altosaar/food2vec/blob/master/src/food2vec.py](https://github.com/altosaar/food2vec/blob/master/src/food2vec.py)) -- if you manage to get better results than the live demo at https://altosaar.github.io/food2vec/ just submit a pull request with the new `assets/data/wordVecs.js` and I'll happily update it :)
* compare the above model embeddings to the `word2vec_optimized.py` embeddings
* make the UI of the website more user-friendly and mobile-friendly

## Acknowledgments
Thanks to Anthony for open-sourcing a [javascript embedding browser](https://github.com/turbomaze/word2vecjson) -- the one here is heavily based on it.
