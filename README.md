# Spintax Framework
The Spintax is a widely used format for text generation (content spinning) in the SEO world. Thus, here is some Python code for executing common operations on this format, such as basic spinning, etc.

## Requirements
- Python 3.4
- Scipy 0.16.0
- Numpy 1.10.0
- NLTK 3.0.5
- Matplotlib 1.4.3

## Code samples

### Basic content spinning
	from spin import Spin
	# From string
	color_spin = Spin("My favorite color is {red|green|blue}{.|!}")
	# From file
	color_spin = Spin(input_file="path/to/my/masterspin/file")
	
	color_spin.unspin()
And the possible results are:

	My favorite color is red.
	My favorite color is red!
	My favorite color is green.
	My favorite color is green!
	My favorite color is blue.
	My favorite color is blue!

### Build a tree representation

	spin = Spin("{My name is|I{ am|'m}} John Doe and I {truly|really} love the {spintax|spin framework}{.|!}")
	tree = spin.build_tree()

This masterspin can be represented as a decision tree, such as:

![Tree representation](https://github.com/aduroy/SpinFramework/blob/master/data/examples/tree.png)

Print it in console:

	print(tree)

And get:

	AND
	__OR
	____My name is
	____AND
	______I
	______OR
	________ am
	________'m
	__ John Doe and I 
	__OR
	____truly
	____really
	__ love the 
	__OR
	____spintax
	____spin framework
	__OR
	____.
	____!
Print a JSON format:

	print(tree.to_json())

And get:

	{"and": [{"or": [{"value": "My name is"}, {"and": [{"value": "I"}, {"or": [{"value": " am"}, {"value": "'m"}]}]}]}, {"value": " John Doe and I "}, {"or": [{"value": "truly"}, {"value": "really"}]}, {"value": " love the "}, {"or": [{"value": "spintax"}, {"value": "spin framework"}]}, {"or": [{"value": "."}, {"value": "!"}]}]}

Moreover, in order to reduce the chances of getting filtered by Google's Duplicate Content algorithm, you might want to visualize the limits of your masterspin. In other words, how many spuns can you generate before reaching a too high similarity between them? For this, several measures are provided, such as:
* Jaccard similarity
* Jaro-Winkler similarity
* Cosine similarity

For instance, by generating 25 spuns and comparing them 2 by 2, we can get the following charts:

	# Will display graphs
	spin.plot_duplicate_evolution(25)
	# Or save it to a file
	spin.plot_duplicate_evolution(25, 'path/to/file.png')

![Plot representation](https://github.com/aduroy/SpinFramework/blob/master/data/results/plot_representation.png)

All of them show a limit around 14 generations until we get 100% duplication.
