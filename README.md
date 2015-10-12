# Spintax Framework
The Spintax is a widely used format for text generation in the SEO world. Thus, here is some Python code for executing common operations on this format, such as basic spinning, etc.

## Requirements
- Python 2.7+

## Code samples

### Basic content spinning
	from spin import Spin
	# From string
	color_spin = Spin("My favorite color is {red|green|blue}{.|!}")
	# From file
	color_spin = Spin("path/to/my/masterspin/file")
	
	color_spin.unspun()
And the possible results are:

	My favorite color is red.
	My favorite color is red!
	My favorite color is green.
	My favorite color is green!
	My favorite color is blue.
	My favorite color is blue!
