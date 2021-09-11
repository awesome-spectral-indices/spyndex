Contributing
============

There are two ways to contribute to spyndex:

1. Contribute with a new Spectral Index to the `Awesome Spectral Indices <https://github.com/davemlz/awesome-ee-spectral-indices>`_ GitHub repository.
2. Contribute with new methods or improvementes to spyndex!

If you choose to contribute directly to spyndex, check the following guide!

Guide
-----

Contributions to spyndex are welcome! Here you will find how to do it:

- **Bugs:** If you find a bug, please report it by opening an issue. if possible, please attach the error, code, version, and other details. 

- **Fixing Issues:** If you want to contributte by fixing an issue, please check the spyndex issues: contributions are welcome for open issues with labels :code:`bug` and :code:`help wanted`.

- **Enhancement:** New features and modules are welcome! You can check the spyndex issues: contributions are welcome for open issues with labels :code:`enhancement` and :code:`help wanted`.

- **Documentation:** You can add examples, notes and references to the spyndex documentation by using the NumPy Docstrings of the spyndex documentation, or by creating blogs, tutorials or papers.

Steps
~~~~~

First, fork the `spyndex <https://github.com/davemlz/spyndex>`_ repository and clone it to your local machine. Then, create a development branch::

   git checkout -b name-of-dev-branch
   
Create a new method, or fix a bug:

.. code-block:: python
   
   def my_new_method(x,other):
        '''Returns the addition of and image and a float.
    
        Parameters
        ----------    
        x : float
            Float to add.
        other : float
            Float to add.

        Returns
        -------    
        float
            Addition of two floats.

        Examples
        --------
        >>> import spyndex
        >>> spyndex.my_new_method(0.5,0.5)
        1.0
        '''
        return x + other

Remember to use `Black <https://github.com/psf/black>`_ and `isort <https://pycqa.github.io/isort/>`_!

In order to test additions, you can use :code:`pytest` over the :code:`tests` folder::

   pytest tests
   
If you have added a new feature, please include it in the tests.

To test across different Python versions, please use :code:`tox`.

Now it's time to commit your changes and push your development branch::

   git add .
   git commit -m "Description of your work"
   git push origin name-of-dev-branch
  
And finally, submit a pull request.