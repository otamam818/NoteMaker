# Transformers

This is where all the transformation functions are held, whether it be string transformations or other future potential transformation functions.
- The string_transf.py file contains all functions for returning strings. Its
  	intention is to be beginner friendly  
  `RULE`: All the functions in this file must return a string  
  `RULE`: All functions must state whether they are *simple* or *complex*  
     **Simple**: Rules that take a string as an argument and return another 
                 string with optional options for where the cursor should be  
    **Complex**: Rules that use the text inside the argument string as a
                 parameter to perform a function based on that parameter.  
  `NOTE`: Some functions can take and make configuration options for the app 
          in order to perform a string transformation
